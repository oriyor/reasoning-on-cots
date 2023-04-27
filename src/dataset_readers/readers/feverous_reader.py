from typing import Dict

from src.common import dataset_utils
from src.dataclasses import Example
from src.dataset_readers.readers.dataset_reader import DatasetReader

PROMPT_CLAIMS = [
    {
        "id": 1,
        "label": "Yes",
        "claim": "Albert Foday, an attacking midfielder and free kick expert (a method of restarting play after an infringement of the laws by the opponent) plays on Kallon FC, which team he played on in 2002-2003 before going to the Mighty Barolle for two years before his return.",
    },
    {
        "id": 2,
        "label": "Yes",
        "claim": "Shattered Angels (a Japanese Manga) had five Absolute Angels, one of which was ClaÃ\xadomh Solais.",
    },
    {
        "id": 3,
        "label": "No",
        "claim": "KLLB was a radio station owned by Ford Motor Corporation and licensed in West Jordan, Utah until 2017.",
    },
    {
        "id": 4,
        "label": "Yes",
        "claim": "Mikro globulus belongs to Kingdom: Animalia, Phylum: Gastropoda, Class: Mollusca, and Subclass: Vetigastropoda.",
    },
    {
        "id": 5,
        "label": "No",
        "claim": "Valeri Karpin played for CSKA Moscow in the 1986 Soviet Second League season.",
    },
    {
        "id": 6,
        "label": "Yes",
        "claim": "2016 BBC Sports Personality of the Year Award was won by Andy Murray of Tennis (who ranked world No. 1 by the Association of Tennis Professionals (ATP) for 41 weeks, and finished as the year-end No. 1 in 2016), garnering 33.1% of the votes ahead of other sports personalities such as Alistair Brownlee, Nick Skelton, and Mo Farah.",
    },
    {
        "id": 7,
        "label": "No",
        "claim": "Ecstasea is a 585 tonnes yacht built in the Cayman Islands, an autonomous British Overseas Territory in the western Red Sea.",
    },
    {
        "id": 8,
        "label": "Yes",
        "claim": "The DOHC Genesis engine has five valves per cylinder as Yamaha adopted the 5-valve concept because it allowed both excellent volumetric efficiency and high rpm.",
    },
    {
        "id": 9,
        "label": "No",
        "claim": "Two episodes of Das unsichtbare Visier are Das Nest im Urwald, which is 89 minutes long, and Depot im Skagerrak, which is 117 minutes long.",
    },
    {
        "id": 10,
        "label": "No",
        "claim": "Robert Craig Kent, born on November 28, 1828 in Wythe County, Virginia, was the 16th Lieutenant Governor of Virginia.",
    },
]


class FeverousDataReader(DatasetReader):
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def __init__(
        self,
        dataset_path="../../../data/full_datasets/feverous/feverous_dev_challenges.jsonl",
    ):
        super().__init__(dataset_path=dataset_path)
        self.examples = None

    def read(self, rand_sample=None):
        self.examples = dataset_utils.load_jsonl(self.dataset_path)
        # self.examples = PROMPT_CLAIMS  # todo: delete

    def get_examples(self):
        return self.examples

    def parse_example(self, example: Dict) -> Example:
        claim_to_question = f"Is it true that {example['claim']}?".replace(".?", "?")
        gold_answer = "Yes" if example["label"] == "SUPPORTS" else "No"
        return Example(
            qid=example["id"],
            question=claim_to_question,
            gold_answer=gold_answer,
            prev_model_answer=None,
            metadata=example,
        )


#
# reader = FeverousDataReader()
# reader.read()
# for ex in reader.get_examples()[:10]:
#     x = reader.parse_example(ex)
#     print(x)
#     print("*"*20)
# print(len(reader.get_examples()))
