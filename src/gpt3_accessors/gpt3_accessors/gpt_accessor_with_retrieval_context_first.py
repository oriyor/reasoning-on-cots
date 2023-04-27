import time

import openai
import os

from src.common.config import Config
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.opeanai.utils import greenify, change_openaikey_and_sleep, gpt_simple_generator
from src.serpapi.serpapi import (
    google,
    get_question_wiki_snippet,
    get_question_google_snippet,
)
import re

openai.api_key = os.getenv(
    "OPENAI_KEY"
)  # get one from https://openai.com , first few requests are free!


FOLLOW_UP_REGEX_PATTERN = r"Follow up:.*\n"


class GptAccessorWithRetrievalContextFirst(GptAccessor):
    def call_gpt(
        self, orig_prompt, stop, temperature, orig_question, model, decomposition_index
    ):
        print(
            f"\n====================== Decomposition {decomposition_index} ======================"
        )
        contexts = (
            [get_question_wiki_snippet(orig_question, cache=True)]
            if Config().get("decomposition.retrieve_orig_question")
            else []
        )
        stop_condition = "Intermediate answer:"
        res = ""
        retries = 6
        # iterate decomposition for 5 steps
        for i in range(5):
            # format input, the input should be:
            # contexts, followed by intermediate QAs
            context_formatted = "\n".join(
                [f"Context{k+1}: {context}" for k, context in enumerate(contexts)]
            )
            context_formatted = (
                "\n" + context_formatted
                if len(context_formatted)
                else context_formatted
            )
            cur_prompt = (
                orig_prompt
                + context_formatted
                + "\nQuestion: "
                + orig_question
                + "\nAre follow up questions needed here: Yes."
                + res
            )

            # get gpt ans with retries
            for i in range(retries):
                try:
                    ans = openai.Completion.create(
                        model=model,
                        max_tokens=512,
                        stop=["Context:", "#"],
                        prompt=cur_prompt,
                        temperature=temperature,
                    )
                    break
                except Exception as e:
                    print(f"exception thrown, sleeping...")
                    print(e)
                    change_openaikey_and_sleep()

            # add context
            returned = ans["choices"][0]["text"]

            # check the stop condition, it's different if we generate the first follow up or if we are in an intermediate step
            # if this is the first follow up, break on the first intermediate question
            if stop_condition == "Intermediate answer:":
                # add the follow-up question to the prompt and change the stop condition
                res += returned.split("Intermediate answer:")[0]
                stop_condition = "Follow up:"

            # else, we are in an intermediate step
            elif stop_condition == "Follow up:":
                # continue until we find the next follow up question
                # since we want to add retrieved contexts given this question
                followup_split = re.split(FOLLOW_UP_REGEX_PATTERN, returned)

                # add everything until the next follow up
                res += followup_split[0]

                # add the next follow up
                if len(followup_split) > 1:
                    res += re.findall(FOLLOW_UP_REGEX_PATTERN, returned)[0]

            # make sure the result does not end in a new line
            if res[-1] == "\n":
                res = res[:-1]

            # if we are in an intermediate step, add the retrieved context to the list of contexts
            if "Follow up: " in returned:
                # get the first follow up
                question = [l for l in returned.split("\n") if "Follow up: " in l][
                    0
                ].split("Follow up: ")[-1]
                retrieval = get_question_wiki_snippet(question, cache=True)
                contexts.append(retrieval)

            # end when the final answer is generated, this means that no follow up questions were asked
            elif "So the final answer is: " in returned:
                final_res = (
                    context_formatted
                    + "\nQuestion: "
                    + orig_question
                    + "\nAre follow up questions needed here: Yes."
                    + res
                )
                print(f"\nDecomposition {decomposition_index} result:")
                print(greenify(final_res), end="")

                # return the contexts followed by the original question, intermediate QAs and final answer
                return final_res
            print(greenify(res), end="")
            print("\n")

        return res
