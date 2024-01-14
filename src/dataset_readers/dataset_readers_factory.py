from typing import Dict, Type

from src.common.abstract_factory import AbstractFactory
from src.dataset_readers.readers.dataset_reader import DatasetReader
from src.dataset_readers.readers.fermi_reader import FermiReader

# from src.dataset_readers.readers.feverous_reader import FeverousDataReader
# from src.dataset_readers.readers.hotpotqa_reader import HotpotQADataReader
# from src.dataset_readers.readers.hover_reader import HoverDataReader
# from src.dataset_readers.readers.quartz_reader import QuartzDataReader
# from src.dataset_readers.readers.bamboogle_reader import BamboogleDataReader
from src.dataset_readers.readers.nq_reader import NQReader
from src.dataset_readers.readers.strategy_qa import StrategyQADataReader
from src.dataset_readers.readers.wikihop_reader import WikiHopDataReader

# from src.info_seeking_questions.dataset_reader import DatasetReader


class DatasetReadersFactory(AbstractFactory):
    """ """

    def get_instance_name_to_class_dict(self) -> Dict[str, Type[DatasetReader]]:
        return {
            "strategy_qa": StrategyQADataReader,
            # "bamboogle": BamboogleDataReader,
            # "quartz": QuartzDataReader,
            "wikihop": WikiHopDataReader,
            "nq": NQReader,
            # "feverous": FeverousDataReader,
            # "hover": HoverDataReader,
            # "hotpotqa": HotpotQADataReader,
            # "fermi": FermiReader,
        }
