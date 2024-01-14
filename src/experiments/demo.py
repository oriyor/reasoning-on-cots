import dataclasses
from typing import Dict

from src.common.config import Config
from src.dataclasses import QuestionV1
from src.experiments.e2e.run import (
    _set_entailment_input,
    _call_gpt_for_entailment_with_batching,
)
from src.gpt3_accessors.gpt_accessor_factory import GptAccessorFactory
from src.pred_evaluators.evaluators_factory import EvaluatorsFactory
from src.prompting.prompt_factory import PromptFactoryDict


def run_question(
    question_text: str,
    dataset: str,
    answer: str,
    model: str = "code-davinci-002",
    num_decomps: int = 3,
) -> Dict:
    """
    runs the question, first by populating decomps and then by running mcr
    """

    # load config
    Config().load(f"src/config/{dataset}/config_with_retrieval_contexts_first.json")

    # set up object
    question = QuestionV1(
        question=question_text,
        prompt=PromptFactoryDict[f"{dataset}_decomposition"],
        gpt3_accessor=GptAccessorFactory().get_instance(
            "gpt_accessor_with_retrieval_context_first"
        ),
        model=model,
        num_decompositions=num_decomps,
    )
    question.populate()

    # set mcr input
    question_with_mcr = _set_entailment_input(
        {"question": dataclasses.asdict(question), "metadata_gold_answer": answer},
        PromptFactoryDict[f"{dataset}_mcr"],
        entailment_values={
            "shuffle_context": False,
            "use_ir_contexts": False,
            "use_qa_pairs": True,
            "question_prompt_prefix": "",
            "stop_condition": "#",
            "model": model,
        },
        sa_contexts_first=True,
        prefix=f"mcr",
    )

    print("\n====================== Running meta-reasoner ======================")
    res = _call_gpt_for_entailment_with_batching(
        [question_with_mcr],
        EvaluatorsFactory().get_instance("bamboogle"),
        entailment_values={
            "shuffle_context": False,
            "use_ir_contexts": False,
            "use_qa_pairs": True,
            "question_prompt_prefix": "",
            "stop_condition": "#",
            "model": model,
        },
        prefix=f"mcr",
    )[0]
    print(f"F1: {res['mcr_acc@mte']}")


#
# dataset = "strategyqa"  # 2wikihop/strategyqa
# question_text = "Did Brad Peyton need to know about seismology?"
# answer = "yes"  # gold answer
#
# run_question(
#     question_text=question_text,
#     dataset=dataset,
#     answer=answer,
#     model="code-davinci-002",
# )
