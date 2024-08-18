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

    default_text = "We propose a new family of policy gradient methods for reinforcement learning, which alternate between sampling data through interaction with the environment, and optimizing a “surrogate” objective function using stochastic gradient ascent."
    text = st.text_area("请输入您的文本:", value=default_text, height=200)
    debug_mode = st.checkbox("调试模式")

    if st.button("提交") and text:
        try:
            os.environ["OPENAI_API_KEY"] = api_cfg[model]["api_key"]
            os.environ["OPENAI_API_BASE"] = api_cfg[model]["api_base"]

            full_prompt = prompts[service_type].format(text=text)
            rewritten_text, explanation, full_response = rewrite_text(text, service_type, model, full_prompt)

            display_results(text, rewritten_text, explanation, full_response, full_prompt, debug_mode)
        except Exception as e:
            st.error(f"处理过程中出现错误: {str(e)}")
    elif not text:
        st.warning("请输入文本后再提交。")


def display_results(original_text, rewritten_text, explanation, full_response, full_prompt, debug_mode):
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
        st.code(full_prompt, language="markdown")


if __name__ == "__main__":
    main()
