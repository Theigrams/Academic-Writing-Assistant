import difflib

import streamlit as st


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


def set_page_style():
    st.markdown(
        """
    <style>
        /* Existing styles */
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

        /* New styles */
        h1, h2, h3 {
            color: #1e3a8a;
        }

        /* Sidebar style adjustments */
        .css-1d391kg {
            padding-top: 1rem;
            padding-right: 0.5rem;
            padding-left: 0.5rem;
        }
        .css-1d391kg .block-container {
            padding-top: 1rem;
        }
        /* Adjust sidebar width */
        .css-1q1n0ol {
            max-width: 14rem;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def set_page_config():
    st.set_page_config(page_title="学术写作助手", page_icon="✍️", initial_sidebar_state="expanded")
