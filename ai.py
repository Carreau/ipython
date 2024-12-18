from openai import OpenAI
import os

# Initialize the OpenAI API client

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

import openai

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
openai.api_key = os.environ.get("OPENAI_API_KEY")


HEAD = """```python\n"""

TAIL = "\n```"


def strip_head_and_tail(code):
    if code.startswith(HEAD):
        code = code[len(HEAD) :]
    if code.endswith(TAIL):
        code = code[: -len(TAIL)]
    return code


def complete_python_code_chat(prompt, model="gpt-3.5", max_tokens=150):
    """
    Calls the OpenAI API chat endpoint to complete Python code.

    Args:
        prompt (str): The starting Python code or description to complete.
        model (str): The OpenAI model to use (e.g., gpt-3.5-turbo or gpt-4).
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The completed Python code.
    """
    try:
        # Call the OpenAI chat API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please send me a python code that complete the followinf=g snippet:, only return the code, no other text, not even a comment,or backticks `{prompt}`",
                }
            ],
            model="gpt-4o",
        )
        part = strip_head_and_tail(chat_completion.choices[0].message.content.strip())
        if part.startswith(prompt):
            part = part[len(prompt) :]
        return part
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Example: Prompt to complete Python code
    while code_prompt := input(">>> "):
        completed_code = complete_python_code_chat(code_prompt)

        print(completed_code)
        print("-----")
