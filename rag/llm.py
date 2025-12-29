from transformers import pipeline

class HFLLM:
    def __init__(self, model_name="google/flan-t5-base"):
        self.generator = pipeline(
            "text2text-generation",
            model=model_name,
            max_length=512
        )

    def generate(self, prompt):
        result = self.generator(prompt)
        return result[0]["generated_text"]
