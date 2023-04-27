class GptAccessor:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls()

    def call_gpt(
        self, prompt: str, stop: str, temperature: float, *args, **kwargs
    ) -> str:
        raise NotImplementedError("Please Implement this method")
