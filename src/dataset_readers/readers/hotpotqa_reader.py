from typing import Dict

from src.common import dataset_utils
from src.dataclasses import Example
from src.dataset_readers.readers.dataset_reader import DatasetReader


class HotpotQADataReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(
        self,
        dataset_path="../../../data/full_datasets/hotpotqa/hotpot_dev_fullwiki_v1.json",
    ):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.examples = dataset_utils.load_json(self.dataset_path)

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        return Example(
            qid=example["_id"],
            question=example["question"],
            gold_answer=example["answer"],
            prev_model_answer=None,
            metadata=example,
        )


# reader = HotpotQADataReader()
# reader.read()
# for ex in reader.get_examples()[:10]:
#     x = reader.parse_example(ex)
#     print(x)
#     print("*"*20)
# print(len(reader.get_examples()))
