import os

import streamlit as st
import yaml

from rewriter import load_prompts, rewrite_text
from utils import generate_word_diff, set_page_style


def load_api_config():
    with open("api.yaml", "r") as file:
        return yaml.safe_load(file)


def main():
    set_page_style()
    st.title("Academic Writing Assistant")

    api_cfg = load_api_config()
    prompts = load_prompts()

    # 默认选择 gpt-4o-mini 和 academic_rewriting
    model_list = list(api_cfg.keys())
    service_type_list = list(prompts.keys())

    default_model_index = model_list.index("gpt-4o-mini")
    default_service_type_index = (
        service_type_list.index("academic_rewriting") if "academic_rewriting" in service_type_list else 0
    )

    model = st.selectbox("请选择要使用的模型:", model_list, index=default_model_index)
    service_type = st.selectbox("请选择服务类型:", service_type_list, index=default_service_type_index)

    default_text = "The Knuth-Morris-Pratt string searching algorithm is way faster than brute force. It uses a prefix function to skip ahead when a mismatch is found, instead of starting over from the next character in the text. This makes it run in O(n+m) time instead of O(n*m) time, which is a huge improvement when searching through large strings."

    if "translation" in service_type:
        default_text = "人工智能技术正在迅速发展,并在各个领域得到广泛应用。它不仅能提高生产效率,还能帮助我们解决复杂的问题。然而,我们也需要警惕人工智能可能带来的伦理和隐私问题,确保其发展方向符合人类的长远利益。"

    text = st.text_area("请输入您的文本:", value=default_text, height=200)
    debug_mode = st.checkbox("调试模式")

    if st.button("提交") and text:
        try:
            os.environ["OPENAI_API_KEY"] = api_cfg[model]["api_key"]
            os.environ["OPENAI_API_BASE"] = api_cfg[model]["api_base"]

            prompt = prompts[service_type]
            rewritten_text, explanation, full_response = rewrite_text(text, prompt, model)

            display_results(text, rewritten_text, explanation, full_response, prompt, debug_mode)
        except Exception as e:
            st.error(f"处理过程中出现错误: {str(e)}")
    elif not text:
        st.warning("请输入文本后再提交。")


def display_results(original_text, rewritten_text, explanation, full_response, prompt, debug_mode):
    word_diff = generate_word_diff(original_text, rewritten_text)

    st.subheader("优化结果对比:")
    st.markdown(f'<div class="diff-result">{word_diff}</div>', unsafe_allow_html=True)

    st.subheader("优化后的文本:")
    st.code(rewritten_text, language="markdown")

    st.subheader("修改说明:")
    st.write(explanation)

    if debug_mode:
        st.subheader("Output (调试模式):")
        st.code(full_response, language="markdown")

        st.subheader("Prompt (调试模式):")
        st.code(prompt, language="markdown")


if __name__ == "__main__":
    main()
