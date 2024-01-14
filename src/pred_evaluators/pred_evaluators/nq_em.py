import string
from typing import List
import regex as re


class NQEMEvaluator:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    @staticmethod
    def _normalize_answer(s: str) -> str:
        def remove_articles(text):
            return re.sub(r"\b(a|an|the)\b", " ", text)

        def white_space_fix(text):
            return " ".join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return "".join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_articles(remove_punc(lower(s))))

    def _exact_match_score(self, prediction: str, ground_truth: str) -> bool:
        return self._normalize_answer(prediction) == self._normalize_answer(
            ground_truth
        )

    def evaluate(self, pred: str, golds: List[str]) -> float:
        # return 1 if we have an em for the pred with one of the golds otherwies 9
        for gold in golds:
            if self._exact_match_score(pred, gold):
                return 1
        return 0
