from typing import List, Dict

from src.common import dataset_utils
from src.dataclasses import Example
from src.dataset_readers.readers.dataset_reader import DatasetReader
from src.serpapi.serpapi import get_string_hash


class FermiReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(self, dataset_path="data/test_datasets/fermi/train_realfp.json"):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.train_examples = dataset_utils.load_json(self.dataset_path)
        self.dev_examples = dataset_utils.load_json(
            self.dataset_path.replace("train", "val")
        )
        unique_questions, self.examples = set(), []
        for x in self.train_examples + self.dev_examples:
            if x["question"] not in unique_questions:
                unique_questions.add(x["question"])
                self.examples.append(x)

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        def _format_question(example: Dict) -> str:
            # check if the there's a $
            if "$" in example["answer"]:
                return f'{example["question"]} Unit: $.'

            # else check the unit after the space
            unit_split = example["answer"].split(" ")
            if len(unit_split) == 1:
                return example["question"]
            else:
                return f'{example["question"]} Unit: {unit_split[-1]}.'

        return Example(
            qid=get_string_hash(example["question"]),
            question=_format_question(example),
            gold_answer=example["answer"],
            prev_model_answer=None,
            metadata=example,
        )
