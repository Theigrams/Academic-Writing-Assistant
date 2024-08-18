import difflib
import os

import streamlit as st
import yaml

from academic_rewriter import rewrite_text


def load_config():
    with open("api.yaml", "r") as file:
        return yaml.safe_load(file)


def generate_word_diff(text1, text2):
    matcher = difflib.SequenceMatcher(None, text1, text2)
    result = []
    for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
        if opcode == "equal":
            result.append(text1[i1:i2])
        elif opcode == "insert":
            result.append(f"<ins>{text2[j1:j2]}</ins>")
        elif opcode == "delete":
            result.append(f"<del>{text1[i1:i2]}</del>")
        elif opcode == "replace":
            result.append(f"<del>{text1[i1:i2]}</del>")
            result.append(f"<ins>{text2[j1:j2]}</ins>")
    return "".join(result)


def main():
    # 设置全局样式
    st.markdown(
        """
    <style>
        /* 差异结果样式 */
        .diff-result {
            font-family: monospace;
            white-space: pre-wrap;
            line-height: 1.5;
            font-size: 1.0rem;
        }
        .diff-result ins {
            color: #28a745;
            background-color: #e6ffec;
            text-decoration: none;
        }
        .diff-result del {
            color: #d73a49;
            background-color: #ffeef0;
            text-decoration: line-through;
        }
        
        /* 深色模式适配 */
        @media (prefers-color-scheme: dark) {
            .diff-result ins {
                color: #85e89d;
                background-color: transparent;
            }
            .diff-result del {
                color: #f97583;
                background-color: transparent;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("学术论文润色工具")

    # 加载配置
    config = load_config()

    # 选择模型
    model_options = list(config.keys())
    model = st.selectbox("请选择要使用的模型:", model_options)

    # 选择服务类型
    service_type = st.selectbox(
        "请选择服务类型:", ["Academic Style Rewriting", "Grammar Correction", "Chinese to English Translation"]
    )

    # 文本输入，添加默认句子
    default_text = "The cat sat on the mat. It was a sunny day."
    text = st.text_area("请输入您的文本:", value=default_text, height=200)

    if st.button("提交"):
        if text:
            # 从配置文件中获取API设置
            api_key = config[model]["api_key"]
            api_base = config[model]["api_base"]

            # 设置环境变量
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["OPENAI_API_BASE"] = api_base

            try:
                # 调用润色函数
                rewritten_text = rewrite_text(text, service_type, model)

                # 生成逐字diff
                word_diff = generate_word_diff(text, rewritten_text)

                # 显示差异
                st.subheader("对比结果:")
                st.markdown(f'<div class="diff-result">{word_diff}</div>', unsafe_allow_html=True)

                # 显示完整的润色后文本
                st.subheader("润色后的完整文本:")
                st.code(rewritten_text, language="markdown")

            except Exception as e:
                st.error(f"处理过程中出现错误: {str(e)}")
        else:
            st.warning("请输入文本后再提交。")


if __name__ == "__main__":
    main()
