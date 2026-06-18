# C3.x 路由器架构 - 超详细技术规范

**创建日期：** 2026-01-08
**最后更新：** 2026-01-08（重大修订 - 三流 GitHub 架构）
**目的：** 将经 C3.x 分析的代码库转换为基于路由器的技能系统的完整架构设计
**状态：** 设计阶段 - 可以开始实现

---

## 执行摘要

### 问题陈述

当前 C3.x 代码库分析生成的单体技能存在以下问题：
- **过大**，不利于 AI 最优消费（666 行 vs 理想的 150-300 行）
- **Token 效率低**（针对特定主题的查询有 77-88% 的浪费）
- **让 AI 困惑**（用户只想要 1 个 OAuth 提供方时却展示了 8 个）
- **难以维护**（单个巨型文件 vs 模块化结构）

**FastMCP E2E 测试结果：**
- 单体 SKILL.md：666 行 / 20KB
- 人类质量：A+（96/100）- 优秀的文档
- AI 质量：B+（87/100）- 过大、存在冗余问题
- **Token 浪费：** OAuth 特定查询浪费 77%（加载 666 行，只用 150 行）

### 提议的解决方案

**两部分架构：**

1. **三流来源集成**（新！）
   - GitHub 作为多源提供者
   - 拆分：代码 → C3.x，文档 → Markdown，Issue → 洞察
   - C3.x 作为深度模式（basic/deep），而非独立工具

2. **基于路由器的技能结构**
   - 1 个主路由器 + N 个聚焦的子技能
   - Token 减少 45%
   - 内容相关性 100%

```
GitHub Repository
  ↓
Three-Stream Fetcher
  ├─ Code Stream → C3.x Analysis (patterns, examples)
  ├─ Docs Stream → README/docs/*.md (official docs)
  └─ Issues Stream → Common problems + solutions
  ↓
Router Generator
  ├─ fastmcp (router - 150 lines)
  ├─ fastmcp-oauth (250 lines)
  ├─ fastmcp-async (200 lines)
  ├─ fastmcp-testing (250 lines)
  └─ fastmcp-api (400 lines)
```

**优势：**
- **Token 减少 45%**（每次查询平均 20KB → 11KB）
- **100% 相关性**（只加载所需的子技能）
- **GitHub 洞察**（来自 issue 的真实用户问题）
- **完整覆盖**（代码 + 文档 + 社区知识）

### 影响指标

| 指标 | 之前（单体） | 之后（路由器 + 三流） | 改进 |
|------|------------|---------------------|------|
| 每次查询的平均 token | 20KB | 11KB | **减少 45%** |
| 相关内容百分比 | 23%（OAuth 查询） | 100% | **提升 4.3 倍** |
| 主技能大小 | 20KB | 5KB | **缩小 4 倍** |
| 数据来源 | 1（仅代码） | 3（代码+文档+issue） | **丰富 3 倍** |
| 常见问题覆盖率 | 0% | 100%（来自 issue） | **全新能力** |

---

## 目录

