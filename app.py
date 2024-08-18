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
    st.title("学术论文GPT")

    api_cfg = load_api_config()
    prompts = load_prompts()

    model = st.selectbox("请选择要使用的模型:", list(api_cfg.keys()))
    service_type = st.selectbox("请选择服务类型:", list(prompts.keys()))

    default_text = "The Knuth-Morris-Pratt string searching algorithm is way faster than brute force. It uses a prefix function to skip ahead when a mismatch is found, instead of starting over from the next character in the text. This makes it run in O(n+m) time instead of O(n*m) time, which is a huge improvement when searching through large strings."
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
        st.subheader("完整Output (调试模式):")
        st.code(full_response, language="markdown")

        st.subheader("完整Prompt (调试模式):")
        st.code(prompt, language="markdown")


if __name__ == "__main__":
    main()