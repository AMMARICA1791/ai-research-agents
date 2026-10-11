# AI Research Agents — 可验证证据驱动的开源 AI 研究实验室

**项目目标：**使用尽可能低的成本，研究并验证开放权重 AI 模型提出的代码修改，让开发者能够复现实验结果。

**现状：**这是实验性研究原型，不是成熟商业服务，也不是能够独立修复任意软件的智能体。系统有七个协调步骤，**并不意味着有七个独立推理的 AI 模型**。

## 已经验证的功能
- 对 Python 代码和部分依赖关系进行有限范围的静态检查。
- 在 GitHub 运行之间保存经过筛选的研究统计信息。
- 通过 Ollama 运行 Qwen 开放权重模型，无需付费 API 密钥。
- Qwen2.5-Coder 1.5B 曾针对真实代码中的 GitHub 网址欺骗问题生成修复方案；经过独立测试与人工审核后，项目负责人在 [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17) 中合并了该修复。
- 具有可复现的少量**合成测试**，但不能据此推断在未知实际项目中的整体准确率。

## 如何体验
在 GitHub 打开 **Actions → Research Lab - Persistent Missions → Run workflow**。请勿输入密码、密钥或私人数据。若要运行免费的本地模型，请选择 **Zero-Key Local Qwen Research**。参见 [快速入门](QUICKSTART.md)。

## 如何参与
阅读 [贡献指南](CONTRIBUTING.md)、[路线图](ROADMAP.md)、[安全政策](SECURITY.md)、[治理说明](GOVERNANCE.md) 和 [功能范围与限制](docs/PROJECT_SCOPE.md)。欢迎提交可复现实验及问题报告。

## 许可证与权利
本项目代码采用 [Apache License 2.0](LICENSE)，由仓库所有者于 2026 年 10 月批准。遵守许可条件即可修改、分发和商业使用代码；**开源代码并不赋予所有者独家商业使用权**。各贡献者保留自己作品的著作权。请参阅 [版权声明](NOTICE)、[商标说明](TRADEMARKS.md) 和 [授权及限制](docs/LICENSING_DECISION.md)。外部依赖项仍适用其各自许可证。

**原则：**只有经过独立验证并有可复现证据的结果，才作为已证实的 AI 能力发布。

其他语言：[English](README.md) · [العربية](README.ar.md) · [Português](README.pt-BR.md) · [Español](README.es.md)。

## 当前统一状态 — 2026 年 10 月

- 本项目是实验性研究实验室，并非成熟 SaaS 或自主软件开发者。七个阶段是协调流程，不是七个独立推理智能体。
- [三个命令的演示](DEMO.md)：Python 3.11+，无需 API 密钥或本地模型；包含八个人工合成案例、确定性的合成修复，以及对 [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17) 历史回归测试的重测。**不会重新运行 Qwen**。
- [公开 Python 仓库审查](docs/PUBLIC_REPO_AUDIT.md)：有限静态分析，不执行外部代码；结果仅供人工复核，并非安全认证。
- [学术文献发现](docs/SCHOLARLY_DISCOVERY.md)：采集 Crossref 书目元数据，记录来源、时间和不确定性；不阅读全文、不评价科学质量、不使用大语言模型。
- [版本证据](VERIFIED_RELEASE.md) 区分历史记录和新测试；[贡献范围](CONTRIBUTING.md) 当前有限。不提供生产保证。
