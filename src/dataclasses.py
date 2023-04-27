from enum import Enum
from typing import List, Dict
from dataclasses import dataclass
from src.common.config import Config
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.consts import (
    POSITIVE_PREFIX,
    NEGATIVE_PREFIX,
    INTERMEDIATE_ANS_PREFIX,
    KNOWLEDGE_FOLLOW_UP_PREFIX,
    REASONING_FOLLOW_UP_PREFIX,
    FINAL_ANSWER_PREFIX,
    FOLLOW_UP_PREFIX,
    CONTEXT_PREFIX,
    CONTEXT_ANSWER_SEP,
    NUMBERED_CONTEXT_PREFIX,
)


# Todo: TW - Commented out because of DeBerta in background
# from src.entailment.entailment import run_entailment


@dataclass
class Example:
    qid: str
    question: str
    gold_answer: str
    prev_model_answer: str
    metadata: Dict


@dataclass
class BreakDecomposition:
    decomposition: str
    intermediate_questions: List[str]
    intermediate_answers: List[str]
    final_answer: str
    intermediate_contexts: List[str]


@dataclass
class IntermediateQuestionWithAnswer:
    """
    an intermediate decompotision in the tree
    """

    intermediate_question: str
    answer: Dict = None  # from gpt-3


@dataclass
class Question:
    """
    a question object
    """

    question: str  # question
    decompositions: List[str]  # decompositions from gpt
    intermediate_questions_with_answers: List[
        IntermediateQuestionWithAnswer
    ] = None  # intermediate steps with their answers


@dataclass
class EntailmentResult:
    entailment: float
    neutral: float
    contradiction: float


@dataclass
class EntailmentResultWithInput:
    premise: str
    hypothesis: str
    entailment_result: EntailmentResult


@dataclass
class DecompositionStepV1:
    question: str
    answer: str
    google_answer: str
    google_answer_long: Dict
    entailment_result_with_input: EntailmentResultWithInput
    gpt_3_ans: str


@dataclass
class TraceResult:
    positive: EntailmentResultWithInput
    negative: EntailmentResultWithInput


@dataclass
class StatementResult:
    original_statement: str
    positive: str
    negative: str


def format_ir_decomposition(
    decomposition: str, entail_facts=False, contexts_first=None
) -> List[DecompositionStepV1]:
    """format decomposition and store retrieved context(s) for each step"""
    if contexts_first is True:
        # decomposition is in SA format where contexts are appended at beginning: 'Context1:...Context2:...'
        for i in range(1, 5):
            decomposition = decomposition.replace(f"Context{i}:\n\n", f"Context{i}: ")
    decomposition_steps = []
    lines = decomposition.split("\n")
    question, answer, gpt_3_ans = None, None, None
    context = None
    context_counter = 1 if Config().get("decomposition.retrieve_orig_question") else 0
    all_contexts = []
    for line in lines:
        line = (
            line + "  "
        )  # add " " to avoid discarding traces when the answer is empty
        if line.startswith(NUMBERED_CONTEXT_PREFIX):
            if contexts_first is True:
                context = ": ".join(
                    line.split(NUMBERED_CONTEXT_PREFIX)[1].split(":")[1:]
                ).strip()
            else:
                context = line.split(CONTEXT_PREFIX)[1].strip()
            all_contexts += [context]
        if line.startswith(FOLLOW_UP_PREFIX):
            question = line.split(FOLLOW_UP_PREFIX)[1].strip()
        if line.startswith(FINAL_ANSWER_PREFIX):
            decomposition_steps.append(
                DecompositionStepV1(
                    question=None,
                    answer=None,
                    google_answer=None,
                    google_answer_long=None,
                    entailment_result_with_input=None,
                    gpt_3_ans=line.split(FINAL_ANSWER_PREFIX)[1].strip(),
                )
            )
        if line.startswith(INTERMEDIATE_ANS_PREFIX) and question is not None:
            answer = line.split(INTERMEDIATE_ANS_PREFIX)[1].strip()
            answer = "" if answer is None else answer
            context = "" if context is None else context
            if contexts_first is True and context_counter < len(all_contexts):
                # for contexts first, we need to align preceding contexts with intermediate Qs
                context = all_contexts[context_counter]
                context_counter += 1
            context_and_answer = context + CONTEXT_ANSWER_SEP + answer

            decomposition_steps.append(
                DecompositionStepV1(
                    question=question,
                    answer=context_and_answer,
                    google_answer=None,
                    google_answer_long=None,
                    entailment_result_with_input=None,
                    gpt_3_ans=None,
                )
            )
            question, answer = None, None
    return decomposition_steps


