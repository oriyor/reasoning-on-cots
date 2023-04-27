from typing import Dict

from src.prompting.prompts_to_keep import (
    wikihop_decompositions_with_retrieval_context_first,
    wikihop_entailment,
    strategyqa_decomposition,
    strategy_mcr,
)

PromptFactoryDict: Dict[str, str] = {
    "2wikihop_decomposition": wikihop_decompositions_with_retrieval_context_first,
    "2wikihop_mcr": wikihop_entailment,
    "strategyqa_decomposition": strategyqa_decomposition,
    "strategyqa_mcr": strategy_mcr,
}
