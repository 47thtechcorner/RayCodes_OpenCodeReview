<div align="center">
  <a href="https://youtu.be/p38pmJpjta8">
    <img src="https://img.youtube.com/vi/p38pmJpjta8/0.jpg" alt="Alibaba's Open Code: 100% Local Claude Code & Cursor Skill That Cuts Tokens 9x!">
  </a>
  <h3>📺 <a href="https://youtu.be/p38pmJpjta8">Watch the full tutorial on YouTube</a></h3>
</div>

<div align="center">
  <h1>Alibaba Open Code Review (OCR)</h1>
  <p><strong>A Precision Hybrid Deterministic-and-LLM Agent Harness for Code Auditing</strong></p>
  <p>
    <a href="https://github.com/alibaba/open-code-review/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square" /></a>
    <a href="https://www.npmjs.com/package/@alibaba-group/open-code-review"><img alt="npm" src="https://img.shields.io/npm/v/@alibaba-group/open-code-review?style=flat-square&color=orange" /></a>
    <a href="https://github.com/alibaba/open-code-review"><img alt="GitHub stars" src="https://img.shields.io/badge/Upstream-Alibaba%20Group-blueviolet?style=flat-square" /></a>
    <a href="https://open-codereview.ai"><img alt="Docs" src="https://img.shields.io/badge/Docs-open--codereview.ai-cyan?style=flat-square" /></a>
    <a href="https://huggingface.co/datasets/Alibaba-Aone/aacr-bench"><img alt="AACR-Bench" src="https://img.shields.io/badge/Benchmark-AACR--Bench-yellow?style=flat-square" /></a>
  </p>
</div>

> "Instead of operating as raw model weights, Open Code Review functions as a precision agent harness. It wraps deterministic file bundling and an independent reflection falsification filter around any OpenAI- or Anthropic-compatible LLM—achieving 4.7x higher precision and consuming up to 15x fewer tokens than general coding agents."

---

## 📊 Production Test Workflows

| Workflow | Capability Tested | Input Artifact | Expected Deliverable |
|---|---|---|---|
| Zero-Noise Patch Audit | Eliminates nitpicks and isolates genuine logic flaws | Messy uncommitted changes with fifty style edits | Exact line-level feedback without false alarm chatter |
| Full Repository Vulnerability Scan | Audits entire codebase without requiring Git history | Unfamiliar legacy backend folder with raw queries | Structured security report isolating critical injection vulnerabilities |
| Automated Pull Request Gating | Resolves merge-base diffs and exports structured data | Multi-file feature branch diverged from main | Actionable JSON findings with line numbers for CI |

---

## ⚡ Installation & Setup

Paste this prompt into your AI coding assistant (**Antigravity**, **Claude Code**, **Cursor**, **Codex**, or **OpenCode**) to install and configure Open Code Review automatically:

```text
Install Alibaba's Open Code Review CLI and agent skills in this workspace using the official repository at https://github.com/alibaba/open-code-review and documentation at open-codereview.ai. Run npx skills add alibaba/open-code-review (or npm install -g @alibaba-group/open-code-review), verify the ocr --version binary works, and configure it in Delegation Mode (or connect it to my local Ollama OpenAI-compatible endpoint at http://localhost:11434/v1) so I can run reviews without paid API keys.
```

