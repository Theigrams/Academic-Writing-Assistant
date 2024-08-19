import os
import time

import streamlit as st
import yaml

from rewriter import delete_prompt, load_prompts, rewrite_text, save_prompt
from utils import generate_word_diff, set_page_config, set_page_style


def load_api_config():
    with open("api.yaml", "r") as file:
        return yaml.safe_load(file)


def save_api_config(config):
    with open("api.yaml", "w") as file:
        yaml.dump(config, file)


def api_config_page():
    st.title("API 配置管理")

    # 创建一个空的占位符用于显示临时消息
    message_placeholder = st.empty()

    st.header("添加新模型")
    add_new_model(load_api_config(), message_placeholder)

    st.header("当前API配置")
    api_cfg = load_api_config()
    for model, config in api_cfg.items():
        st.subheader(f"模型: {model}")
        st.json(config)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"复制 {model}", key=f"copy_{model}"):
                st.session_state.copying_model = model
                st.rerun()
        with col2:
            if st.button(f"删除 {model}", key=f"delete_{model}"):
                del api_cfg[model]
                save_api_config(api_cfg)
                st.rerun()


def add_new_model(api_cfg, message_placeholder):
    if "clear_new_model" not in st.session_state:
        st.session_state.clear_new_model = False

    if st.session_state.clear_new_model:
        new_model = st.text_input("模型名称", key="new_model_name", value="")
        new_api_key = st.text_input("API Key", key="new_api_key", value="")
        new_api_base = st.text_input("API Base", key="new_api_base", value="")
        st.session_state.clear_new_model = False
    else:
        if "copying_model" in st.session_state:
            default_name = f"{st.session_state.copying_model}_copy"
            default_api_key = api_cfg[st.session_state.copying_model]["api_key"]
            default_api_base = api_cfg[st.session_state.copying_model]["api_base"]
        else:
            default_name = ""
            default_api_key = ""
            default_api_base = ""

        new_model = st.text_input("模型名称", key="new_model_name", value=default_name)
        new_api_key = st.text_input("API Key", key="new_api_key", value=default_api_key)
        new_api_base = st.text_input("API Base", key="new_api_base", value=default_api_base)

    if st.button("添加模型"):
        if new_model and new_api_key and new_api_base:
            api_cfg[new_model] = {"api_key": new_api_key, "api_base": new_api_base}
            save_api_config(api_cfg)
            show_success_message(message_placeholder, f"新模型 {new_model} 已成功添加")
            st.session_state.clear_new_model = True
            if "copying_model" in st.session_state:
                del st.session_state.copying_model
            time.sleep(1)
            st.rerun()
        else:
            st.warning("请填写所有字段")


def prompts_config_page():
    st.title("Prompts 配置管理")

    prompts = load_prompts()
    service_type_list = list(prompts.keys())

    selected_prompt = st.selectbox("选择要编辑的 Prompt:", service_type_list)

    current_prompt = prompts[selected_prompt]
    edited_prompt = st.text_area("编辑 Prompt:", value=current_prompt, height=300)

    # 创建一个空的占位符用于显示临时消息
    message_placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("保存 Prompt"):
            save_prompt(selected_prompt, edited_prompt)
            show_success_message(message_placeholder, f"{selected_prompt} Prompt 已成功保存")
            time.sleep(1)  # 等待1秒，让用户看到消息
            st.rerun()
    with col2:
        if st.button("删除 Prompt"):
            if len(prompts) > 1:  # 确保至少保留一个 Prompt
                delete_prompt(selected_prompt)
                show_success_message(message_placeholder, f"{selected_prompt} Prompt 已成功删除")
                time.sleep(1)  # 等待1秒，让用户看到消息
                st.rerun()
            else:
                st.error("无法删除最后一个 Prompt")

    st.header("添加新 Prompt")

    # 使用 session_state 来存储新 Prompt 的名称和内容，以及一个清空标志
    if "clear_new_prompt" not in st.session_state:
        st.session_state.clear_new_prompt = False

    if st.session_state.clear_new_prompt:
        new_prompt_name = st.text_input("新 Prompt 名称:", key="new_prompt_name", value="")
        new_prompt_content = st.text_area("新 Prompt 内容:", key="new_prompt_content", height=200, value="")
        st.session_state.clear_new_prompt = False
    else:
        new_prompt_name = st.text_input("新 Prompt 名称:", key="new_prompt_name")
        new_prompt_content = st.text_area("新 Prompt 内容:", key="new_prompt_content", height=200)

    if st.button("添加新 Prompt"):
        if new_prompt_name and new_prompt_name not in prompts:
            save_prompt(new_prompt_name, new_prompt_content)
            show_success_message(message_placeholder, f"新 Prompt {new_prompt_name} 已创建并保存")
            # 设置清空标志
            st.session_state.clear_new_prompt = True
            time.sleep(1)  # 等待1秒，让用户看到消息
            st.rerun()
        elif new_prompt_name in prompts:
            st.warning("该 Prompt 名称已存在")
        else:
            st.warning("请输入有效的 Prompt 名称")


