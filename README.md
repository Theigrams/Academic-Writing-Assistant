# Academic Writing Assistant

Academic Writing Assistant 是一款基于 AI 的学术写作辅助工具,旨在帮助研究人员和学生提升学术写作质量。

## 主要特性

- **多模型支持**: 基于 [litellm](https://github.com/BerriAI/litellm) 集成多种主流 LLM API
- **高亮修改**: 直观展示原文与优化后文本的差异
- **详细解释**: 提供 AI 修改的具体理由,深入理解优化逻辑
- **自定义 Prompt**: 支持根据个人需求定制专属 prompt

## 快速开始

### 安装

1. 克隆仓库:

   ```bash
   git clone https://github.com/Theigrams/Academic-Writing-Assistant.git
   ```

2. 安装依赖:

   ```bash
   pip install -r requirements.txt
   ```

### 配置

1. API 设置:
   编辑 `api.yaml` 文件,填入您的 API 信息:

   ```yaml
   model_name:
     api_key: "your-api-key"
     api_base: "https://api.example.com"
   ```

2. Prompt 准备:
   在 `prompts` 目录下创建 `.md` 文件,为不同类型的服务设置专属 prompt。

### 运行

1. 启动应用:

   ```bash
   streamlit run app.py
   ```

2. 在浏览器中访问显示的 URL (通常为 `http://localhost:8501`)

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
