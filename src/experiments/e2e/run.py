"""
main script to run experiments.
"""

import ast

import numpy as np
from tqdm import tqdm
import argparse
import dataclasses
import json
import os
import random
from collections import Counter
from datetime import datetime
from typing import Dict, List
import pandas as pd
import wandb

from src.common.config import Config
from src.common.logger import get_logger
from src.consts import (
    FULL_MTE_FIELD,
    PRED_MTE_FIELD,
    ACC_MTE_FIELD,
    ACC_AT_1_FIELD,
    ACC_AT_3_FIELD,
    ACC_AT_MAJORITY_FIELD,
    NUM_EXAMPLES_FIELD,
    NUM_ABSTAINS_FIELD,
    CONTEXT_ANSWER_SEP,
)
from src.dataclasses import (
    QuestionV1,
    QuestionWithAnswer,
    format_decompsition_string,
    format_ir_decomposition,
)
from src.dataset_readers.dataset_readers_factory import DatasetReadersFactory
from src.dataset_readers.readers.dataset_reader import DatasetReader
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.gpt3_accessors.gpt_accessor_factory import GptAccessorFactory
from src.opeanai.utils import gpt_simple_generator
from src.pred_evaluators.evaluators_factory import EvaluatorsFactory
from src.pred_evaluators.pred_evaluators.base_evaluator import Evaluator
from src.prompting.prompt_factory import PromptFactoryDict
from src.serpapi.serpapi import get_string_hash, google
from src.serpapi.serpapi import get_question_wiki_snippet

logger = get_logger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_path",
        type=str,
        default="src/config/2wikihop/config_with_retrieval_contexts_first.json",
        help="Config file path",
    )
    return parser.parse_args()


def _call_gpt_for_entailment_with_batching(
    questions: List[Dict],
    evaluator: Evaluator,
    entailment_values: Dict,
    prefix="mte",
    batch_size: int = 10,
) -> List[Dict]:
    """
    call gpt for entailment with batching.
    will sort the input to batches, call gpt for each batch and return results as a list of questions
    """

    def batch_iterable(iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]

    batches = [x for x in batch_iterable(list(questions), batch_size)]

    logger.info(f"Running entailment with batching.")
    for batch in tqdm(batches):
        input_prompts = [question[f"{prefix}_entailment_input"] for question in batch]
        # call gpt-3
        gpt_trace_entailment, _ = gpt_simple_generator(
            prompt=input_prompts,
            model=entailment_values.get("model"),
            stop_condition=entailment_values.get("stop_condition"),
            temperature=0,
        )

        # change to a list if a string was returned
        gpt_trace_entailment = (
            [gpt_trace_entailment]
            if type(gpt_trace_entailment) == str
            else gpt_trace_entailment
        )

        # iterate questions in batch
        for i, question in enumerate(batch):
            # add prediction
            gpt_res = gpt_trace_entailment[i]
            question[f"{prefix}_{FULL_MTE_FIELD}"] = gpt_res

            if "the answer is:" in question[f"{prefix}_{FULL_MTE_FIELD}"]:
                # take the final answer
                final_answer = gpt_res.split("the answer is:")[-1].strip()

                # remove the dot if it's the last character
                if len(final_answer) and final_answer[-1] == ".":
                    final_answer = final_answer[:-1]
                question[f"{prefix}_{PRED_MTE_FIELD}"] = final_answer.replace(
                    "\n", ""
                ).strip()
                if "unknown" in question[f"{prefix}_{PRED_MTE_FIELD}"].lower():
                    mte_acc = None
                else:
                    mte_acc = evaluator.evaluate(
                        question[f"{prefix}_{PRED_MTE_FIELD}"]
                        .strip()
                        .replace("\n", ""),
                        question["metadata_gold_answer"]
                        if "metadata" not in question
                        else question["metadata"]["gold_answer"],
                    )
            else:
                mte_acc = None
            question[f"{prefix}_{ACC_MTE_FIELD}"] = mte_acc
    return list(questions)