def show_success_message(placeholder, message):
    placeholder.success(message)


def main():
    # 设置页面配置
    set_page_config()

    # 设置页面样式
    set_page_style()

    st.sidebar.title("导航")
    page = st.sidebar.radio("选择页面", ["主页", "API 配置", "Prompts 配置"])

    if page == "主页":
        home_page()
    elif page == "API 配置":
        api_config_page()
    elif page == "Prompts 配置":
        prompts_config_page()


def home_page():
    st.title("Academic Writing Assistant")

    api_cfg = load_api_config()
    prompts = load_prompts()

    model_list = list(api_cfg.keys())
    service_type_list = list(prompts.keys())

    default_model_index = 0
    default_service_type_index = (
        service_type_list.index("academic_rewriting") if "academic_rewriting" in service_type_list else 0
    )

    model = st.selectbox("请选择要使用的模型:", model_list, index=default_model_index)
    service_type = st.selectbox("请选择服务类型:", service_type_list, index=default_service_type_index)

    default_text = "The Knuth-Morris-Pratt string searching algorithm is way faster than brute force. It uses a prefix function to skip ahead when a mismatch is found, instead of starting over from the next character in the text."

    if "translation" in service_type:
        default_text = "人工智能技术正在迅速发展,并在各个领域得到广泛应用。它不仅能提高生产效率,还能帮助我们解决复杂的问题。而,我们也需要警惕人工智能可能带来的伦理和隐私问题,确保其发展方向符合人类的长远利益。"

    text = st.text_area("请输入您的文本:", value=default_text, height=100)
    debug_mode = st.checkbox("调试模式")

    if debug_mode:
        prompt = st.text_area("编辑Prompt:", value=prompts[service_type], height=300)
    else:
        prompt = prompts[service_type]

    if st.button("提交", type="primary") and text:
        try:
            os.environ["OPENAI_API_KEY"] = api_cfg[model]["api_key"]
            os.environ["OPENAI_API_BASE"] = api_cfg[model]["api_base"]

            rewritten_text, explanation, full_response = rewrite_text(text, prompt, model)

            display_results(text, rewritten_text, explanation, full_response, prompt, debug_mode)
        except Exception as e:
            st.error(f"处理过程中出现错误: {str(e)}")
    elif not text:
        st.warning("请入文本后再提交。")


def display_results(original_text, rewritten_text, explanation, full_response, prompt, debug_mode):
    word_diff = generate_word_diff(original_text, rewritten_text)

    st.subheader("优化结果对比:")
    st.markdown(f'<div class="diff-result">{word_diff}</div>', unsafe_allow_html=True)

    st.subheader("优化后的文本:")
    st.code(rewritten_text, language="markdown")

    st.subheader("修改说明:")
    st.write(explanation)

    with st.expander("Output", expanded=False):
        st.code(full_response, language="markdown")

    with st.expander("Prompt", expanded=False):
        st.code(prompt, language="markdown")


if __name__ == "__main__":
    main()
