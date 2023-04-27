import time

import openai
import os

from src.common.config import Config
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.opeanai.utils import greenify

openai.api_key = os.getenv(
    "OPENAI_KEY"
)  # get one from https://openai.com , first few requests are free!


class GptAccessorSimple(GptAccessor):
    def call_gpt(self, cur_prompt, stop, temperature):
        retries = 3
        # get gpt ans with retries
        for i in range(retries):
            try:
                ans = openai.Completion.create(
                    model="code-davinci-002",
                    max_tokens=512,
                    stop="#",
                    prompt=cur_prompt,
                    temperature=temperature,
                )
                break
            except Exception as e:
                print("exception thrown, sleeping...", e)
                time.sleep(30)
                print("finished sleeping")

        # add context
        returned = ans["choices"][0]["text"]
        print(greenify(returned), end="")
        return returned
