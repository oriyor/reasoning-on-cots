import ast
from typing import Dict

import pandas as pd
from src.dataclasses import Example
from src.dataset_readers.readers.dataset_reader import DatasetReader


class NQReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(
        self,
        dataset_path="data/test_datasets/nq/nq-dev.qa.csv",
    ):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.examples = (
            pd.read_csv(self.dataset_path, sep="\t").fillna("").to_dict("records")
        )
        # ttt = pd.read_csv("data/retrieval_robustness/datasets/nq_v1.csv").to_dict("rows")
        # ttt_set = {z['question'] for z in ttt}
        # self.examples = [x for x in self.examples if x['question'] not in ttt_set]

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        return Example(
            qid=[i for i, x in enumerate(self.examples) if x == example][0],
            question=example["question"],
            gold_answer=ast.literal_eval(example["answer"]),
            prev_model_answer=None,
            metadata=example,
        )
