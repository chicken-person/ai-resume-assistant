# AI Resume Assistant

**真正实用、可直接投入使用的 AI 简历优化助手**

针对应届生设计的专业工具：上传 PDF 简历 → 输入目标岗位 → 使用**免费 DeepSeek** 给出**具体可执行**的优化建议和 bullet 改写。

> **⚠️ 重要提示（GitHub 克隆用户必看）**  
> 直接克隆后运行 `streamlit run app.py` **一定会报错**！  
> 请**严格按照下方「保姆级部署指南（复制粘贴即可成功）」**操作，包含检查步骤，确保 100% 成功。

---

## 🛡️ 保姆级部署指南（复制粘贴即可 100% 成功）

**Windows 用户推荐流程（最稳）**：

```powershell
# 1. 克隆项目
git clone https://github.com/chicken-person/ai-resume-assistant.git
cd ai-resume-assistant

# 2. 一键安装依赖（强烈推荐）
.\setup.ps1

# 3. 配置 DeepSeek 免费 Key（必须）
# 打开 .env 文件，填入你的 Key
notepad .env
# 去 https://platform.deepseek.com/api_keys 注册并创建免费 Key（sk- 开头）

# 4. 运行检查程序（确保一切就绪）
.\check_install.ps1

# 5. 启动应用（检查通过后执行）
streamlit run app.py
```

**检查程序会告诉你：**
- Python 版本是否合格
- 虚拟环境是否正确激活
- 所有依赖是否安装
- .env 中的 DeepSeek Key 是否正确配置
- 核心模块是否能正常导入

只有所有检查通过（显示 🎉 所有检查通过），你才能成功运行应用。

**如果检查失败**，按照提示修复后，**再次运行** `.\check_install.ps1` 直到通过。

---

## 其他系统部署

```bash
# macOS / Linux
git clone https://github.com/chicken-person/ai-resume-assistant.git
cd ai-resume-assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 编辑 .env 填入 DeepSeek Key
cp .env.example .env
nano .env

# 手动检查（或参考 check_install.ps1 逻辑）
python -c "from resume_parser import process_resume; print('✅ 模块导入成功')"

streamlit run app.py
```

---

## ✨ 核心价值

- 不是泛泛而谈，而是**基于你真实简历内容**的深度诊断
- 针对具体目标岗位，给出**可直接复制的改写建议**（前后对比 + 理由）
- 指出真正缺失的内容（而非模板化建议）
- 支持连续对话追问

---

## 🛠 技术栈

- **LLM**：DeepSeek（deepseek-chat / deepseek-reasoner）—— 免费额度充足，中文极强
- **RAG**：LangChain + Chroma + text2vec-base-chinese
- **解析**：pypdf
- **前端**：Streamlit（简洁专业）
- **后端**：FastAPI（可选）

---

## 传统快速开始（已整合到上方保姆级指南）

请直接参考上方 **「保姆级部署指南（复制粘贴即可 100% 成功）」**，它包含了检查程序，成功率最高。

传统步骤（仅供参考）：
1. `.\setup.ps1`
2. 编辑 `.env` 填入 DeepSeek Key
3. `.\check_install.ps1` （必须！）
4. `streamlit run app.py` （仅在检查通过后）。

---

## 使用流程

1. **左侧上传**你的 PDF 简历
2. **输入目标岗位**（例如：法务助理、法院实习生、合规专员）
3. 点击「解析并建立知识库」
4. 去 **📊 深度分析报告** 标签，点击按钮生成专业分析
5. 去 **💬 与简历对话** 进行连续追问和 bullet 改写
6. 最后下载 Markdown 报告

---

## 功能说明

| 功能           | 说明                                      |
|----------------|-------------------------------------------|
| 深度分析报告   | DeepSeek 给出结构化诊断 + 具体改写建议     |
| 智能对话       | 支持上下文追问，可要求改写特定经历         |
| 一键下载报告   | 生成完整 Markdown，可直接用于简历迭代     |
| RAG 检索       | 所有回答都基于你简历真实内容（防幻觉）     |

---

## 常见问题

**Q: DeepSeek 真的免费吗？**  
A: 是的，新注册用户会获得大量免费 Token，个人使用通常足够。

**Q: 分析结果不准确怎么办？**  
A: 确保简历 PDF 文字可提取（扫描件效果差）。多试几次不同目标岗位，效果会更好。

**Q: 可以本地完全免费运行吗？**  
A: 可以。配置好 DeepSeek Key 后，所有分析都在 DeepSeek 免费额度内完成。

**Q: 支持英文简历吗？**  
A: 当前主要优化中文简历（尤其是法律/涉外方向）。英文支持有限。

---

## 📦 上传到 GitHub（已完成）

这个项目已经完整推送到 GitHub：

**仓库地址**：https://github.com/chicken-person/ai-resume-assistant

### 如何自己上传/同步（如果你 fork 或重新 clone）

```powershell
# 1. Fork 或 clone 这个仓库
git clone https://github.com/chicken-person/ai-resume-assistant.git
cd ai-resume-assistant

# 2. 或者如果你想创建自己的仓库
# 在 GitHub 创建新仓库后：
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

---

## 🖥️ 方便的本地部署方法

### 方法一：使用一键安装脚本（推荐 Windows 用户）

```powershell
# 克隆仓库
git clone https://github.com/chicken-person/ai-resume-assistant.git
cd ai-resume-assistant

# 运行一键设置脚本
.\setup.ps1
```

脚本会自动：
- 创建虚拟环境
- 安装所有依赖
- 创建 `.env` 文件（你只需编辑填入 DeepSeek Key）

然后运行：
```powershell
streamlit run app.py
```

### 方法二：手动安装（跨平台）

```bash
git clone https://github.com/chicken-person/ai-resume-assistant.git
cd ai-resume-assistant

# 创建虚拟环境
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置 Key（见下方）
# 编辑 .env 文件，填入你的 DeepSeek API Key

# 启动
streamlit run app.py
```

---

## 🔑 配置 DeepSeek 免费 API Key

1. 访问 https://platform.deepseek.com/
2. 用微信/手机号注册（新用户自动获得大量免费 Token 额度）
3. 进入 **API Keys** 页面 → 创建新 Key
4. 复制 Key（格式以 `sk-` 开头）
5. 在项目根目录的 `.env` 文件中填入：

```env
DEEPSEEK_API_KEY=sk-你的免费key
DEEPSEEK_MODEL=deepseek-chat
```

---

## 项目结构

```
ai-resume-assistant/
├── app.py                 # Streamlit 主界面（推荐入口）
├── main.py                # FastAPI 后端（可选）
├── resume_parser.py       # PDF 解析
├── rag_engine.py          # RAG + DeepSeek 分析核心
├── requirements.txt
├── .env.example
├── README.md
└── data/                  # 简历与向量库存储
```

---

## License

MIT

**Made for 真正需要改简历的应届生**  
希望这个工具能真正帮到你。欢迎反馈使用体验！