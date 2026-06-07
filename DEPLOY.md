# 部署指南：让别人能通过网址访问你的 AI Resume Assistant

## 当前状态
- 本地运行：`streamlit run app.py` → 只有你自己能访问（localhost:8501）
- 别人无法通过任何网址打开

---

## 方案一：最快让别人看到（临时公网地址）—— ngrok

适合：想立刻发给朋友/面试官看效果

步骤：
1. 本地正常启动项目
   ```powershell
   cd ai-resume-assistant
   .\.venv\Scripts\Activate.ps1
   streamlit run app.py
   ```

2. 下载 ngrok（https://ngrok.com/），注册并获取 authtoken

3. 在**另一个** PowerShell 窗口运行：
   ```powershell
   ngrok http 8501
   ```

4. 复制 ngrok 给你的 https 地址（比如 `https://abc123.ngrok-free.app`），发给别人。

**注意**：关闭 ngrok 或关电脑后地址就失效了。

---

## 方案二：永久免费部署到互联网（推荐用于简历）

使用 **Streamlit Community Cloud**（官方免费托管）

### 准备工作
1. 拥有 GitHub 账号（没有就注册一个）
2. 把这个项目推到 GitHub（公开仓库）

### 部署步骤
1. 在 GitHub 新建一个仓库（名字比如 `ai-resume-assistant`），**不要初始化 README**（我们已经有）
2. 在本地执行推送命令（首次）：
   ```powershell
   cd ai-resume-assistant
   git add .
   git commit -m "Initial commit - AI Resume Assistant"
   git remote add origin https://github.com/你的用户名/ai-resume-assistant.git
   git push -u origin main
   ```
3. 打开浏览器访问：https://share.streamlit.io
4. 用 GitHub 登录
5. 点击 **New app**
6. 选择你的仓库
7. **Main file path** 填写：`app.py`
8. 点击 **Deploy!**

第一次部署会：
- 安装依赖
- 下载中文嵌入模型（shibing624/text2vec-base-chinese）
- 可能需要 3-8 分钟

部署成功后，你会得到一个永久网址，例如：
`https://你的用户名-ai-resume-assistant.streamlit.app`

### 部署后的注意事项
- 免费版 15 分钟无人访问会进入休眠，下次访问要等 30 秒~1 分钟冷启动
- 第一次加载模型会比较慢，属于正常
- 如果你想让访问者上传自己的简历，功能已经支持
- 建议不要把真实简历 + OpenAI Key 放公开版本（可以用测试简历）

---

## 其他部署平台

- **Hugging Face Spaces**：对 AI 项目很友好，支持 GPU
- **Render.com**：免费 tier 可用
- **Railway**：简单但免费额度有限

---

## 我已经帮你做的部署准备

- 添加了 `.gitignore`（防止 venv、缓存、大模型文件上传）
- 添加了 `.streamlit/config.toml`（主题 + 超时设置）
- 在 README.md 中增加了「如何让别人通过网址访问」章节
- 保留了 `data/test_resume.pdf` 和 `extracted_resume.txt`，方便部署后自动初始化

---

需要我帮你：
- 生成更详细的 GitHub 推送命令？
- 修改代码让部署更丝滑（比如自动重建向量库）？
- 准备一个专门的“在线演示版”配置？

随时说！