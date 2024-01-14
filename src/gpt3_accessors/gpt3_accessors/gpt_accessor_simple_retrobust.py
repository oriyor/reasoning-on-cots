import time

import openai
import os

from src.common.config import Config
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.inference.wrappers.fastchat import FastChatWrapper
from src.inference.wrappers.openai import OpenAIWrapper
from src.opeanai.utils import greenify

openai.api_key = os.getenv(
    "OPENAI_KEY"
)  # get one from https://openai.com , first few requests are free!


class GptAccessorSimpleRetrobust(GptAccessor):
    def call_gpt(self, cur_prompt, stop, temperature):
        inference_wrapper = (
            FastChatWrapper()
            if Config().get("decomposition.llm_wrapper") == "fastchat"
            else OpenAIWrapper()
        )
        follow_ups = "No." if Config().get("dataset.name") == "nq" else "Yes."
        retries = 3
        # get gpt ans with retries
        for i in range(retries):
            try:
                ans = inference_wrapper.complete(
                    model="code-davinci-002",
                    max_tokens=512,
                    stop="#",
                    prompt=cur_prompt + "\nAre follow up questions needed here: " + follow_ups,
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
