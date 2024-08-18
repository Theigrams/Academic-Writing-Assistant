import os
import re

from litellm import completion


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


def rewrite_text(text, service_type, model, full_prompt):
    prompts = load_prompts()

    if service_type not in prompts:
        return text, "服务类型不匹配,返回原始文本", ""

    response = completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "您是一位受人尊敬的学术编辑和语言学家，在各个学科领域都有丰富的学术写作增强经验。您的专长包括改进学术语言、完善语法、确保符合特定领域的惯例，以及在保持学术语气和细微差别的同时进行语言间的翻译。",
            },
            {"role": "user", "content": full_prompt},
        ],
        max_tokens=4000,
    )

    full_response = response.choices[0].message.content.strip()

    output_match = re.search(r"<output>(.*?)</output>", full_response, re.DOTALL)
    explanation_match = re.search(r"<explanation>(.*?)(?:</explanation>|$)", full_response, re.DOTALL)

    output = remove_xml_tags(output_match.group(1).strip()) if output_match else "未提供输出"
    explanation = remove_xml_tags(explanation_match.group(1).strip()) if explanation_match else "未提供解释"

    return output, explanation, full_response
