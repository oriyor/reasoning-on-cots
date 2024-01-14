from time import sleep

from src.common.config import Config
from src.common.logger import get_logger
from src.inference.wrappers.base_inference_wrapper import InferenceWrapper
import requests

logger = get_logger()
RE_TRYING = False


class FastChatWrapper(InferenceWrapper):
    def complete(
        self,
        model="vicuna-13b",
        max_tokens=256,
        stop="#",
        prompt="",
        temperature=0.7,
    ):
        RE_TRYING = True
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic bXRlOm10ZWlzbWNy",
        }
        json_data = {
            "model": Config().get("decomposition.fastchat_model")
            if Config().get("decomposition.fastchat_model")
            else "Llama-2-13b-hf",
            "prompt": prompt,
            "max_tokens": 256,
            "stop": stop,
            "temperature": temperature,
        }

        # try 5 times
        for i in range(5):
            try:
                response = requests.post(
                    Config().get("decomposition.fastchat_url") + "/v1/completions",
                    headers=headers,
                    json=json_data,
                    timeout=150,
                )
                if response.status_code == 200:
                    if RE_TRYING or response.json()["choices"][0]["text"].split(
                        "Answer:"
                    )[-1].replace(".", "").replace("\n", "") in {"Yes", "No"}:
                        if RE_TRYING:
                            print(response.json()["choices"][0]["text"])
                        return response.json()
                    else:
                        json_data["prompt"] = (
                            prompt
                            + response.json()["choices"][0]["text"]
                            + "But the most likely answer is:"
                        )
                        RE_TRYING = True
                else:
                    logger.info("got exception from fastchat server, sleeping...")
                    sleep(10)
            except Exception as e:
                logger.info("got exception from fastchat server, sleeping...")
                sleep(10)
        logger.info("failed 5 times to access fastchat server, exiting...")
        response_messsage = response.json()["message"]
        logger.info(response_messsage)
        # return empty message
        return {"choices": [{"text": ""}]}
