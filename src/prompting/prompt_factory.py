from typing import Dict

from src.prompting.prompts_to_keep import (
    wikihop_decompositions_with_retrieval_context_first,
    wikihop_entailment,
    strategyqa_decomposition,
    strategy_mcr,
)
from src.prompting.retrobust import nq_with_retrieval_at1, nq_with_retrieval_at10, nq_with_retrieval_mix, \
    nq_no_retrieval

PromptFactoryDict: Dict[str, str] = {
    "2wikihop_decomposition": wikihop_decompositions_with_retrieval_context_first,
    "2wikihop_mcr": wikihop_entailment,
    "strategyqa_decomposition": strategyqa_decomposition,
    "strategyqa_mcr": strategy_mcr,
    "question_prefix": "Question: ",
    "nq_with_retrieval_at1": nq_with_retrieval_at1,
    "nq_with_retrieval_at10": nq_with_retrieval_at10,
    "nq_with_retrieval_mix": nq_with_retrieval_mix,
    "nq_no_retrieval": nq_no_retrieval
}