def _set_entailment_input(
    question: Dict,
    question_prompt: str,
    entailment_values: Dict,
    prefix="mte",
    seed=0,
    sa_contexts_first=None,
) -> Dict:
    """
    adds gpt input field in place
    """

    def _get_decomps(use_ir: bool) -> List[str]:
        """
        get the list of facts from decompositions, either the contexts (use_ir) or the QA facts
        """
        decompositions = []

        # add question ir context if configged
        if entailment_values.get("retrieve_orig_question"):
            decompositions.append(
                [
                    question["question"]["question"]
                    + " | "
                    + get_question_wiki_snippet(question["question"]["question"])
                ]
            )

        # limit decomps, for example for ste
        max_decompositions = entailment_values.get("max_decompositions")
        if max_decompositions is None:
            max_decompositions = 100

        for i, decomposition in enumerate(
            question["question"]["decompositions"][:max_decompositions]
        ):
            # format decompositions for the context
            decomp = format_decompsition_string(
                decomposition.replace("Follow up:\n\n", "Follow up: ")
                .replace("Intermediate answer:\n\n", "Intermediate answer: ")
                .replace("So the final answer is:\n\n", "So the final answer is: ")
            )
            if use_ir is not None:
                decomp = format_ir_decomposition(
                    decomposition.replace("Follow up:\n\n", "Follow up: ")
                    .replace("Intermediate answer:\n\n", "Intermediate answer: ")
                    .replace("So the final answer is:\n\n", "So the final answer is: ")
                    .replace("Context:\n\n", "Context: "),
                    contexts_first=sa_contexts_first,
                )
            decomp_facts = []
            for j, decomp_step in enumerate(decomp):
                decomp_step = dataclasses.asdict(decomp_step)

                # this is when the model decides to give a direct answer (no intermediate steps).

                if j == 0 and decomp_step["gpt_3_ans"]:
                    decomp_facts.append(
                        (
                            question["question"]["question"]
                            + " "
                            + decomp_step["gpt_3_ans"]
                        )
                    )
                # intermediate steps
                if not decomp_step["gpt_3_ans"]:
                    if (
                        decomp_step["question"] is not None
                        and decomp_step["answer"] is not None
                        and use_ir is None
                    ):
                        decomp_facts.append(
                            decomp_step["question"] + " " + decomp_step["answer"]
                        )
                    # print("decomp_step: ", decomp_step)  # todo: tw - delete
                    # print("decomposition: ", decomposition)  # todo: tw - delete
                    # TW - added in case intermediate answer is None
                    questn = (
                        ""
                        if decomp_step["question"] is None
                        else decomp_step["question"]
                    )
                    if use_ir is not None:
                        # when doing entailment on retrieved contexts, answer is comprised of [context][sep][ans]
                        #   we split it using [sep] to extract just the context (retrieved snippet)
                        if decomp_step["answer"] is None:
                            ans = ""
                        else:
                            retrieved_context, ans = decomp_step["answer"].split(
                                CONTEXT_ANSWER_SEP
                            )
                            ans = "| " + retrieved_context
                        decomp_facts.append(questn + " " + ans)
            decompositions.append(decomp_facts)
        return decompositions

    retrieved_contexts = _get_decomps(use_ir=True)
    facts = _get_decomps(use_ir=None)
    context_list = [d for f in retrieved_contexts for d in f]
    fact_list = [d for f in facts for d in f]
    # add the context to the suffix
    prompt_suffix = "\n"
    if entailment_values.get("shuffle_context"):
        seed = random.randint(1, 1000)
        random.seed(seed)
        random.shuffle(context_list)
        random.shuffle(fact_list)
        question[f"{prefix}_shuffle_seed"] = seed

    # add contexts
    if entailment_values.get("use_ir_contexts"):
        prompt_suffix += "\n\n".join(context_list) + "\n"
        if entailment_values.get("use_qa_pairs"):
            prompt_suffix += "\nDerived facts:\n"

    # add qa pairs
    if entailment_values.get("use_qa_pairs"):
        prompt_suffix += "\n".join(fact_list) + "\n"

    # add to prompt suffix
    prompt_suffix += "\nQuestion:" + "\n" + question["question"]["question"] + "\n"
    prompt_suffix += "\nAnswer:"
    question[f"{prefix}_entailment_input"] = question_prompt + prompt_suffix

    return question


