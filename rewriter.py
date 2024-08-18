import os
import re
from functools import lru_cache

from litellm import completion


@lru_cache(maxsize=1)
def load_prompts():
    prompts = {}
    prompts_dir = "prompts"
    for filename in os.listdir(prompts_dir):
        if filename.endswith(".md"):
            service_type = filename[:-3]  # 移除 .md 扩展名
            with open(os.path.join(prompts_dir, filename), "r", encoding="utf-8") as file:
                prompts[service_type] = file.read()
    return prompts


def remove_xml_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def rewrite_text(text, prompt, model):
    response = completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": text},
        ],
        max_tokens=4000,
    )

    full_response = response.choices[0].message.content.strip()

    output_match = re.search(r"<output>(.*?)</output>", full_response, re.DOTALL)
    explanation_match = re.search(r"<explanation>(.*?)(?:</explanation>|$)", full_response, re.DOTALL)

    output = remove_xml_tags(output_match.group(1).strip()) if output_match else "未提供输出"
    explanation = remove_xml_tags(explanation_match.group(1).strip()) if explanation_match else "未提供解释"

    return output, explanation, full_response
