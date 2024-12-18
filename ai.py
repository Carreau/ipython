import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use "gpt2-medium", "gpt2-large", etc.
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


def suggest_completion(partial_code):
    """
    Suggests code completions for the given partial Python code.

    Args:
        partial_code (str): The partial Python code to complete.

    Returns:
        str: Suggested code completion.
    """
    # Encode the input code
    inputs = tokenizer.encode(partial_code, return_tensors="pt")

    # Generate code completion
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=len(inputs[0]) + 50,  # Adjust length as needed
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode the generated output
    completion = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Return the completion, trimming the original input
    return completion[len(partial_code) :].strip()


# Example usage
if __name__ == "__main__":
    import rich

    while partial_code := input():
        completion = suggest_completion(partial_code)
        rich.print(f"{partial_code}[gray]{completion}[/gray]")
