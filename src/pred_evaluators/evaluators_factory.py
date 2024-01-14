from typing import Dict, Type

from src.common.abstract_factory import AbstractFactory
from src.pred_evaluators.pred_evaluators.bamboogle_evaluator import BamboogleEvaluator
from src.pred_evaluators.pred_evaluators.base_evaluator import Evaluator
from src.pred_evaluators.pred_evaluators.em_evaluator import EMEvaluator
from src.pred_evaluators.pred_evaluators.hover_evaluator import HoverEvaluator
from src.pred_evaluators.pred_evaluators.fermi_evaluator import FermiEvaluator
from src.pred_evaluators.pred_evaluators.nq_em import NQEMEvaluator
from src.pred_evaluators.pred_evaluators.quartz_em_evaluator import QuartzEMEvaluator
from src.pred_evaluators.pred_evaluators.wikihop_evaluator import WikiHopEvaluator


class EvaluatorsFactory(AbstractFactory):
    """ """

    def get_instance_name_to_class_dict(self) -> Dict[str, Type[Evaluator]]:
        return {
            "em": EMEvaluator,
            "quartz": QuartzEMEvaluator,
            "bamboogle": BamboogleEvaluator,
            "hover": HoverEvaluator,
            "fermi": FermiEvaluator,
            "wikihop": WikiHopEvaluator,
            "nq": NQEMEvaluator,
        }
