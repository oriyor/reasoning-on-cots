import time

import openai
import os

from src.common.config import Config
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.opeanai.utils import greenify
from src.serpapi.serpapi import (
    google,
    get_question_wiki_snippet,
    get_question_google_snippet,
)

openai.api_key = os.getenv(
    "OPENAI_KEY"
)  # get one from https://openai.com , first few requests are free!


class GptAccessorWithRetrieval(GptAccessor):
    def call_gpt(self, cur_prompt, stop, temperature):
        res = ""
        retries = 3
        # iterate decomposition for 5 steps
        for i in range(5):
            # get gpt ans with retries
            for i in range(retries):
                try:
                    ans = openai.Completion.create(
                        model="code-davinci-002",
                        max_tokens=512,
                        stop=["Context:", "#"],
                        prompt=cur_prompt,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print("exception thrown, sleeping...", e)
                    time.sleep(60)
                    print("finished sleeping")

            # add context
            returned = ans["choices"][0]["text"]
            res += returned
            cur_prompt += returned
            if "Follow up: " in returned:
                question = returned.split("Follow up: ")[-1].replace("\n", "")
                retrieval = get_question_wiki_snippet(question, cache=True)
                cur_prompt += f"Context: {retrieval}\n"
                res += f"Context: {retrieval}\n"
            if "So the final answer is: " in returned:
                print(greenify(res), end="")
                return res
            print(greenify(res), end="")

        return res