*(Prefer manual terminal setup? See the [Manual CLI Installation & Reference](#-manual-cli-installation--reference) section at the bottom.)*

---

## 🤖 Agent Review Prompts

Once installed, paste any of these 3 prompts into your AI coding assistant to test Open Code Review against the included sample inputs:

### Task 1: Uncommitted Changes Review (Zero-Noise Patch Audit)
Reviews the messy session manager in `inputs/task1_messy_session_manager.py`, testing the reflection filter's ability to discard superficial formatting changes and pinpoint real concurrency and SQL bugs:

```text
Use the open-code-review skill to run a line-level review on inputs/task1_messy_session_manager.py using `ocr review --audience agent`. Discard cosmetic style nitpicks, list only verified high-confidence bugs with exact line numbers and diff patches, and save a brief Markdown review report to outputs/task1_zero_noise_review.md.
```

---

### Task 2: Full Directory Security Audit (Cold-Start Scan)
Audits the legacy billing service directory in `inputs/legacy_service/` without Git diff history, tracing untrusted router inputs down to raw SQL injection in `db.py`:

```text
Run `ocr scan --path inputs/legacy_service/` to audit the legacy service for SQL injection, thread-safety issues, and unhandled network exceptions. Summarize the verified findings with diff patches in a brief Markdown report saved to outputs/task2_security_audit.md.
```

---

### Task 3: Branch Comparison PR Check (Merge-Base Gatekeeper)
Evaluates the pull request diff in `inputs/task3_pr_feature.diff` using merge-base diffing, sub-agent file bundling, and distributed transaction boundary verification:

```text
Compare the feature branch diff in inputs/task3_pr_feature.diff using `ocr review --from main --analysis --format json` and write a brief Markdown CI gatekeeper report to outputs/task3_pr_gatekeeper.md listing every critical defect, exact file and line number, and recommended patch.
```

---

## 📈 Benchmark Showdown (AACR-Bench)

Evaluated on Alibaba's **AACR-Bench** dataset across **50 popular open-source repositories**, **200 real pull requests**, and **10 programming languages** with **1,505 engineer-verified ground-truth issues** using identical underlying models:

| Metric / Attribute | Alibaba Open Code Review (ocr) | Claude Code (General Agent) | Key Takeaway |
|---|---|---|---|
| **Precision (Claude-4.6-Opus)** | **33.90%** | 7.23% | **4.7x higher accuracy**; filters out false alarm noise |
| **SEM-F1 Score (Peak)** | **25.10%** | 11.57% | **2.17x better balance** between bug recall and precision |
| **Avg. Token Consumption** | **~385K tokens** | ~5,664K tokens | **9x to 15x cheaper** per pull request review |
| **Recall Strategy** | Conservative (~20% top-p) | Broad / Verbose | Designed as high-signal first pass, not spam bot |

---

## 🛠️ Practical Use Cases

- 🛡️ **Zero-Noise Pull Request Auditing**: Filters out cosmetic formatting opinions so human reviewers only spend time on real concurrency bugs, null pointers, and logic errors.
- ⚡ **Pre-Commit Safety Gate**: Catches unhandled exceptions and unescaped inputs on staged changes before code ever leaves the local workstation.
- 🔍 **Legacy Codebase Triage**: Uses `ocr scan` on unfamiliar open-source repositories without Git history to rapidly identify security hot-spots and dead code.
- 🔒 **Air-Gapped Compliance**: Pairs seamlessly with local Ollama runtimes (e.g., Qwen2.5-Coder, DeepSeek-R1) to review sensitive internal IP without cloud API leakage.
- 👥 **Host Agent Delegation**: Integrates natively into Antigravity, Claude Code, and Cursor via skills, running structured review guardrails without separate API credentials.

---

## 🚀 Future Feature Roadmap

- 🌐 **Enhanced GitHub Actions & GitLab CI Native Runners**: Turnkey automated PR comment posting with SARIF summary widgets.
- 🧠 **AST-Guided Multi-Repository Dependency Tracing**: Cross-repo reference resolution for microservice architectures.
- 📦 **Standalone Binary Releases**: Native single-binary downloads without requiring Node.js runtime prerequisites.
- 📊 **Interactive Browser Session Replay UI**: Local visual interface to step through review sessions, accept suggestions, and hide resolved comments.
- 📈 **Continuous Project Rule Learning**: Automatically infer custom project review rules from historical repository commit fixes.

---

## 💻 Manual CLI Installation & Reference

If you prefer installing and running the CLI directly in your terminal without an AI coding agent:

```bash
# Install the CLI binary globally
npm install -g @alibaba-group/open-code-review

# Verify installation
ocr --version

# Mode A: Delegation Mode (Zero API keys — reuses host agent credentials)
ocr delegate preview
ocr delegate rule src/main.py src/handler.py

# Mode B: Local Ollama (100% private offline auditing)
ocr config provider
# Select 'Custom / OpenAI-Compatible' -> Base URL: http://localhost:11434/v1 -> Model: qwen2.5-coder:latest

# Review uncommitted changes in current workspace
ocr review

# Review current branch against main (merge-base mode)
ocr review --from main

# Compare two specific branches
ocr review --from main --to feature-branch

# Review a specific commit
ocr review --commit abc1234

# Full-file security audit (no Git diff needed)
ocr scan --path inputs/legacy_service/

# Export review findings to JSON for CI/CD pipelines
ocr review --format json --output review-results.json
```

---

## 🤝 Contributing & Community

- Upstream Repository: [alibaba/open-code-review](https://github.com/alibaba/open-code-review)
- Official Documentation: [open-codereview.ai](https://open-codereview.ai)
- Benchmark Dataset: [Hugging Face AACR-Bench](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench)

To support this project and daily AI engineering breakdowns: [Ray Codes Support](https://ko-fi.com/prayasjain)

---

<sub>Keywords: opencode review, claude code review, claude code skill, code review skill, open code review, claude code plugin, agent skills, ai code review, pull request review, ocr scan, ocr review, token efficient ai, antigravity code review, coderabbit alternative, greptile alternative, ollama code review, qwen coder ollama, security code review, ai code audit, pr review ai, apache 2.0 ai, open code review alibaba, alibaba open code review, opencodereview, google antigravity skill, security scanner, ai vulnerability scanner, cursor ai plugin</sub>