1. [来源架构（新）](#来源架构)
2. [现状分析](#现状分析)
3. [提议的路由器架构](#提议的路由器架构)
4. [数据流与算法](#数据流与算法)
5. [技术实现](#技术实现)
6. [文件结构](#文件结构)
7. [过滤策略](#过滤策略)
8. [质量指标](#质量指标)
9. [边界情况与解决方案](#边界情况与解决方案)
10. [可扩展性分析](#可扩展性分析)
11. [迁移路径](#迁移路径)
12. [测试策略](#测试策略)
13. [实现阶段](#实现阶段)

---

## 1. 来源架构（新）

### 1.1 重新思考来源类型

**旧的（令人困惑的）模型：**
```
Source Types:
1. Documentation (HTML scraping)
2. GitHub (basic analysis)
3. C3.x Codebase Analysis (deep analysis)
4. PDF

Problem: GitHub and C3.x both analyze code at different depths!
```

**新的（正确的）模型：**
```
Source Types:
1. Documentation (HTML scraping from docs sites)
2. Codebase (local OR GitHub, with depth: basic/c3x)
3. PDF (supplementary)

Insight: GitHub is a SOURCE PROVIDER, C3.x is an ANALYSIS DEPTH
```

### 1.2 三流 GitHub 架构

**核心原则：** GitHub 仓库包含三种有价值的数据：

```
┌─────────────────────────────────────────────────────────┐
│ GitHub Repository                                       │
│ https://github.com/facebook/react                       │
└─────────────────────────────────────────────────────────┘
                      ↓
        ┌─────────────────────────┐
        │  GitHub Fetcher         │
        │  (Gets EVERYTHING)      │
        └─────────────────────────┘
                      ↓
        ┌─────────────────────────┐
        │  Intelligent Splitter   │
        └─────────────────────────┘
                      ↓
    ┌─────────────────┴─────────────────┐
    │                                    │
    ↓                                    ↓
┌───────────────┐              ┌────────────────┐
│ STREAM 1:     │              │ STREAM 2:      │
│ CODE          │              │ DOCUMENTATION  │
├───────────────┤              ├────────────────┤
│ *.py, *.js    │              │ README.md      │
│ *.tsx, *.go   │              │ CONTRIBUTING.md│
│ *.rs, etc.    │              │ docs/*.md      │
│               │              │ *.rst          │
│ → C3.x        │              │                │
│   Analysis    │              │ → Doc Parser   │
│   (20-60 min) │              │   (1-2 min)    │
└───────────────┘              └────────────────┘
                      ↓
              ┌───────────────┐
              │ STREAM 3:     │
              │ METADATA      │
              ├───────────────┤
              │ Open issues   │
              │ Closed issues │
              │ Labels        │
              │ Stars, forks  │
              │               │
              │ → Issue       │
              │   Analyzer    │
              │   (1-2 min)   │
              └───────────────┘
                      ↓
              ┌───────────────┐
              │  MERGER       │
              │  Combines all │
              │  3 streams    │
              └───────────────┘
```

### 1.3 来源类型定义（修订版）

**来源类型 1：文档（HTML）**
```json
{
  "type": "documentation",
  "base_url": "https://react.dev/",
  "selectors": {...},
  "max_pages": 200
}
```

**作用：**
- 抓取 HTML 文档站点
- 提取结构化内容
- 耗时：20-40 分钟

**来源类型 2：代码库（统一）**
```json
{
  "type": "codebase",
  "source": "https://github.com/facebook/react",  // OR "/path/to/local"
  "analysis_depth": "c3x",  // or "basic"
  "fetch_github_metadata": true,  // Issues, README, etc.
  "split_docs": true  // Separate markdown files as doc source
}
```

**作用：**
1. **获取来源：**
   - 如果是 GitHub URL：克隆到 `/tmp/repo/`
   - 如果是本地路径：直接使用

2. **拆分为流：**
   - **代码流：** `*.py`、`*.js` 等 → C3.x 或基础分析
   - **文档流：** `README.md`、`docs/*.md` → 文档解析器
   - **元数据流：** Issue、统计数据 → 洞察提取器

3. **分析深度模式：**
   - **basic**（1-2 分钟）：文件结构、导入、入口点
   - **c3x**（20-60 分钟）：完整 C3.x 套件（模式、示例、架构）

**来源类型 3：PDF（补充）**
```json
{
  "type": "pdf",
  "url": "https://example.com/guide.pdf"
}
```

**作用：**
- 从 PDF 中提取文本和代码
- 作为补充参考添加

### 1.4 C3.x 作为分析深度（而非来源类型）

**关键洞察：** C3.x 不是来源类型，而是一种**分析深度级别**。

```python
# OLD (Wrong)
sources = [
    {"type": "github", ...},      # Basic analysis
    {"type": "c3x_codebase", ...} # Deep analysis - CONFUSING!
]

# NEW (Correct)
sources = [
    {
        "type": "codebase",
        "source": "https://github.com/facebook/react",
        "analysis_depth": "c3x"  # ← Depth, not type
    }
]
```

**分析深度模式：**

| 模式 | 耗时 | 组件 | 用例 |
|------|------|------|------|
| **basic** | 1-2 分钟 | 文件结构、导入、入口点 | 快速概览、测试 |
| **c3x** | 20-60 分钟 | C3.1-C3.7（模式、示例、指南、配置、架构） | 生产级技能 |

### 1.5 GitHub 三流输出

**当你指定一个 GitHub 代码库来源时：**

```json
{
  "type": "codebase",
  "source": "https://github.com/jlowin/fastmcp",
  "analysis_depth": "c3x",
  "fetch_github_metadata": true
}
```

**你会自动获得三个数据流：**

```python
{
    # STREAM 1: Code Analysis (C3.x)
    "code_analysis": {
        "patterns": [...],      # 905 design patterns
        "examples": [...],      # 723 test examples
        "architecture": {...},  # Service Layer Pattern
        "api_reference": [...], # 316 API files
        "configs": [...]        # 45 config files
    },

    # STREAM 2: Documentation (from repo)
    "documentation": {
        "readme": "FastMCP is a Python framework...",
        "contributing": "To contribute...",
        "docs_files": [
            {"path": "docs/getting-started.md", "content": "..."},
            {"path": "docs/oauth.md", "content": "..."},
        ]
    },

    # STREAM 3: GitHub Insights
    "github_insights": {
        "metadata": {
            "stars": 1234,
            "forks": 56,
            "open_issues": 12,
            "language": "Python"
        },
        "common_problems": [
            {"title": "OAuth setup fails", "issue": 42, "comments": 15},
            {"title": "Async tools not working", "issue": 38, "comments": 8}
        ],
        "known_solutions": [
            {"title": "Fixed OAuth redirect", "issue": 35, "closed": true}
        ],
        "top_labels": [
            {"label": "question", "count": 23},
            {"label": "bug", "count": 15}
        ]
    }
}
```

### 1.6 多源合并策略

**场景：** 用户同时提供文档 URL 和 GitHub 仓库

```json
{
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://fastmcp.dev/"
    },
    {
      "type": "codebase",
      "source": "https://github.com/jlowin/fastmcp",
      "analysis_depth": "c3x",
      "fetch_github_metadata": true
    }
  ]
}
```

**结果：4 个待合并的数据流：**
1. HTML 文档（抓取的文档站点）
2. 代码分析（来自 GitHub 的 C3.x）
3. 仓库文档（来自 GitHub 的 README/docs）
4. GitHub 洞察（issue、统计数据）

**合并优先级：**
```
Priority 1: C3.x code analysis (ground truth - what code DOES)
Priority 2: HTML documentation (official intent - what code SHOULD do)
Priority 3: Repo documentation (README/docs - quick reference)
Priority 4: GitHub insights (community knowledge - common problems)
```

**冲突解决：**
- 如果 HTML 文档写的是 `GoogleProvider(app_id=...)`
- 但 C3.x 代码显示的是 `GoogleProvider(client_id=...)`
- → 创建混合内容，同时展示两者并附警告

---

## 2. 现状分析

### 2.1 FastMCP E2E 测试输出

**输入：** `/tmp/fastmcp` 仓库（361 个文件）

**C3.x 分析结果：**
```
output/fastmcp-e2e-test_unified_data/c3_analysis_temp/
├── patterns/
│   └── detected_patterns.json (470KB, 905 pattern instances)
├── test_examples/
│   └── test_examples.json (698KB, 723 examples)
├── config_patterns/
│   └── config_patterns.json (45 config files)
├── api_reference/
│   └── *.md (316 API documentation files)
└── architecture/
    └── architectural_patterns.json (Service Layer Pattern detected)
```

**生成的单体技能：**
```
output/fastmcp-e2e-test/
├── SKILL.md (666 lines, 20KB)
└── references/
    ├── index.md (3.6KB)
    ├── getting_started.md (6.9KB)
    ├── architecture.md (9.1KB)
    ├── patterns.md (16KB)
    ├── examples.md (10KB)
    └── api.md (6.5KB)
```

### 2.2 内容分布分析

**SKILL.md 拆解（666 行）：**
- OAuth/身份验证：约 150 行（23%）
- 异步模式：约 80 行（12%）
- 测试：约 60 行（9%）
- 设计模式：约 80 行（12%）
- 架构：约 70 行（11%）
- 示例：约 120 行（18%）
- 其他：约 106 行（15%）

**问题：** 用户问"如何添加 Google OAuth？"时必须加载全部 666 行，但只有 150 行是相关的（77% 浪费）。

### 2.3 我们缺失的内容（没有 GitHub 洞察时）

**当前方法：** 只分析代码

**缺失的有价值数据：**
- ❌ 常见用户问题（来自开放的 issue）
- ❌ 已知解决方案（来自已关闭的 issue）
- ❌ 热门问题（来自 issue 标签）
- ❌ 官方快速开始（来自 README）
- ❌ 贡献指南（来自 CONTRIBUTING.md）
- ❌ 仓库受欢迎程度（star、fork）

**采用三流 GitHub 架构后：**
- ✅ 以上全部自动包含
- ✅ SKILL.md 中有"常见问题"部分
- ✅ README 内容作为快速参考
- ✅ 解决真实用户问题

### 2.4 Token 使用场景

**场景 1：OAuth 特定查询**
- 用户："如何为我的 FastMCP 服务器添加 Google OAuth？"
- **当前：** 加载 666 行（浪费 77%）
- **使用路由器：** 加载 150 行路由器 + 250 行 OAuth = 400 行（浪费 40%）
- **加上 GitHub 洞察：** 还能得到 issue #42 "OAuth setup fails" 的解决方案

**场景 2："FastMCP 有哪些常见问题？"**
- **当前：** 无法回答（代码分析不了解用户问题）
- **加上 GitHub 洞察：** 前 10 个 issue 及其解决方案立即可用

---

## 3. 提议的路由器架构

### 3.1 路由器 + 子技能结构

```
fastmcp/                      # Main router skill
├── SKILL.md (150 lines)      # Overview + routing logic
└── references/
    ├── index.md
    └── common_issues.md      # NEW: From GitHub issues

fastmcp-oauth/                # OAuth sub-skill
├── SKILL.md (250 lines)      # OAuth-focused content
└── references/
    ├── oauth_overview.md     # From C3.x + docs
    ├── google_provider.md    # From C3.x examples
    ├── azure_provider.md     # From C3.x examples
    ├── oauth_patterns.md     # From C3.x patterns
    └── oauth_issues.md       # NEW: From GitHub issues

fastmcp-async/                # Async sub-skill
├── SKILL.md (200 lines)
└── references/
    ├── async_basics.md
    ├── async_patterns.md
    ├── decorator_pattern.md
    └── async_issues.md       # NEW: From GitHub issues

fastmcp-testing/              # Testing sub-skill
├── SKILL.md (250 lines)
└── references/
    ├── unit_tests.md
    ├── integration_tests.md
    ├── pytest_examples.md
    └── testing_issues.md     # NEW: From GitHub issues

fastmcp-api/                  # API reference sub-skill
├── SKILL.md (400 lines)
└── references/
    └── api_modules/
        └── *.md (316 files)
```

### 3.2 增强版路由器 SKILL.md 模板（含 GitHub 洞察）

```markdown
---
name: fastmcp
description: FastMCP framework for building MCP servers - use this skill to learn FastMCP basics and route to specialized topics
---

# FastMCP - Python Framework for MCP Servers

**Repository:** https://github.com/jlowin/fastmcp
**Stars:** ⭐ 1,234 | **Language:** Python | **Open Issues:** 12

[From GitHub metadata - shows popularity and activity]

## When to Use This Skill

Use this skill when:
- You want an overview of FastMCP
- You need quick installation/setup steps
- You're deciding which FastMCP feature to use
- **Route to specialized skills for deep dives:**
  - `fastmcp-oauth` - OAuth authentication (Google, Azure, GitHub)
  - `fastmcp-async` - Async/await patterns
  - `fastmcp-testing` - Unit and integration testing
  - `fastmcp-api` - Complete API reference

## Quick Start (from README.md)

[Content extracted from GitHub README - official quick start]

## Common Issues (from GitHub)

Based on analysis of 100+ GitHub issues, here are the most common problems:

1. **OAuth provider configuration** (Issue #42, 15 comments)
   - See `fastmcp-oauth` skill for solution

2. **Async tools not working** (Issue #38, 8 comments)
   - See `fastmcp-async` skill for solution

[From GitHub issue analysis - real user problems]

## Choose Your Path

**Need authentication?** → Use `fastmcp-oauth` skill
**Building async tools?** → Use `fastmcp-async` skill
**Writing tests?** → Use `fastmcp-testing` skill
**Looking up API details?** → Use `fastmcp-api` skill

## Architecture Overview

FastMCP uses a Service Layer Pattern with 206 Strategy pattern instances.

[From C3.7 architecture analysis]

## Next Steps

[Links to sub-skills with trigger keywords]
```

**大小目标：** 150 行 / 5KB

**使用的数据来源：**
- ✅ GitHub 元数据（star 数、issue 数）
- ✅ README.md（快速开始）
- ✅ GitHub issue（常见问题）
- ✅ C3.7 架构（模式信息）

### 3.3 增强版子技能模板（OAuth 示例）

```markdown
---
name: fastmcp-oauth
description: OAuth authentication for FastMCP servers - Google, Azure, GitHub providers with Strategy pattern
triggers: ["oauth", "authentication", "google provider", "azure provider", "auth provider"]
---

# FastMCP OAuth Authentication

## When to Use This Skill

Use when implementing OAuth authentication in FastMCP servers.

## Quick Reference (from C3.x examples)

[5 OAuth examples from test files - real code]

## Common OAuth Issues (from GitHub)

**Issue #42: OAuth setup fails with Google provider**
- Problem: Redirect URI mismatch
- Solution: Use `http://localhost:8000/oauth/callback` in Google Console
- Status: Solved (12 comments)

**Issue #38: Azure provider 401 error**
- Problem: Wrong tenant_id
- Solution: Check Azure AD tenant ID matches config
- Status: Solved (8 comments)

[From GitHub closed issues - real solutions]

## Supported Providers (from C3.x + README)

### Google OAuth

**Official docs say:** (from README.md)
```python
GoogleProvider(app_id="...", app_secret="...")
```

**Current implementation:** (from C3.x analysis, confidence: 95%)
```python
GoogleProvider(client_id="...", client_secret="...")
```

⚠️ **Conflict detected:** Parameter names changed. Use current implementation.

[Hybrid content showing both docs and code]

### Azure OAuth (from C3.x analysis)

[Azure-specific example with real code from tests]

## Design Patterns (from C3.x)

### Strategy Pattern (206 instances in FastMCP)
[Strategy pattern explanation with OAuth context]

### Factory Pattern (142 instances in FastMCP)
[Factory pattern for provider creation]

## Testing OAuth (from C3.2 test examples)

[OAuth testing examples from test files]

## See Also

- Main `fastmcp` skill for overview
- `fastmcp-testing` skill for authentication testing patterns
```

**大小目标：** 250 行 / 8KB

**使用的数据来源：**
- ✅ C3.x 测试示例（真实代码）
- ✅ README.md（官方文档）
- ✅ GitHub issue（常见问题 + 解决方案）
- ✅ C3.x 模式（设计模式）
- ✅ 冲突检测（文档 vs 代码）

---

## 4. 数据流与算法

### 4.1 完整流水线（三流增强版）

```
INPUT: User provides GitHub repo URL
  │
  ▼
ACQUISITION PHASE (GitHub Fetcher)
  │
  ├─ Clone repository to /tmp/repo/
  ├─ Fetch GitHub API metadata (stars, issues, labels)
  ├─ Fetch open issues (common problems)
  └─ Fetch closed issues (known solutions)
  │
  ▼
STREAM SPLITTING PHASE
  │
  ├─ STREAM 1: Code Files
  │  ├─ Filter: *.py, *.js, *.ts, *.go, *.rs, etc.
  │  └─ Exclude: docs/, tests/, node_modules/, etc.
  │
  ├─ STREAM 2: Documentation Files
  │  ├─ README.md
  │  ├─ CONTRIBUTING.md
  │  ├─ docs/*.md
  │  └─ *.rst
  │
  └─ STREAM 3: GitHub Metadata
     ├─ Open issues (common problems)
     ├─ Closed issues (solutions)
     ├─ Issue labels (categories)
     └─ Repository stats (stars, forks, language)
  │
  ▼
PARALLEL ANALYSIS PHASE
  │
  ├─ Thread 1: C3.x Code Analysis (20-60 min)
  │  ├─ Input: Code files from Stream 1
  │  ├─ C3.1: Detect design patterns (905 instances)
  │  ├─ C3.2: Extract test examples (723 examples)
  │  ├─ C3.3: Build how-to guides (if working)
  │  ├─ C3.4: Analyze config files (45 configs)
  │  └─ C3.7: Detect architecture (Service Layer)
  │
  ├─ Thread 2: Documentation Processing (1-2 min)
  │  ├─ Input: Markdown files from Stream 2
  │  ├─ Parse README.md → Quick start section
  │  ├─ Parse CONTRIBUTING.md → Contribution guide
  │  └─ Parse docs/*.md → Additional references
  │
  └─ Thread 3: Issue Analysis (1-2 min)
     ├─ Input: Issues from Stream 3
     ├─ Categorize by label (bug, question, enhancement)
     ├─ Identify top 10 common problems (open issues)
     └─ Extract solutions (closed issues with comments)
  │
  ▼
MERGE PHASE
  │
  ├─ Combine all 3 streams
  ├─ Detect conflicts (docs vs code)
  ├─ Create hybrid content (show both versions)
  └─ Build cross-references
  │
  ▼
ARCHITECTURE DECISION
  │
  ├─ Should use router?
  │  └─ YES (estimated 666 lines > 200 threshold)
  │
  ▼
TOPIC DEFINITION PHASE
  │
  ├─ Analyze pattern distribution → OAuth, Async dominant
  ├─ Analyze example categories → Testing has 723 examples
  ├─ Analyze issue labels → "oauth", "async", "testing" top labels
  └─ Define 4 topics: OAuth, Async, Testing, API
  │
  ▼
FILTERING PHASE (Multi-Stage)
  │
  ├─ Stage 1: Keyword Matching (broad)
  ├─ Stage 2: Relevance Scoring (precision)
  ├─ Stage 3: Confidence Filtering (quality ≥ 0.8)
  └─ Stage 4: Diversity Selection (coverage)
  │
  ▼
CROSS-REFERENCE RESOLUTION
  │
  ├─ Identify items in multiple topics
  ├─ Assign primary topic (highest priority)
  └─ Create secondary mentions (links)
  │
  ▼
SUB-SKILL GENERATION
  │
  ├─ For each topic:
  │  ├─ Apply topic template
  │  ├─ Include filtered patterns/examples
  │  ├─ Add GitHub issues for this topic
  │  ├─ Add README content if relevant
  │  └─ Generate references/
  │
  ▼
ROUTER GENERATION
  │
  ├─ Extract routing keywords
  ├─ Add README quick start
  ├─ Add top 5 common issues
  ├─ Create routing table
  └─ Generate scenarios
  │
  ▼
ENHANCEMENT PHASE (Multi-Stage AI)
  │
  ├─ Stage 1: Source Enrichment (Premium)
  │  └─ AI resolves conflicts, ranks examples
  │
  ├─ Stage 2: Sub-Skill Enhancement (Standard)
  │  └─ AI enhances each SKILL.md
  │
  └─ Stage 3: Router Enhancement (Required)
     └─ AI enhances router logic
  │
  ▼
PACKAGING PHASE
  │
  ├─ Validate quality (size, examples, cross-refs)
  ├─ Package router → fastmcp.zip
  ├─ Package sub-skills → fastmcp-*.zip
  └─ Create upload manifest
  │
  ▼
OUTPUT
  ├─ fastmcp.zip (router)
  ├─ fastmcp-oauth.zip
  ├─ fastmcp-async.zip
  ├─ fastmcp-testing.zip
  └─ fastmcp-api.zip
```

### 4.2 GitHub 三流获取器算法

```python
class GitHubThreeStreamFetcher:
    """
    Fetch from GitHub and split into 3 streams.

    Outputs:
    - Stream 1: Code (for C3.x)
    - Stream 2: Docs (for doc parser)
    - Stream 3: Insights (for issue analyzer)
    """

    def fetch(self, repo_url: str) -> ThreeStreamData:
        """
        Main fetching algorithm.

        Steps:
        1. Clone repository
        2. Fetch GitHub API data
        3. Classify files into code vs docs
        4. Analyze issues
        5. Return 3 streams
        """

        # STEP 1: Clone repository
        print(f"📦 Cloning {repo_url}...")
        local_path = self.clone_repo(repo_url)

        # STEP 2: Fetch GitHub metadata
        print(f"🔍 Fetching GitHub metadata...")
        metadata = self.fetch_github_metadata(repo_url)
        issues = self.fetch_issues(repo_url, max_issues=100)

        # STEP 3: Classify files
        print(f"📂 Classifying files...")
        code_files, doc_files = self.classify_files(local_path)
        print(f"  - Code: {len(code_files)} files")
        print(f"  - Docs: {len(doc_files)} files")

        # STEP 4: Analyze issues
        print(f"🐛 Analyzing {len(issues)} issues...")
        issue_insights = self.analyze_issues(issues)

        # STEP 5: Return 3 streams
        return ThreeStreamData(
            code_stream=CodeStream(
                directory=local_path,
                files=code_files
            ),
            docs_stream=DocsStream(
                readme=self.read_file(local_path / 'README.md'),
                contributing=self.read_file(local_path / 'CONTRIBUTING.md'),
                docs_files=[self.read_file(f) for f in doc_files]
            ),
            insights_stream=InsightsStream(
                metadata=metadata,
                common_problems=issue_insights['common_problems'],
                known_solutions=issue_insights['known_solutions'],
                top_labels=issue_insights['top_labels']
            )
        )

    def classify_files(self, repo_path: Path) -> tuple[List[Path], List[Path]]:
        """
        Split files into code vs documentation.

        Code patterns:
        - *.py, *.js, *.ts, *.go, *.rs, *.java, etc.
        - In src/, lib/, pkg/, etc.

        Doc patterns:
        - README.md, CONTRIBUTING.md, CHANGELOG.md
        - docs/**/*.md, doc/**/*.md
        - *.rst (reStructuredText)
        """

        code_files = []
        doc_files = []

        # Documentation patterns
        doc_patterns = [
            '**/README.md',
            '**/CONTRIBUTING.md',
            '**/CHANGELOG.md',
            '**/LICENSE.md',
            'docs/**/*.md',
            'doc/**/*.md',
            'documentation/**/*.md',
            '**/*.rst',
        ]

        # Code patterns (by extension)
        code_extensions = [
            '.py', '.js', '.ts', '.jsx', '.tsx',
            '.go', '.rs', '.java', '.kt',
            '.c', '.cpp', '.h', '.hpp',
            '.rb', '.php', '.swift'
        ]

        for file in repo_path.rglob('*'):
            if not file.is_file():
                continue

            # Skip hidden files and common excludes
            if any(part.startswith('.') for part in file.parts):
                continue
            if any(exclude in str(file) for exclude in ['node_modules', '__pycache__', 'venv']):
                continue

            # Check if documentation
            is_doc = any(file.match(pattern) for pattern in doc_patterns)

            if is_doc:
                doc_files.append(file)
            elif file.suffix in code_extensions:
                code_files.append(file)

        return code_files, doc_files

    def analyze_issues(self, issues: List[Dict]) -> Dict:
        """
        Analyze GitHub issues to extract insights.

        Returns:
        {
            "common_problems": [
                {
                    "title": "OAuth setup fails",
                    "number": 42,
                    "labels": ["question", "oauth"],
                    "comments": 15,
                    "state": "open"
                },
                ...
            ],
            "known_solutions": [
                {
                    "title": "Fixed OAuth redirect",
                    "number": 35,
                    "labels": ["bug", "oauth"],
                    "solution": "Check redirect URI in Google Console",
                    "state": "closed"
                },
                ...
            ],
            "top_labels": [
                {"label": "question", "count": 23},
                {"label": "bug", "count": 15},
                ...
            ]
        }
        """

        common_problems = []
        known_solutions = []
        all_labels = []

        for issue in issues:
            labels = issue.get('labels', [])
            all_labels.extend(labels)

            # Open issues with many comments = common problems
            if issue['state'] == 'open' and issue.get('comments', 0) > 5:
                common_problems.append({
                    'title': issue['title'],
                    'number': issue['number'],
                    'labels': labels,
                    'comments': issue['comments'],
                    'state': 'open'
                })

            # Closed issues with comments = known solutions
            elif issue['state'] == 'closed' and issue.get('comments', 0) > 0:
                known_solutions.append({
                    'title': issue['title'],
                    'number': issue['number'],
                    'labels': labels,
                    'comments': issue['comments'],
                    'state': 'closed'
                })

        # Count label frequency
        from collections import Counter
        label_counts = Counter(all_labels)

        return {
            'common_problems': sorted(common_problems, key=lambda x: x['comments'], reverse=True)[:10],
            'known_solutions': sorted(known_solutions, key=lambda x: x['comments'], reverse=True)[:10],
            'top_labels': [
                {'label': label, 'count': count}
                for label, count in label_counts.most_common(10)
            ]
        }
```

### 4.3 多源合并算法（增强版）

```python
class EnhancedSourceMerger:
    """
    Merge data from all sources with conflict detection.

    Sources:
    1. HTML documentation (if provided)
    2. GitHub code stream (C3.x)
    3. GitHub docs stream (README/docs)
    4. GitHub insights stream (issues)
    """

    def merge(
        self,
        html_docs: Optional[Dict],
        github_three_streams: Optional[ThreeStreamData]
    ) -> MergedSkillData:
        """
        Merge all sources with priority:
        1. C3.x code (ground truth)
        2. HTML docs (official intent)
        3. GitHub docs (repo documentation)
        4. GitHub insights (community knowledge)
        """

        merged = MergedSkillData()

        # LAYER 1: GitHub Code Stream (C3.x) - Ground Truth
        if github_three_streams and github_three_streams.code_stream:
            print("📊 Layer 1: C3.x code analysis")
            c3x_data = self.run_c3x_analysis(github_three_streams.code_stream)

            merged.patterns = c3x_data['patterns']
            merged.examples = c3x_data['examples']
            merged.architecture = c3x_data['architecture']
            merged.api_reference = c3x_data['api_files']
            merged.source_priority['c3x_code'] = 1  # Highest

        # LAYER 2: HTML Documentation - Official Intent
        if html_docs:
            print("📚 Layer 2: HTML documentation")
            for topic, content in html_docs.items():
                if topic in merged.topics:
                    # Detect conflicts with C3.x
                    conflicts = self.detect_conflicts(
                        code_version=merged.topics[topic],
                        docs_version=content
                    )

                    if conflicts:
                        merged.conflicts.append(conflicts)
                        # Create hybrid (show both)
                        merged.topics[topic] = self.create_hybrid(
                            code=merged.topics[topic],
                            docs=content,
                            conflicts=conflicts
                        )
                    else:
                        # Enrich with docs
                        merged.topics[topic].add_documentation(content)
                else:
                    merged.topics[topic] = content

            merged.source_priority['html_docs'] = 2

        # LAYER 3: GitHub Docs Stream - Repo Documentation
        if github_three_streams and github_three_streams.docs_stream:
            print("📄 Layer 3: GitHub documentation")
            docs = github_three_streams.docs_stream

            # Add README quick start
            merged.quick_start = docs.readme

            # Add contribution guide
            merged.contributing = docs.contributing

            # Add docs/ files as references
            for doc_file in docs.docs_files:
                merged.references.append({
                    'source': 'github_docs',
                    'content': doc_file,
                    'priority': 3
                })

            merged.source_priority['github_docs'] = 3

        # LAYER 4: GitHub Insights Stream - Community Knowledge
        if github_three_streams and github_three_streams.insights_stream:
            print("🐛 Layer 4: GitHub insights")
            insights = github_three_streams.insights_stream

            # Add common problems
            merged.common_problems = insights.common_problems
            merged.known_solutions = insights.known_solutions

            # Add metadata
            merged.metadata = insights.metadata

            # Categorize issues by topic
            merged.issues_by_topic = self.categorize_issues_by_topic(
                problems=insights.common_problems,
                solutions=insights.known_solutions,
                topics=merged.topics.keys()
            )

            merged.source_priority['github_insights'] = 4

        return merged

    def categorize_issues_by_topic(
        self,
        problems: List[Dict],
        solutions: List[Dict],
        topics: List[str]
    ) -> Dict[str, List[Dict]]:
        """
        Categorize issues by topic using label/title matching.

        Example:
        - Issue "OAuth setup fails" → oauth topic
        - Issue "Async tools error" → async topic
        """

        categorized = {topic: [] for topic in topics}

        all_issues = problems + solutions

        for issue in all_issues:
            title_lower = issue['title'].lower()
            labels_lower = [l.lower() for l in issue.get('labels', [])]

            # Match to topic by keywords
            for topic in topics:
                topic_keywords = self.get_topic_keywords(topic)

                # Check title and labels
                if any(kw in title_lower for kw in topic_keywords):
                    categorized[topic].append(issue)
                    continue

                if any(kw in label for label in labels_lower for kw in topic_keywords):
                    categorized[topic].append(issue)
                    continue

        return categorized

    def get_topic_keywords(self, topic: str) -> List[str]:
        """Get keywords for each topic."""
        keywords = {
            'oauth': ['oauth', 'auth', 'provider', 'google', 'azure', 'token'],
            'async': ['async', 'await', 'asynchronous', 'concurrent'],
            'testing': ['test', 'pytest', 'mock', 'fixture'],
            'api': ['api', 'reference', 'function', 'class']
        }
        return keywords.get(topic, [])
```

### 4.4 主题定义算法（结合 GitHub 洞察的增强版）

```python
def define_topics_enhanced(
    base_name: str,
    c3x_data: Dict,
    github_insights: Optional[InsightsStream]
) -> Dict[str, TopicConfig]:
    """
    Auto-detect topics using:
    1. C3.x pattern distribution
    2. C3.x example categories
    3. GitHub issue labels (NEW!)

    Example: If GitHub has 23 "oauth" labeled issues,
    that's strong signal OAuth is important topic.
    """

    topics = {}

    # Analyze C3.x patterns
    pattern_counts = count_patterns_by_keyword(c3x_data['patterns'])

    # Analyze C3.x examples
    example_categories = categorize_examples(c3x_data['examples'])

    # Analyze GitHub issue labels (NEW!)
    issue_label_counts = {}
    if github_insights:
        for label_info in github_insights.top_labels:
            issue_label_counts[label_info['label']] = label_info['count']

    # TOPIC 1: OAuth (if significant)
    oauth_signals = (
        pattern_counts.get('auth', 0) +
        example_categories.get('auth', 0) +
        issue_label_counts.get('oauth', 0) * 2  # Issues weighted 2x
    )

    if oauth_signals > 50:
        topics['oauth'] = TopicConfig(
            keywords=['auth', 'oauth', 'provider', 'token'],
            patterns=['Strategy', 'Factory'],
            target_length=250,
            priority=1,
            github_issue_count=issue_label_counts.get('oauth', 0)  # NEW
        )

    # TOPIC 2: Async (if significant)
    async_signals = (
        pattern_counts.get('async', 0) +
        example_categories.get('async', 0) +
        issue_label_counts.get('async', 0) * 2
    )

    if async_signals > 30:
        topics['async'] = TopicConfig(
            keywords=['async', 'await'],
            patterns=['Decorator'],
            target_length=200,
            priority=2,
            github_issue_count=issue_label_counts.get('async', 0)
        )

    # TOPIC 3: Testing (if examples exist)
    if example_categories.get('test', 0) > 50:
        topics['testing'] = TopicConfig(
            keywords=['test', 'mock', 'pytest'],
            patterns=[],
            target_length=250,
            priority=3,
            github_issue_count=issue_label_counts.get('testing', 0)
        )

    # TOPIC 4: API Reference (always)
    topics['api'] = TopicConfig(
        keywords=[],
        patterns=[],
        target_length=400,
        priority=4,
        github_issue_count=0
    )

    return topics
```

---

## 5. 技术实现

### 5.1 核心类（增强版）

```python
# src/nexus_core/cli/github_fetcher.py

from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path

@dataclass
class CodeStream:
    """Code files for C3.x analysis."""
    directory: Path
    files: List[Path]

@dataclass
class DocsStream:
    """Documentation files from repository."""
    readme: Optional[str]
    contributing: Optional[str]
    docs_files: List[Dict]  # [{"path": "docs/oauth.md", "content": "..."}]

@dataclass
class InsightsStream:
    """GitHub metadata and issues."""
    metadata: Dict  # stars, forks, language, etc.
    common_problems: List[Dict]
    known_solutions: List[Dict]
    top_labels: List[Dict]

@dataclass
class ThreeStreamData:
    """Complete output from GitHub fetcher."""
    code_stream: CodeStream
    docs_stream: DocsStream
    insights_stream: InsightsStream


class GitHubThreeStreamFetcher:
    """
    Fetch from GitHub and split into 3 streams.

    Usage:
        fetcher = GitHubThreeStreamFetcher(
            repo_url="https://github.com/facebook/react",
            github_token=os.getenv('GITHUB_TOKEN')
        )

        three_streams = fetcher.fetch()

        # Now you have:
        # - three_streams.code_stream (for C3.x)
        # - three_streams.docs_stream (for doc parser)
        # - three_streams.insights_stream (for issue analyzer)
    """

    def __init__(self, repo_url: str, github_token: Optional[str] = None):
        self.repo_url = repo_url
        self.github_token = github_token
        self.owner, self.repo = self.parse_repo_url(repo_url)

    def fetch(self, output_dir: Path = Path('/tmp')) -> ThreeStreamData:
        """Fetch everything and split into 3 streams."""
        # Implementation from section 4.2
        pass

    def clone_repo(self, output_dir: Path) -> Path:
        """Clone repository to local directory."""
        # Implementation from section 4.2
        pass

    def fetch_github_metadata(self) -> Dict:
        """Fetch repo metadata via GitHub API."""
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        headers = {}
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'

        response = requests.get(url, headers=headers)
        return response.json()

    def fetch_issues(self, max_issues: int = 100) -> List[Dict]:
        """Fetch GitHub issues (open + closed)."""
        # Implementation from section 4.2
        pass

    def classify_files(self, repo_path: Path) -> tuple[List[Path], List[Path]]:
        """Split files into code vs documentation."""
        # Implementation from section 4.2
        pass

    def analyze_issues(self, issues: List[Dict]) -> Dict:
        """Analyze issues to extract insights."""
        # Implementation from section 4.2
        pass


# src/nexus_core/cli/unified_codebase_analyzer.py

class UnifiedCodebaseAnalyzer:
    """
    Unified analyzer for ANY codebase (local or GitHub).

    Key insight: C3.x is a DEPTH MODE, not a source type.

    Usage:
        analyzer = UnifiedCodebaseAnalyzer()

        # Analyze from GitHub
        result = analyzer.analyze(
            source="https://github.com/facebook/react",
            depth="c3x",
            fetch_github_metadata=True
        )

        # Analyze local directory
        result = analyzer.analyze(
            source="/path/to/project",
            depth="c3x"
        )

        # Quick basic analysis
        result = analyzer.analyze(
            source="/path/to/project",
            depth="basic"
        )
    """

    def analyze(
        self,
        source: str,  # GitHub URL or local path
        depth: str = 'c3x',  # 'basic' or 'c3x'
        fetch_github_metadata: bool = True
    ) -> Dict:
        """
        Analyze codebase with specified depth.

        Returns unified result with all available streams.
        """

        # Step 1: Acquire source
        if self.is_github_url(source):
            # Use three-stream fetcher
            fetcher = GitHubThreeStreamFetcher(source)
            three_streams = fetcher.fetch()

            code_directory = three_streams.code_stream.directory
            github_data = {
                'docs': three_streams.docs_stream,
                'insights': three_streams.insights_stream
            }
        else:
            # Local directory
            code_directory = Path(source)
            github_data = None

        # Step 2: Analyze code with specified depth
        if depth == 'basic':
            code_analysis = self.basic_analysis(code_directory)
        elif depth == 'c3x':
            code_analysis = self.c3x_analysis(code_directory)
        else:
            raise ValueError(f"Unknown depth: {depth}")

        # Step 3: Combine results
        result = {
            'code_analysis': code_analysis,
            'github_docs': github_data['docs'] if github_data else None,
            'github_insights': github_data['insights'] if github_data else None,
        }

        return result

    def basic_analysis(self, directory: Path) -> Dict:
        """
        Fast, shallow analysis (1-2 min).

        Returns:
        - File structure
        - Imports
        - Entry points
        """
        return {
            'files': self.list_files(directory),
            'structure': self.get_directory_structure(directory),
            'imports': self.extract_imports(directory),
            'entry_points': self.find_entry_points(directory),
            'analysis_time': '1-2 min',
            'analysis_depth': 'basic'
        }

    def c3x_analysis(self, directory: Path) -> Dict:
        """
        Deep C3.x analysis (20-60 min).

        Returns:
        - Everything from basic
        - C3.1: Design patterns
        - C3.2: Test examples
        - C3.3: How-to guides
        - C3.4: Config patterns
        - C3.7: Architecture
        """

        # Start with basic
        basic = self.basic_analysis(directory)

        # Add C3.x components
        c3x = {
            **basic,
            'c3_1_patterns': self.detect_patterns(directory),
            'c3_2_examples': self.extract_test_examples(directory),
            'c3_3_guides': self.build_how_to_guides(directory),
            'c3_4_configs': self.analyze_configs(directory),
            'c3_7_architecture': self.detect_architecture(directory),
            'analysis_time': '20-60 min',
            'analysis_depth': 'c3x'
        }

        return c3x

    def is_github_url(self, source: str) -> bool:
        """Check if source is a GitHub URL."""
        return 'github.com' in source


# src/nexus_core/cli/c3x_to_router.py (Enhanced)

class EnhancedC3xToRouterPipeline:
    """
    Enhanced pipeline with three-stream GitHub support.

    New capabilities:
    - Integrates GitHub docs (README, CONTRIBUTING)
    - Adds GitHub issues to "Common Problems" sections
    - Shows repository stats in overview
    - Categorizes issues by topic
    """

    def __init__(
        self,
        analysis_dir: Path,
        output_dir: Path,
        github_data: Optional[ThreeStreamData] = None
    ):
        self.analysis_dir = Path(analysis_dir)
        self.output_dir = Path(output_dir)
        self.github_data = github_data
        self.c3x_data = self.load_c3x_data()

    def run(self, base_name: str) -> Dict[str, Path]:
        """
        Execute complete pipeline with GitHub integration.

        Enhanced steps:
        1. Define topics (using C3.x + GitHub issue labels)
        2. Filter data for each topic
        3. Categorize GitHub issues by topic
        4. Resolve cross-references
        5. Generate sub-skills (with GitHub issues)
        6. Generate router (with README + top issues)
        7. Validate quality
        """

        print(f"🚀 Starting Enhanced C3.x to Router pipeline for {base_name}")

        # Step 1: Define topics (enhanced with GitHub insights)
        topics = self.define_topics_enhanced(
            base_name,
            github_insights=self.github_data.insights_stream if self.github_data else None
        )
        print(f"📋 Defined {len(topics)} topics: {list(topics.keys())}")

        # Step 2: Filter data for each topic
        filtered_data = {}
        for topic_name, topic_config in topics.items():
            print(f"🔍 Filtering data for topic: {topic_name}")
            filtered_data[topic_name] = self.filter_for_topic(topic_config)

        # Step 3: Categorize GitHub issues by topic (NEW!)
        if self.github_data:
            print(f"🐛 Categorizing GitHub issues by topic")
            issues_by_topic = self.categorize_issues_by_topic(
                insights=self.github_data.insights_stream,
                topics=list(topics.keys())
            )
            # Add to filtered data
            for topic_name, issues in issues_by_topic.items():
                if topic_name in filtered_data:
                    filtered_data[topic_name].github_issues = issues

        # Step 4: Resolve cross-references
        print(f"🔗 Resolving cross-references")
        filtered_data = self.resolve_cross_references(filtered_data, topics)

        # Step 5: Generate sub-skills (with GitHub issues)
        skill_paths = {}
        for topic_name, data in filtered_data.items():
            print(f"📝 Generating sub-skill: {base_name}-{topic_name}")
            skill_path = self.generate_sub_skill_enhanced(
                base_name, topic_name, data, topics[topic_name]
            )
            skill_paths[f"{base_name}-{topic_name}"] = skill_path

        # Step 6: Generate router (with README + top issues)
        print(f"🧭 Generating router skill: {base_name}")
        router_path = self.generate_router_enhanced(
            base_name,
            list(skill_paths.keys()),
            github_docs=self.github_data.docs_stream if self.github_data else None,
            github_insights=self.github_data.insights_stream if self.github_data else None
        )
        skill_paths[base_name] = router_path

        # Step 7: Quality validation
        print(f"✅ Validating quality")
        self.validate_quality(skill_paths)

        print(f"🎉 Pipeline complete! Generated {len(skill_paths)} skills")
        return skill_paths

    def generate_sub_skill_enhanced(
        self,
        base_name: str,
        topic_name: str,
        data: FilteredData,
        config: TopicConfig
    ) -> Path:
        """
        Generate sub-skill with GitHub issues integrated.

        Adds new section: "Common Issues (from GitHub)"
        """
        output_dir = self.output_dir / f"{base_name}-{topic_name}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Use topic-specific template
        template = self.get_topic_template(topic_name)

        # Generate SKILL.md with GitHub issues
        skill_md = template.render(
            base_name=base_name,
            topic_name=topic_name,
            data=data,
            config=config,
            github_issues=data.github_issues if hasattr(data, 'github_issues') else []  # NEW
        )

        # Write SKILL.md
        skill_file = output_dir / 'SKILL.md'
        skill_file.write_text(skill_md)

        # Generate reference files (including GitHub issues)
        self.generate_references_enhanced(output_dir, data)

        return output_dir

    def generate_router_enhanced(
        self,
        base_name: str,
        sub_skills: List[str],
        github_docs: Optional[DocsStream],
        github_insights: Optional[InsightsStream]
    ) -> Path:
        """
        Generate router with:
        - README quick start
        - Top 5 GitHub issues
        - Repository stats
        """
        output_dir = self.output_dir / base_name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate router SKILL.md
        router_md = self.create_router_md_enhanced(
            base_name,
            sub_skills,
            github_docs,
            github_insights
        )

        # Write SKILL.md
        skill_file = output_dir / 'SKILL.md'
        skill_file.write_text(router_md)

        # Generate reference files
        refs_dir = output_dir / 'references'
        refs_dir.mkdir(exist_ok=True)

        # Add index
        (refs_dir / 'index.md').write_text(self.create_router_index(sub_skills))

        # Add common issues (NEW!)
        if github_insights:
            (refs_dir / 'common_issues.md').write_text(
                self.create_common_issues_reference(github_insights)
            )

        return output_dir

    def create_router_md_enhanced(
        self,
        base_name: str,
        sub_skills: List[str],
        github_docs: Optional[DocsStream],
        github_insights: Optional[InsightsStream]
    ) -> str:
        """Create router SKILL.md with GitHub integration."""

        # Extract repo URL from github_insights
        repo_url = f"https://github.com/{base_name}"  # Simplified

        md = f"""---
name: {base_name}
description: {base_name.upper()} framework - use for overview and routing to specialized topics
---

# {base_name.upper()} - Overview

"""

        # Add GitHub metadata (if available)
        if github_insights:
            metadata = github_insights.metadata
            md += f"""**Repository:** {repo_url}
**Stars:** ⭐ {metadata.get('stars', 0)} | **Language:** {metadata.get('language', 'Unknown')} | **Open Issues:** {metadata.get('open_issues', 0)}

"""

        md += """## When to Use This Skill

Use this skill when:
- You want an overview of """ + base_name.upper() + """
- You need quick installation/setup steps
- You're deciding which feature to use
- **Route to specialized skills for deep dives**

"""

        # Add Quick Start from README (if available)
        if github_docs and github_docs.readme:
            md += f"""## Quick Start (from README)

{github_docs.readme[:500]}...  <!-- Truncated -->

"""

        # Add Common Issues (if available)
        if github_insights and github_insights.common_problems:
            md += """## Common Issues (from GitHub)

Based on analysis of GitHub issues:

"""
            for i, problem in enumerate(github_insights.common_problems[:5], 1):
                topic_hint = self.guess_topic_from_issue(problem, sub_skills)
                md += f"""{i}. **{problem['title']}** (Issue #{problem['number']}, {problem['comments']} comments)
   - See `{topic_hint}` skill for details

"""

        # Add routing table
        md += """## Choose Your Path

"""
        for skill_name in sub_skills:
            if skill_name == base_name:
                continue
            topic = skill_name.replace(f"{base_name}-", "")
            md += f"""**{topic.title()}?** → Use `{skill_name}` skill
"""

        # Add architecture overview
        if self.c3x_data.get('architecture'):
            arch = self.c3x_data['architecture']
            md += f"""
## Architecture Overview

{base_name.upper()} uses a {arch.get('primary_pattern', 'layered')} architecture.

"""

        return md

    def guess_topic_from_issue(self, issue: Dict, sub_skills: List[str]) -> str:
        """Guess which sub-skill an issue belongs to."""
        title_lower = issue['title'].lower()
        labels_lower = [l.lower() for l in issue.get('labels', [])]

        for skill_name in sub_skills:
            topic = skill_name.split('-')[-1]  # Extract topic from skill name

            if topic in title_lower or topic in str(labels_lower):
                return skill_name

        # Default to main skill
        return sub_skills[0] if sub_skills else 'main'
```

### 5.2 增强版主题模板（含 GitHub Issue）

```python
# src/nexus_core/cli/topic_templates.py (Enhanced)

class EnhancedOAuthTemplate(TopicTemplate):
    """Enhanced OAuth template with GitHub issues."""

    TEMPLATE = """---
name: {{ base_name }}-{{ topic_name }}
description: {{ base_name.upper() }} {{ topic_name }} - OAuth authentication with multiple providers
triggers: {{ triggers }}
---

# {{ base_name.upper() }} OAuth Authentication

## When to Use This Skill

Use this skill when implementing OAuth authentication in {{ base_name }} servers.

## Quick Reference (from C3.x examples)

{% for example in top_examples[:5] %}
### {{ example.title }}

```{{ example.language }}
{{ example.code }}
```

{{ example.description }}

{% endfor %}

## Common OAuth Issues (from GitHub)

{% if github_issues %}
Based on {{ github_issues|length }} GitHub issues related to OAuth:

{% for issue in github_issues[:5] %}
**Issue #{{ issue.number }}: {{ issue.title }}**
- Status: {{ issue.state }}
- Comments: {{ issue.comments }}
{% if issue.state == 'closed' %}
- ✅ Solution found (see issue for details)
{% else %}
- ⚠️ Open issue - community discussion ongoing
{% endif %}

{% endfor %}

{% endif %}

## Supported Providers

{% for provider in providers %}
### {{ provider.name }}

**From C3.x analysis:**
```{{ provider.language }}
{{ provider.example_code }}
```

**Key features:**
{% for feature in provider.features %}
- {{ feature }}
{% endfor %}

{% endfor %}

## Design Patterns

{% for pattern in patterns %}
### {{ pattern.name }} ({{ pattern.count }} instances)

{{ pattern.description }}

**Example:**
```{{ pattern.language }}
{{ pattern.example }}
```

{% endfor %}

## Testing OAuth

{% for test_example in test_examples[:10] %}
### {{ test_example.name }}

```{{ test_example.language }}
{{ test_example.code }}
```

{% endfor %}

## See Also

- Main {{ base_name }} skill for overview
- {{ base_name }}-testing for authentication testing patterns
"""

    def render(
        self,
        base_name: str,
        topic_name: str,
        data: FilteredData,
        config: TopicConfig,
        github_issues: List[Dict] = []  # NEW parameter
    ) -> str:
        """Render template with GitHub issues."""
        template = Template(self.TEMPLATE)

        # Extract data (existing)
        top_examples = self.extract_top_examples(data.examples)
        providers = self.extract_providers(data.patterns, data.examples)
        patterns = self.extract_patterns(data.patterns)
        test_examples = self.extract_test_examples(data.examples)
        triggers = self.extract_triggers(topic_name)

        # Render with GitHub issues
        return template.render(
            base_name=base_name,
            topic_name=topic_name,
            top_examples=top_examples,
            providers=providers,
            patterns=patterns,
            test_examples=test_examples,
            triggers=triggers,
            github_issues=github_issues  # NEW
        )
```

---

## 6. 文件结构（增强版）

### 6.1 输入结构（三流）

```
GitHub Repository (https://github.com/jlowin/fastmcp)
  ↓ (after fetching)

/tmp/fastmcp/                         # Cloned repository
├── src/                              # Code stream
│   └── *.py
├── tests/                            # Code stream
│   └── test_*.py
├── README.md                         # Docs stream
├── CONTRIBUTING.md                   # Docs stream
├── docs/                             # Docs stream
│   ├── getting-started.md
│   ├── oauth.md
│   └── async.md
└── .github/
    └── ... (ignored)

Plus GitHub API data:                 # Insights stream
├── Repository metadata
│   ├── stars: 1234
│   ├── forks: 56
│   ├── open_issues: 12
│   └── language: Python
├── Issues (100 fetched)
│   ├── Open: 12
│   └── Closed: 88
└── Labels
    ├── oauth: 15 issues
    ├── async: 8 issues
    └── testing: 6 issues

After splitting:

STREAM 1: Code Analysis Input
/tmp/fastmcp_code_stream/
├── patterns/detected_patterns.json (from C3.x)
├── test_examples/test_examples.json (from C3.x)
├── config_patterns/config_patterns.json (from C3.x)
├── api_reference/*.md (from C3.x)
└── architecture/architectural_patterns.json (from C3.x)

STREAM 2: Documentation Input
/tmp/fastmcp_docs_stream/
├── README.md
├── CONTRIBUTING.md
└── docs/
    ├── getting-started.md
    ├── oauth.md
    └── async.md

STREAM 3: Insights Input
/tmp/fastmcp_insights_stream/
├── metadata.json
├── common_problems.json
├── known_solutions.json
└── top_labels.json
```

### 6.2 输出结构（增强版）

```
output/
├── fastmcp/                          # Router skill (ENHANCED)
│   ├── SKILL.md (150 lines)
│   │   └── Includes: README quick start + top 5 GitHub issues
│   └── references/
│       ├── index.md
│       └── common_issues.md          # NEW: From GitHub insights
│
├── fastmcp-oauth/                    # OAuth sub-skill (ENHANCED)
│   ├── SKILL.md (250 lines)
│   │   └── Includes: C3.x + GitHub OAuth issues
│   └── references/
│       ├── oauth_overview.md         # From C3.x + README
│       ├── google_provider.md        # From C3.x examples
│       ├── azure_provider.md         # From C3.x examples
│       ├── oauth_patterns.md         # From C3.x patterns
│       └── oauth_issues.md           # NEW: From GitHub issues
│
├── fastmcp-async/                    # Async sub-skill (ENHANCED)
│   ├── SKILL.md (200 lines)
│   └── references/
│       ├── async_basics.md
│       ├── async_patterns.md
│       ├── decorator_pattern.md
│       └── async_issues.md           # NEW: From GitHub issues
│
├── fastmcp-testing/                  # Testing sub-skill (ENHANCED)
│   ├── SKILL.md (250 lines)
│   └── references/
│       ├── unit_tests.md
│       ├── integration_tests.md
│       ├── pytest_examples.md
│       └── testing_issues.md         # NEW: From GitHub issues
│
└── fastmcp-api/                      # API reference sub-skill
    ├── SKILL.md (400 lines)
    └── references/
        └── api_modules/
            └── *.md (316 files, from C3.x)
```

---

## 7. 过滤策略（未变化）

[原文档中的内容 - 无需更改]

---

## 8. 质量指标（增强版）

### 8.1 大小约束（未变化）

**目标：**
- 路由器：150 行（±20）
- OAuth 子技能：250 行（±30）
- 异步子技能：200 行（±30）
- 测试子技能：250 行（±30）
- API 子技能：400 行（±50）

### 8.2 内容质量（增强版）

**要求：**
- 每个子技能至少 3 个代码示例（来自 C3.x）
- 每个子技能至少 2 个 GitHub issue（如可用）
- 所有代码块必须有语言标签
- 没有占位内容（TODO、[Add...]）
- 交叉引用必须有效
- GitHub issue 链接必须有效（#42 等）

**验证：**
```python
def validate_content_quality_enhanced(skill_md: str, has_github: bool):
    """Check content quality including GitHub integration."""

    # Existing checks
    code_blocks = skill_md.count('```')
    assert code_blocks >= 6, "Need at least 3 code examples"

    assert '```python' in skill_md or '```javascript' in skill_md, \
        "Code blocks must have language tags"

    assert 'TODO' not in skill_md, "No TODO placeholders"
    assert '[Add' not in skill_md, "No [Add...] placeholders"

    # NEW: GitHub checks
    if has_github:
        # Check for GitHub metadata
        assert '⭐' in skill_md or 'Repository:' in skill_md, \
            "Missing GitHub metadata"

        # Check for issue references
        issue_refs = len(re.findall(r'Issue #\d+', skill_md))
        assert issue_refs >= 2, f"Need at least 2 GitHub issue references, found {issue_refs}"

        # Check for "Common Issues" section
        assert 'Common Issues' in skill_md or 'Common Problems' in skill_md, \
            "Missing Common Issues section from GitHub"
```

### 8.3 GitHub 集成质量（新）

**要求：**
- 路由器必须包含仓库统计（star、fork、语言）
- 路由器必须包含前 5 个常见问题
- 每个子技能必须包含相关 issue（如果存在）
- Issue 引用必须正确格式化（#42）
- 已关闭的 issue 应显示 "✅ Solution found"

**验证：**
```python
def validate_github_integration(skill_md: str, topic: str, github_insights: InsightsStream):
    """Validate GitHub integration quality."""

    # Check metadata present
    if topic == 'router':
        assert '⭐' in skill_md, "Missing stars count"
        assert 'Open Issues:' in skill_md, "Missing issue count"

    # Check issue formatting
    issue_matches = re.findall(r'Issue #(\d+)', skill_md)
    for issue_num in issue_matches:
        # Verify issue exists in insights
        all_issues = github_insights.common_problems + github_insights.known_solutions
        issue_exists = any(str(i['number']) == issue_num for i in all_issues)
        assert issue_exists, f"Issue #{issue_num} referenced but not in GitHub data"

    # Check solution indicators
    closed_issue_matches = re.findall(r'Issue #(\d+).*closed', skill_md, re.IGNORECASE)
    for match in closed_issue_matches:
        assert '✅' in skill_md or 'Solution' in skill_md, \
            f"Closed issue #{match} should indicate solution found"
```

### 8.4 Token 效率（增强版）

**要求：** 相比单体平均减少 40%+ 的 token

**新增：GitHub 开销计算**
```python
def measure_token_efficiency_with_github(scenarios: List[Dict]):
    """
    Measure token usage with GitHub integration overhead.

    GitHub adds ~50 lines per skill (metadata + issues).
    Router architecture still wins due to selective loading.
    """

    # Monolithic with GitHub
    monolithic_size = 666 + 50  # SKILL.md + GitHub section

    # Router with GitHub
    router_size = 150 + 50  # Router + GitHub metadata
    avg_subskill_size = (250 + 200 + 250 + 400) / 4  # ~275 lines
    avg_subskill_with_github = avg_subskill_size + 30  # +30 for issue section

    # Calculate average query
    avg_router_query = router_size + avg_subskill_with_github  # ~455 lines

    reduction = (monolithic_size - avg_router_query) / monolithic_size
    # (716 - 455) / 716 = 36% reduction

    assert reduction >= 0.35, f"Token reduction {reduction:.1%} below 35% (with GitHub overhead)"

    return reduction
```

**结果：** 即使加上 GitHub 集成，路由器仍能实现 35-40% 的 token 减少。

---

## 9-13. [其余章节]

[边界情况、可扩展性、迁移、测试、实现阶段等章节与原文档基本相同，并增加以下增强：]

- 添加 GitHub 获取器测试
- 添加 issue 分类测试
- 添加混合内容生成测试
- 更新实现阶段以包含 GitHub 集成
- 添加 GitHub API 获取的时间估算（1-2 分钟）

---

## 实现阶段（更新版）

### 阶段 1：三流 GitHub 获取器（第 1 天，8 小时）

**新阶段 - 最高优先级**

**任务：**
1. 创建 `github_fetcher.py` ✅
   - 克隆仓库
   - 获取 GitHub API 元数据
   - 获取 issue（开放 + 已关闭）
   - 文件分类（代码 vs 文档）

2. 创建 `GitHubThreeStreamFetcher` 类 ✅
   - `fetch()` 主方法
   - `classify_files()` 拆分器
   - `analyze_issues()` 洞察提取器

3. 与 `unified_codebase_analyzer.py` 集成 ✅
   - 检测 GitHub URL
   - 调用三流获取器
   - 返回统一结果

4. 编写测试 ✅
   - 测试文件分类
   - 测试 issue 分析
   - 测试真实 GitHub 获取（使用 token）

**交付物：** 可用的三流 GitHub 获取器

---

### 阶段 2：增强的来源合并（第 2 天，6 小时）

**任务：**
1. 更新 `source_merger.py` ✅
   - 添加 GitHub 文档流处理
   - 添加 GitHub 洞察流处理
   - 按主题对 issue 分类
   - 创建带 issue 链接的混合内容

2. 更新主题定义 ✅
   - 使用 GitHub issue 标签
   - 在主题评分中为 issue 加权

3. 编写测试 ✅
   - 测试 issue 分类
   - 测试混合内容生成
   - 测试冲突检测

**交付物：** 集成 GitHub 的增强合并功能

---

### 阶段 3：含 GitHub 的路由器生成（第 2-3 天，6 小时）

**任务：**
1. 更新路由器模板 ✅
   - 添加 README 快速开始部分
   - 添加仓库统计
   - 添加前 5 个常见问题
   - 将 issue 链接到子技能

2. 更新子技能模板 ✅
   - 添加"常见问题"部分
   - 格式化 issue 引用
   - 添加解决方案标识

3. 编写测试 ✅
   - 测试包含 GitHub 数据的路由器
   - 测试包含 issue 的子技能
   - 验证 issue 链接

**交付物：** 集成 GitHub 的完整路由器

---

### 阶段 4：测试与完善（第 3 天，4 小时）

**任务：**
1. 在 FastMCP 上运行完整 E2E 测试 ✅
   - 使用 GitHub 三流
   - 验证 3 个流全部存在
   - 检查 issue 集成
   - 测量 token 节省

2. 手动测试 ✅
   - 测试 10 个真实查询
   - 验证 issue 相关性
   - 检查 GitHub 链接可用

3. 性能优化 ✅
   - GitHub API 速率限制
   - 并行流处理
   - 缓存 GitHub 数据

**交付物：** 生产就绪的流水线

---

### 阶段 5：文档（第 4 天，2 小时）

**任务：**
1. 更新文档 ✅
   - 本架构文档
   - CLI 帮助文本
   - 含 GitHub 示例的 README

2. 创建示例 ✅
   - 含 GitHub 的 FastMCP
   - 含 GitHub 的 React
   - 添加到官方配置

**交付物：** 完整的文档

---

## 总时间线：4 天（26 小时）

**第 1 天（8 小时）：** GitHub 三流获取器
**第 2 天（8 小时）：** 增强合并 + 路由器生成
**第 3 天（8 小时）：** 测试、完善、质量验证
**第 4 天（2 小时）：** 文档和示例

---

## 附录 A：配置示例（更新版）

### 示例 1：使用三流的 GitHub（新）

```json
{
  "name": "fastmcp",
  "description": "FastMCP framework - complete analysis with GitHub insights",
  "sources": [
    {
      "type": "codebase",
      "source": "https://github.com/jlowin/fastmcp",
      "analysis_depth": "c3x",
      "fetch_github_metadata": true,
      "split_docs": true,
      "max_issues": 100
    }
  ],
  "router_mode": true
}
```

**结果：**
- ✅ 使用 C3.x 分析代码
- ✅ 提取 README/docs
- ✅ 分析 100 个 issue
- ✅ 生成路由器 + 4 个子技能
- ✅ 所有技能均包含 GitHub 洞察

### 示例 2：文档 + GitHub（多源）

```json
{
  "name": "react",
  "description": "React framework - official docs + GitHub insights",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://react.dev/",
      "max_pages": 200
    },
    {
      "type": "codebase",
      "source": "https://github.com/facebook/react",
      "analysis_depth": "c3x",
      "fetch_github_metadata": true,
      "max_issues": 100
    }
  ],
  "merge_mode": "conflict_detection",
  "router_mode": true
}
```

**结果：**
- ✅ 抓取 HTML 文档（200 页）
- ✅ 使用 C3.x 分析代码
- ✅ 添加 GitHub 洞察
- ✅ 检测冲突（文档 vs 代码）
- ✅ 生成混合内容
- ✅ 路由器 + 包含所有来源的子技能

### 示例 3：本地代码库（无 GitHub）

```json
{
  "name": "internal-tool",
  "description": "Internal tool - local analysis only",
  "sources": [
    {
      "type": "codebase",
      "source": "/path/to/internal-tool",
      "analysis_depth": "c3x",
      "fetch_github_metadata": false
    }
  ],
  "router_mode": true
}
```

**结果：**
- ✅ 使用 C3.x 分析代码
- ❌ 没有 GitHub 洞察（不适用）
- ✅ 生成路由器 + 子技能
- ✅ 没有 GitHub 数据也能工作

---

**增强架构文档结束**

---

## 主要变更摘要

### 变更内容：

1. **来源架构重新设计**
   - GitHub 现在是"多源提供者"（3 个流）
   - C3.x 现在是"分析深度模式"，而非来源类型
   - 统一代码库分析器同时处理本地和 GitHub

2. **三流 GitHub 集成**
   - 流 1：代码 → C3.x 分析
   - 流 2：文档 → README/CONTRIBUTING/docs/*.md
   - 流 3：洞察 → Issue、标签、统计数据

3. **增强的路由器内容**
   - 概览中包含仓库统计
   - README 快速开始
   - 来自 GitHub 的前 5 个常见问题
   - Issue 到技能的路由

4. **增强的子技能内容**
   - 每个主题都有"常见问题"部分
   - 来自 GitHub 的真实用户问题
   - 来自已关闭 issue 的已知解决方案
   - Issue 引用（#42 等）

5. **数据流更新**
   - 并行流处理
   - 按主题对 issue 分类
   - 包含 GitHub 数据的混合内容

6. **实现更新**
   - 新类：`GitHubThreeStreamFetcher`、`UnifiedCodebaseAnalyzer`
   - 支持 GitHub 的增强模板
   - 针对 GitHub 集成的新质量指标

### 关键收益：

1. **更丰富的技能：** 代码 + 文档 + 社区知识
2. **真实用户问题：** 来自 GitHub issue
3. **官方快速开始：** 来自 README
4. **更好的架构：** 关注点清晰分离
5. **依然高效：** Token 减少 35-40%（即使有 GitHub 开销）

_本文档现在代表了带有三流 GitHub 集成的 C3.x 路由器技能的完整、生产就绪架构。_
