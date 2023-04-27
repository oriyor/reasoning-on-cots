from typing import Dict

from src.common import dataset_utils
from src.dataclasses import Example
from src.dataset_readers.readers.dataset_reader import DatasetReader


class StrategyQADataReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(self, dataset_path="../../../data/full_datasets/strategyqa/sqa.csv"):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.examples = dataset_utils.read_csv_to_dict(self.dataset_path)

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        return Example(
            qid=example["qid"],
            question=example["question"],
            gold_answer=example["gold_answer"],
            prev_model_answer=example["model_answer"],
            metadata=example,
        )