def format_statement(statement: str) -> StatementResult:
    """ """
    positive, negative = None, None
    lines = statement.split("\n")
    for line in lines:
        if line.startswith(POSITIVE_PREFIX):
            positive = line.split(POSITIVE_PREFIX)[1]
        if line.startswith(NEGATIVE_PREFIX):
            negative = line.split(NEGATIVE_PREFIX)[1]
    return StatementResult(
        original_statement=statement, positive=positive, negative=negative
    )


def format_decompsition_break(
    decomposition: BreakDecomposition,
) -> List[DecompositionStepV1]:
    decomposition_steps = []
    for i in range(len(decomposition.intermediate_questions)):
        decomposition_steps.append(
            DecompositionStepV1(
                question=decomposition.intermediate_questions[i],
                answer=decomposition.intermediate_answers[i + 1],
                google_answer=None,
                google_answer_long=None,
                entailment_result_with_input=None,
                gpt_3_ans=None,
            )
        )
    decomposition_steps.append(
        DecompositionStepV1(
            question=None,
            answer=None,
            google_answer=None,
            google_answer_long=None,
            entailment_result_with_input=None,
            gpt_3_ans=decomposition.final_answer,
        )
    )
    return decomposition_steps


def format_decompsition_string(
    decomposition: str, entail_facts=False
) -> List[DecompositionStepV1]:
    """ """
    decomposition_steps = []
    lines = decomposition.split("\n")
    question, answer, gpt_3_ans = None, None, None
    for line in lines:
        if line.startswith(KNOWLEDGE_FOLLOW_UP_PREFIX):
            question = line.split(KNOWLEDGE_FOLLOW_UP_PREFIX)[1]
        elif line.startswith(REASONING_FOLLOW_UP_PREFIX):
            question = line.split(REASONING_FOLLOW_UP_PREFIX)[1]
        elif line.startswith(FOLLOW_UP_PREFIX):
            question = line.split(FOLLOW_UP_PREFIX)[1]
        if line.startswith(FINAL_ANSWER_PREFIX):
            decomposition_steps.append(
                DecompositionStepV1(
                    question=None,
                    answer=None,
                    google_answer=None,
                    google_answer_long=None,
                    entailment_result_with_input=None,
                    gpt_3_ans=line.split(FINAL_ANSWER_PREFIX)[1],
                )
            )
        if line.startswith(INTERMEDIATE_ANS_PREFIX) and question is not None:
            answer = line.split(INTERMEDIATE_ANS_PREFIX)[1]

            # calc answer
            gooogle_ans_short, entailment_result_with_input, google_ans_long = (
                None,
                None,
                None,
            )
            # Todo: TW - Commented out because of DeBerta in background
            # if entail_facts:
            #     gooogle_ans_short, google_ans_long = google(question)
            #     premise = question + " " + gooogle_ans_short
            #     hypothesis = question + " " + answer
            #     entailment = run_entailment(premise, hypothesis)
            #     entailment_result_with_input = EntailmentResultWithInput(
            #         premise=premise, hypothesis=hypothesis, entailment_result=entailment
            #     )
            decomposition_steps.append(
                DecompositionStepV1(
                    question=question,
                    answer=answer,
                    google_answer=gooogle_ans_short,
                    google_answer_long=google_ans_long,
                    entailment_result_with_input=entailment_result_with_input,
                    gpt_3_ans=None,
                )
            )
            question, answer = None, None
    return decomposition_steps


def linearize_decompositions(decompositions: List[DecompositionStepV1]) -> str:
    """ """
    res = ""
    valid_decompositions = [d for d in decompositions if d.question]
    for decomp in valid_decompositions:
        res += decomp.question + " " + decomp.answer + "\n"
    print(res)
    return res


def linearize_decompositions_google(decompositions: List[DecompositionStepV1]) -> str:
    """ """
    res = ""
    valid_decompositions = [d for d in decompositions if d.question]
    for decomp in valid_decompositions:
        if decomp.google_answer is not None:
            res += decomp.question + " " + decomp.google_answer + "\n"
    print(res)
    return res


