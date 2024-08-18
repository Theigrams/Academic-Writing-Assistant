from litellm import completion


def rewrite_text(text, service_type, model):
    # Set different prompts based on service type
    if service_type == "Academic Style Rewriting":
        prompt = f"Please rewrite the following text in a more academic style while maintaining the original meaning:\n\n{text}\n\nRewritten text:"
    elif service_type == "Grammar Correction":
        prompt = f"Please correct any grammatical errors in the following text while maintaining the original meaning:\n\n{text}\n\nCorrected text:"
    elif service_type == "Chinese to English Translation":
        prompt = f"Please translate the following Chinese text into English:\n\n{text}\n\nEnglish translation:"
    else:
        return text  # If service type doesn't match, return original text

    # Call LLM for text processing
    response = completion(
        model=model,  # Use the model selected by the user
        messages=[
            {
                "role": "system",
                "content": "You are a professional academic editor skilled in improving the language and grammar of academic articles.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,  # Adjust as needed
    )

    # Return the processed text
    return response.choices[0].message.content.strip()
