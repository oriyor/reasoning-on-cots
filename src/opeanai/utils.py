import time

import openai
import os
import datetime
from dotenv import load_dotenv

from openai.error import RateLimitError, InvalidRequestError
import json

from src.common.logger import get_logger
from src.serpapi.serpapi import google, get_question_wiki_snippet

logger = get_logger()

# load openai keys from env, and set a random key at random
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
open_ai_keys = [openai.api_key]
last_time_out_for_keys = {k: datetime.datetime.min for k in open_ai_keys}
sleep_time_per_key = 30
print()


def call_gpt(cur_prompt, stop="\n"):
    """
    call the gpt-3 api
    """
    print("calling gpt")
    ans = openai.Completion.create(
        model="code-davinci-002",
        max_tokens=1,
        stop=stop,
        prompt=cur_prompt,
        temperature=0,
        logprobs=5,
    )
    returned = ans["choices"][0]["text"]

    return ans


def greenify(input):
    return "\x1b[102m" + input + "\x1b[0m"


def yellowfy(input):
    return "\x1b[106m" + input + "\x1b[0m"


#
# def format_question(question: str, show_question=True) -> str:
#     """
#     format a question that wil be presented to gpt-3 validator
#     """
#     # init
#     res = "Provide a yes or no answer to the question given the following facts.\n"
#     intermediate_res = []
#
#     # get a list of facts and intermediate answers
#     question_liines = question.split("\n")
#     facts, intermediate_answers = [], []
#     for line in question_liines:
#         if line.startswith(QUESTION_PREFIX):
#             question = line.split(QUESTION_PREFIX)[1]
#             res += f"{question}\n"
#         if line.startswith(FOLLOW_UP_PREFIX):
#             facts.append(line.split(FOLLOW_UP_PREFIX)[1])
#         if line.startswith(INTERMEDIATE_ANS_PREFIX):
#             intermediate_answers.append(line.split(INTERMEDIATE_ANS_PREFIX)[1])
#
#     for i, (fact, ans) in enumerate(zip(facts, intermediate_answers)):
#         if show_question:
#             res += f"{i + 1}. {fact} {ans}\n"
#             intermediate_res.append(f"{res}Answer:\n")
#         else:
#             res += f"{i + 1}. {ans}\n"
#             intermediate_res.append(f"{res}Answer:\n")
#
#     res += "Answer:\n"
#
#     return intermediate_res
#
#
# def call_gpt3_for_question(curr_question: Question) -> Question:
#     """
#     calls gpt-3 an populates
#     """
#     # create the set of questions
#     intermediate_questions = []
#     for decmop in curr_question.decompositions:
#         question_with_decomp = f"{QUESTION_PREFIX}{curr_question.question}\n{decmop}"
#         intermediate_questions += format_question(question_with_decomp)
#     qusetion_intermediate_questions = set(intermediate_questions)
#     qusetion_intermediate_questions_with_answers = []
#
#     # print
#     for intermediate_question in qusetion_intermediate_questions:
#         gpt_res = call_gpt(intermediate_question[:-1], "\n")
#         gpt3_probs = {
#             k: math.exp(v)
#             for k, v in gpt_res["choices"][0]["logprobs"]["top_logprobs"][0]
#             .to_dict()
#             .items()
#         }
#         yes_probs = sum([v for k, v in gpt3_probs.items() if "yes" in k.lower()])
#         no_probs = sum([v for k, v in gpt3_probs.items() if "no" in k.lower()])
#         probs = {"yes": yes_probs, "no": no_probs, "other": 1 - yes_probs - no_probs}
#         probs = {
#             **probs,
#             **{
#                 "yes_normalized": probs["yes"] / (probs["yes"] + probs["no"]),
#                 "no_normalized": probs["no"] / (probs["yes"] + probs["no"]),
#             },
#         }
#         probs
#         print(probs)
#         qusetion_intermediate_questions_with_answers.append(
#             IntermediateQuestionWithAnswer(
#                 intermediate_question=intermediate_question, answer=probs
#             )
#         )
#
#     # set var
#     curr_question.intermediate_questions_with_answers = (
#         qusetion_intermediate_questions_with_answers
#     )
#     return curr_question


def change_openaikey_and_sleep():
    """
    if we encountered a time-out, change the key and sleep if necessary
    """
    # set the date for current time out
    last_time_out_for_keys[openai.api_key] = datetime.datetime.now()

    # get first time out and calc the time that passed
    first_timed_out_key = min(last_time_out_for_keys, key=last_time_out_for_keys.get)
    time_since_first_time_out = (
        datetime.datetime.now() - last_time_out_for_keys[first_timed_out_key]
    )

    # change the key to be the one that was last timed out
    openai.api_key = first_timed_out_key
    logger.info(f"switched to openaikey: {openai.api_key}")

    # sleep if the time that passed between now and when we last used the key is smaller than a threshold, sleep
    if time_since_first_time_out.seconds < sleep_time_per_key:
        sleeping_time = sleep_time_per_key - time_since_first_time_out.seconds
        print(f"sleeping for {sleeping_time} seconds")
        print(last_time_out_for_keys)
        time.sleep(sleep_time_per_key - time_since_first_time_out.seconds)
        print("finished sleeping")


def gpt_simple_generator(
    prompt, model="code-davinci-002", stop_condition="\n", temperature=0, max_tokens=256
):
    retries = 6
    for i in range(retries):
        try:
            print(f"Using: {openai.api_key}")
            ans = openai.Completion.create(
                model=model,
                max_tokens=max_tokens,
                stop=stop_condition,
                prompt=prompt,
                temperature=temperature,
                # logprobs=5,
            )
            returned = [res["text"] for res in ans["choices"]]

            # if the answer is of size 1, we were prompted with 1 prompt so print it and return
            if len(returned) == 1:
                print(greenify(returned[0]), end="")
                return returned[0], {}

            # else iterate all results and return a list
            else:
                for res in returned:
                    print(greenify(res), end="")
                return returned, {}

        except RateLimitError as e:
            print(f"exception thrown, sleeping...")
            print(e)
            change_openaikey_and_sleep()

        except InvalidRequestError as e:
            print(
                "Invalid request caught, maybe the prompt is too long? Sleeping, plz take a look!"
            )
            time.sleep(30)
            # return "" if type(prompt) == str else ["" for _ in range(len(prompt))], {}

        except Exception as e:
            print(e)
            time.sleep(90)


def call_gpt_self_ask(cur_prompt, stop):
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
                    temperature=0.7,
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