@dataclass
class QuestionV1:
    """
    a question object
    """

    question: str  # original question
    statement: StatementResult  # the parsed statement after calling gpt-3
    decompositions: List[str]  # decompositions from gpt-3 self-ask
    decompsition_steps: List[List[DecompositionStepV1]]  # reasoning traces
    traces_entailments: List[List[TraceResult]]

    def __init__(
        self,
        question: str,
        prompt: str,
        gpt3_accessor: GptAccessor,
        model: str,
        num_decompositions: int = 5,
    ):
        self.question = question
        self.send_question_separately = Config().get(
            "decomposition.send_question_separately"
        )
        self.gpt_accessor_indices_with_temperature_0 = Config().get(
            "decomposition.gpt_accessor_indices_with_temperature_0"
        )
        self.model = model
        self.curr_prompt = (
            prompt if self.send_question_separately else prompt + self.question
        )
        self.num_decompositions = num_decompositions
        self.gpt3_accessor = gpt3_accessor
        self.statement = None
        self.decompositions = None
        self.decompsition_steps = None
        self.traces_entailments = None
        self.traces_entailments_google = None

    # Todo: TW - Commented out because of DeBerta in background
    # def _get_entailment_res(
    #     self, decomposition_linearized: str, statement: str
    # ) -> EntailmentResultWithInput:
    #     entailment = run_entailment(
    #         premise=decomposition_linearized, hypothesis=statement
    #     )
    #     entailment_result_with_input = EntailmentResultWithInput(
    #         premise=decomposition_linearized,
    #         hypothesis=statement,
    #         entailment_result=entailment,
    #     )
    #     return entailment_result_with_input

    def populate_statement(self):
        # gpt_statement_res = call_gpt_statement_generatior(
        #     statement_generation_prompt + self.question, ""
        # )
        gpt_statement_res = ""
        self.statement = format_statement(gpt_statement_res)

    def populate_decompositions(self):
        def get_temp_at_index(index: int) -> float:
            # check if the index should get temp 0
            if (
                self.gpt_accessor_indices_with_temperature_0 is not None
                and index in self.gpt_accessor_indices_with_temperature_0
            ):
                return 0
            return Config().get("decomposition.gpt3_accessor_temperature")

        print("\nRunning decomposition + retrieval models")
        self.decompositions = [
            self.gpt3_accessor.call_gpt(
                self.curr_prompt, "", get_temp_at_index(i), self.model, i
            )
            if not self.send_question_separately
            else self.gpt3_accessor.call_gpt(
                self.curr_prompt, "", get_temp_at_index(i), self.question, self.model, i
            )
            for i in range(self.num_decompositions)
        ]

    def populate_decomposition_steps(self):
        # print("\npopulating_decompositions_steps")
        self.decompsition_steps = [
            format_decompsition_break(decomposition)
            if type(decomposition) == BreakDecomposition
            else format_decompsition_string(decomposition)
            for decomposition in self.decompositions
        ]

    def populate_trace_entailments(self):
        print("\npopulate_trace_entailments")
        trace_results = [
            [
                TraceResult(
                    positive=self._get_entailment_res(
                        linearize_decompositions(decompsition[: i + 1]),
                        self.statement.positive,
                    ),
                    negative=self._get_entailment_res(
                        linearize_decompositions(decompsition[: i + 1]),
                        self.statement.negative,
                    ),
                )
                for i in range(len(decompsition))
            ]
            for decompsition in self.decompsition_steps
        ]
        self.traces_entailments = trace_results

        print("\npopulate_trace_entailments_google")
        self.traces_entailments_google = []

    def populate(self):
        """ """
        self.populate_statement()
        self.populate_decompositions()
        self.populate_decomposition_steps()
        # Todo: TW - Commented out because of DeBerta in background
        # self.populate_trace_entailments()


class Answer(str, Enum):
    Yes = "YES"
    No = "NO"
    MaybeYes = "MaybeYes"
    MaybeNo = "MaybeNo"
    Donno = "Donno"


@dataclass
class QuestionWithAnswer:
    question: QuestionV1
    answers: Dict[str, Answer]
    gpt_answers: List[str]
