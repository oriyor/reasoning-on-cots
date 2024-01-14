import openai

from src.inference.wrappers.base_inference_wrapper import InferenceWrapper


class OpenAIWrapper(InferenceWrapper):
    def complete(
        self,
        model="code-davinci-002",
        max_tokens=512,
        stop=["Context:", "#"],
        prompt="",
        temperature=0.7,
    ):
        res = openai.Completion.create(
            model=model,
            max_tokens=max_tokens,
            stop=stop,
            prompt=prompt,
            temperature=temperature,
        )
        return res
