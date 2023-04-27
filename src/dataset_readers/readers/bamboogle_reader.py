from typing import Dict

from src.common import dataset_utils
from src.dataclasses import Example
from src.dataset_readers.readers.dataset_reader import DatasetReader


class BamboogleDataReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(
        self,
        dataset_path="data/test_datasets/bamboogle_prerelease_random.csv",
    ):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.examples = dataset_utils.read_csv_to_dict(self.dataset_path)

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        # Manually corrected wrong answers in Bamboogle
        corrected_ans = (
            example["Answer_corrected"]
            if example["Answer_corrected"] != ""
            else example["Answer"]
        )
        return Example(
            qid=[i for i, x in enumerate(self.examples) if x == example][0],
            question=example["Question"],
            gold_answer=corrected_ans,
            prev_model_answer=None,
            metadata=example,
        )
