from typing import List, Dict

from src.common import dataset_utils
from src.dataclasses import Example
from src.info_seeking_questions.dataset_reader import DatasetReader


class QuartzDataReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(
        self, dataset_path="data/test_datasets/quartz-dataset-v1-aug2019/dev.jsonl"
    ):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.examples = dataset_utils.load_jsonl(self.dataset_path)

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        def _format_choices(choices: List[Dict[str, str]]) -> str:
            return " ".join(
                [
                    f'{choice["label"]}. {choice["text"]}'
                    for choice in example["question"]["choices"]
                ]
            )

        return Example(
            qid=example["id"],
            question=example["question"]["stem"]
            + " "
            + _format_choices(example["question"]["choices"]),
            gold_answer=example["answerKey"],
            prev_model_answer=None,
            metadata=example,
        )