def _populate_decompositions(
    example: Dict,
    prompt: str,
    dataset_reader: DatasetReader,
    gpt_accessor: GptAccessor,
    evaluator: Evaluator,
    decomposition_cache_dir: str,
    num_decompositions: int,
) -> Dict:
    """ """
    example = dataset_reader.parse_example(example)
    question = QuestionV1(
        question=example.question,
        prompt=prompt,
        gpt3_accessor=gpt_accessor,
        num_decompositions=num_decompositions,
    )
    question.populate()

    gpt_answers = [
        s[-1].gpt_3_ans[:-1] if s[-1].gpt_3_ans[-1] == "." else s[-1].gpt_3_ans
        for s in question.decompsition_steps
        if len(s) > 0 and s[-1].gpt_3_ans is not None and len(s[-1].gpt_3_ans) > 0
    ]
    question_with_answer = QuestionWithAnswer(
        question=question, answers=None, gpt_answers=gpt_answers
    )
    question_with_answer_dict = dataclasses.asdict(question_with_answer)
    results = {}
    if len(question_with_answer_dict["gpt_answers"]) > 0:
        results["acc@1"] = evaluator.evaluate(
            question_with_answer_dict["gpt_answers"][0], example.gold_answer
        )
        results["acc@3"] = max(
            [
                evaluator.evaluate(ans, example.gold_answer)
                for ans in question_with_answer_dict["gpt_answers"]
            ]
        )
        majority_prediction = Counter(
            [y.lower() for y in question_with_answer_dict["gpt_answers"]]
        ).most_common(n=1)[0][0]
        majority_prediction_at_three = Counter(
            [y.lower() for y in question_with_answer_dict["gpt_answers"][:3]]
        ).most_common(n=1)[0][0]
        results["acc@majority"] = evaluator.evaluate(
            majority_prediction, example.gold_answer
        )
        results["acc@majority_3"] = evaluator.evaluate(
            majority_prediction_at_three, example.gold_answer
        )

    else:
        results["acc@1"] = False
        results["acc@3"] = False
        results["acc@majority"] = False
        results["acc@majority_3"] = False
    dataset_metadata_fields = Config().get("dataset.metadata_fields")
    results["metadata"] = {
        **{k: v for k, v in example.metadata.items() if k in dataset_metadata_fields},
        **{k: v for k, v in dataclasses.asdict(example).items() if k != "metadata"},
    }
    logger.info(results)
    question_with_answer_dict.update(results)

    # save example
    filename = get_string_hash(example.question)
    with open(f"{decomposition_cache_dir}/{filename}.json", "w") as json_file:
        json.dump(question_with_answer_dict, json_file)
    return question_with_answer_dict


def _report_results(suffix: str, examples: List[Dict]):
    """ """
    questions_with_entailment_df = pd.DataFrame(examples)
    res = {
        f"{NUM_EXAMPLES_FIELD}_{suffix}": questions_with_entailment_df.shape[0],
        f"{NUM_ABSTAINS_FIELD}_{suffix}": questions_with_entailment_df[
            f"mte_{ACC_MTE_FIELD}"
        ]
        .isna()
        .sum(),
        f"{ACC_AT_1_FIELD}_{suffix}": questions_with_entailment_df[
            ACC_AT_1_FIELD
        ].mean(),
        f"{ACC_AT_3_FIELD}_{suffix}": questions_with_entailment_df[
            ACC_AT_3_FIELD
        ].mean(),
        f"{ACC_AT_MAJORITY_FIELD}_{suffix}": questions_with_entailment_df[
            ACC_AT_MAJORITY_FIELD
        ].mean(),
        f"mte_{ACC_MTE_FIELD}_{suffix}": questions_with_entailment_df[
            f"mte_{ACC_MTE_FIELD}"
        ].mean(),
    }
    for report_func in [logger.info]:
        report_func(res)


def _save_examples(examples: List[Dict], output_path: str):
    """ """
    # format
    for ex in examples:
        # flatten metadata
        if "metadata" in ex:
            for k, v in ex["metadata"].items():
                ex[f"metadata_{k}"] = v
            del ex["metadata"]

        # flatten decompositions
        num_decompositions = len(ex["question"]["decompositions"])
        for i in range(num_decompositions):
            ex[f"decomposition_{i}"] = ex["question"]["decompositions"][i]

    # save
    pd.DataFrame(examples).to_csv(output_path)


def _read_csv(file_path: str) -> List[Dict]:
    """
    read decomps from a csv file
    """
    logger.info(f"Reading input data form csv file at path: {file_path}")
    df = pd.read_csv(file_path)
    data = df.to_dict("rows")
    for x in data:
        x["question"] = ast.literal_eval(x["question"])
    num_rows = len(data)
    logger.info(f"Read {num_rows} from file")
    return data


def _run_decompositions(
    examples: List[Dict],
    cache_dir: str,
    output_dir: str,
    experiment_unique_name: str,
    dataset: DatasetReader,
    prompt: str,
    gpt_accessor: GptAccessor,
    evaluator: Evaluator,
    num_decompositions: int,
) -> List[Dict]:
    if cache_dir is None:
        decomposition_cache_dir = (
            f"{output_dir}/{experiment_unique_name}/decompositions"
        )
        os.makedirs(decomposition_cache_dir, exist_ok=True)
        logger.info(f"Saving decompositions in: {decomposition_cache_dir}")
        questions_with_decompositions = [
            _populate_decompositions(
                example,
                prompt,
                dataset,
                gpt_accessor,
                evaluator,
                decomposition_cache_dir,
                num_decompositions,
            )
            for example in tqdm(examples)
        ]
    else:
        logger.info(f"Reading decompositions from: {cache_dir}")
        cached_files = [f for f in os.listdir(cache_dir)]
        cached_decompositions = {}
        for filename in cached_files:
            with open(f"{cache_dir}/{filename}", "r") as f:
                data = json.load(f)
                cached_decompositions[filename] = data
        questions_with_decompositions = cached_decompositions.values()
    return questions_with_decompositions


def run_experiment(config_path: str):
    """ """
    # read config
    Config().load(config_path)
    wandb.init(project="GRE", config=Config()._config)

    # start experiment
    experiment_name = Config().get("experiment_name")
    logger.info(f"Starting experiment: {experiment_name}")
    output_dir = Config().get("output_dir")

    # datetime
    timestamp = datetime.now().timestamp()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d_%m_%Y_%H_%M_%S")
    experiment_unique_name = f"{experiment_name}_{str_date_time}"

    # read dataset
    dataset_name = Config().get("dataset.name")
    logger.info(f"Reading dataset: {dataset_name}.")
    dataset = DatasetReadersFactory().get_instance(dataset_name)
    dataset.read()
    examples = dataset.examples

    # get evaluator
    evaluator_name = Config().get("evaluator")
    logger.info(f"Using evaluator: {evaluator_name} to report metrics")
    evaluator = EvaluatorsFactory().get_instance(evaluator_name)

    # decomposition settings
    gpt_accessor_name = Config().get("decomposition.gpt3_accessor")
    prompt_name = Config().get("decomposition.prompt")
    logger.info(
        f"GPT3 accessor for decompositions: {gpt_accessor_name}, with prompt: {prompt_name}"
    )
    gpt_accessor = GptAccessorFactory().get_instance(gpt_accessor_name)
    prompt = PromptFactoryDict[prompt_name]
    num_decompositions = Config().get("decomposition.num_decompositions")

    # abstain settings
    entailment_prompt_name = list(Config().get("entailment").values())[0].get("prompt")
    logger.info(f"Using entailment engine with prompt: {entailment_prompt_name}")
    entailment_prompt = PromptFactoryDict[entailment_prompt_name]

    abstain_prompt_name = Config().get("abstain.prompt")
    logger.info(f"Using entailment engine with prompt: {entailment_prompt_name}")
    abstain_prompt = PromptFactoryDict[abstain_prompt_name]

    # filter examples in prompts
    examples_not_in_prompts = [
        e
        for e in dataset.examples
        if not (
            dataset.parse_example(e).question.lower() in prompt.lower()
            or dataset.parse_example(e).question.lower() in entailment_prompt.lower()
        )
    ]
    num_examples, num_examples_not_in_prompts = len(examples), len(
        examples_not_in_prompts
    )
    num_examples_in_prompt = num_examples - num_examples_not_in_prompts
    logger.info(
        f"Removing {num_examples_in_prompt}/{num_examples} examples. Left with {num_examples_not_in_prompts} examples."
    )
    examples = examples_not_in_prompts

    # sample examples
    num_examples = Config().get("sampling.num_examples")
    if num_examples is not None:
        sampling_seed = Config().get("sampling.seed")
        logger.info(f"Down-sampling to {num_examples} examples.")
        random.seed(sampling_seed)
        examples = random.sample(examples, num_examples)

    # sample from csv
    examples_csv = Config().get("sampling.examples_csv")
    if examples_csv is not None:
        prev_examples = pd.read_csv(examples_csv).to_dict("rows")
        previous_qids = {x["metadata_qid"] for x in prev_examples}

        # create a dataset with the previous examples
        prev_examples_dataset, prev_examples_dataset_qids = [], set()
        for x in examples:
            if x["qid"] in previous_qids and x["qid"] not in prev_examples_dataset_qids:
                prev_examples_dataset.append(x)
                prev_examples_dataset_qids.add(x["qid"])

        # assign the new dataset for the examples
        examples = prev_examples_dataset

    # retries
    num_retries = Config().get("num_retries")
    logger.info(f"Running with {num_retries} retries.")
    examples_with_answers: List[Dict] = []
    examples_to_answer: List[Dict] = examples  # [207:]  # todo: TW - delete

    # use contexts first format in Self-ask decomposition
    sa_contexts_first = (
        Config().get("decomposition.gpt3_accessor")
        == "gpt_accessor_with_retrieval_context_first"
    )

    for i in range(num_retries + 1):
        # populate question with decomposition
        cache_dir = Config().get("decomposition.cache_dir")
        csv_input_file = Config().get("decomposition.csv_input_file")
        questions_with_decompositions = (
            _run_decompositions(
                examples=examples_to_answer,
                cache_dir=cache_dir if i == 0 else None,
                output_dir=output_dir,
                experiment_unique_name=experiment_unique_name,
                dataset=dataset,
                prompt=prompt,
                gpt_accessor=gpt_accessor,
                evaluator=evaluator,
                num_decompositions=num_decompositions,
            )
            if csv_input_file is None
            else _read_csv(csv_input_file)
        )

        # add input for entailment (for batching)
        for entailment_prefix, entailment_values in Config().get("entailment").items():
            # set num iterations
            iterations = entailment_values.get("iterations")
            if iterations is None:
                iterations = 1

            for k in range(iterations):
                # entailment settings
                entailment_prompt_name = entailment_values.get("prompt")
                logger.info(
                    f"Using entailment engine with prompt: {entailment_prompt_name}"
                )
                entailment_prompt = PromptFactoryDict[entailment_prompt_name]

                for question in questions_with_decompositions:
                    _set_entailment_input(
                        question,
                        entailment_prompt,
                        entailment_values,
                        sa_contexts_first=sa_contexts_first,
                        prefix=f"{k}_{entailment_prefix}",
                    )

                # call gpt with batching, adds results in place
                questions_with_entailment = _call_gpt_for_entailment_with_batching(
                    questions_with_decompositions,
                    evaluator,
                    entailment_values,
                    prefix=f"{k}_{entailment_prefix}",
                )
        # questions_with_abstain = [
        #     _populate_entailment(question, abstain_prompt, evaluator, 0, "abstain")
        #     for question in tqdm(list(questions_with_decompositions))
        # ]

        # save results
        if output_dir is not None:
            output_path = f"{output_dir}/{experiment_unique_name}_{i}.csv"
            logger.info(f"Saving output path to: {output_path}")
            _save_examples(questions_with_entailment, output_path)

        # report results
        _report_results(
            suffix=f"_{experiment_name}_iteration={i}",
            examples=questions_with_decompositions,
        )

        # aggregate for next iteration

        examples_with_answers += [
            q
            for q in questions_with_entailment
            if
            # 'unknown' not in q['abstain_multi_trace_entailment_prediction'].lower()
            # and
            q[f"mte_{ACC_MTE_FIELD}"] is not None
        ]

        # get abstain ids and keep only abstain answers in examples_to_answer
        abstain_ids = {
            q["metadata_qid"]
            for q in questions_with_entailment
            if (
                q[f"mte_{ACC_MTE_FIELD}"]
                is None
                # or 'unknown' in q['abstain_multi_trace_entailment_prediction'].lower()
            )
        }
        examples_to_answer = [
            e for e in examples if dataset.parse_example(e).qid in abstain_ids
        ]
        if len(examples_to_answer) == 0:
            break

    # aggregate after retries loop
    unanswered_examples = [
        q for q in questions_with_entailment if q[f"mte_{ACC_MTE_FIELD}"] is None
    ]
    all_examples = examples_with_answers + unanswered_examples
    _report_results(suffix=f"_{experiment_name}_final", examples=all_examples)

    # save results
    if output_dir is not None:
        output_path = f"{output_dir}/{experiment_unique_name}_final.csv"
        logger.info(f"Saving output path to: {output_path}")
        _save_examples(all_examples, output_path)


if __name__ == "__main__":
    """ """
    args = parse_args()
    run_experiment(args.config_path)
