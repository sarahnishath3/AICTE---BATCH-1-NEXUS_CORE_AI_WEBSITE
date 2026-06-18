# Integration Guide Templates

**Purpose:** Reusable templates for creating integration guides with other tools
**Date:** February 2, 2026

---

## 📋 Integration Guide Template

Use this template for each new tool integration guide.

```markdown
# Using Nexus Core with [Tool Name]

**Last Updated:** [Date]
**Status:** Production Ready
**Difficulty:** Easy ⭐ | Medium ⭐⭐ | Advanced ⭐⭐⭐

---

## 🎯 The Problem

[Tool Name] is excellent for [what it does], but hits limitations when working with complex [frameworks/libraries/codebases]:

- **Context Window Limits** - Can't load complete framework documentation
- **Incomplete Knowledge** - Missing [specific aspect]
- **Quality Issues** - [Specific problem with current approach]

**Example:**
> "When using [Tool] with React, you might get suggestions that miss [specific React pattern] because the complete documentation exceeds the context window."

---

## ✨ The Solution

Use Nexus Core as **essential preparation step** before [Tool Name]:

1. **Generate comprehensive skills** from framework documentation + GitHub repos
2. **Solve context limitations** with smart organization and router skills
3. **Get better results** from [Tool] with complete framework knowledge

**Result:**
[Tool Name] now has access to complete, structured framework knowledge without context limits.

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- [Tool Name] installed and configured
- Python 3.10+ (for Nexus Core)
- [Any tool-specific requirements]

### Installation

```bash
# Install Nexus Core
pip install nexus-core

# Verify installation
nexus-core --version
```

### Generate Your First Skill

```bash
# Example: React framework skill
nexus-core create --config configs/react.json

# OR use GitHub repo
nexus-core create  facebook/react --name react-skill

# Enhance quality (optional, recommended)
nexus-core enhance output/react/ --mode LOCAL
```

### Use with [Tool Name]

[Tool-specific steps for loading/using the skill]

**Example for MCP-compatible tools:**
```json
{
  "mcpServers": {
    "nexus-core": {
      "command": "nexus-core-mcp",
      "args": []
    }
  }
}
```

---

## 📖 Detailed Setup Guide

### Step 1: Install and Configure Nexus Core

[Detailed installation steps with troubleshooting]

### Step 2: Choose Your Framework/Library

Popular frameworks with preset configs:
- React: `configs/react.json`
- Vue: `configs/vue.json`
- Django: `configs/django.json`
- FastAPI: `configs/fastapi.json`
- [List more]

### Step 3: Generate Skills

**Option A: Use Preset Config (Fastest)**
```bash
nexus-core create --config configs/[framework].json
```

**Option B: From GitHub Repo (Most Comprehensive)**
```bash
nexus-core create  owner/repo --name skill-name
```

**Option C: Unified (Docs + Code + PDF)**
```bash
nexus-core create --config configs/[framework]_unified.json
```

### Step 4: Enhance Quality (Optional but Recommended)

```bash
# Free enhancement using LOCAL mode
nexus-core enhance output/[skill-name]/ --mode LOCAL

# Or API mode (faster, costs ~$0.20)
export ANTHROPIC_API_KEY=sk-ant-...
nexus-core enhance output/[skill-name]/
```

### Step 5: Integrate with [Tool Name]

[Detailed integration steps specific to the tool]

---

## 🎨 Advanced Usage

### Router Skills for Large Frameworks

If your framework documentation is large (40K+ pages):

```bash
# Generate router skill to split documentation
nexus-core generate-router output/[skill-name]/

# Creates:
# - Main router (lightweight, <5K tokens)
# - Topic-specific skills (components, API, hooks, etc.)
```

### Multi-Platform Export

Export skills for multiple AI platforms:

```bash
# Claude AI (default)
nexus-core package output/[skill-name]/

# Google Gemini
nexus-core package output/[skill-name]/ --target gemini

# OpenAI ChatGPT
nexus-core package output/[skill-name]/ --target openai
```

### CI/CD Integration

Auto-generate skills when documentation updates:

```yaml
# .github/workflows/skills.yml
name: Update Skills
on:
  push:
    paths: ['docs/**']
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: nexus-core/action@v1
        with:
          source: github
          auto_upload: true
```

---

## 💡 Best Practices

### 1. Start Small
Begin with one framework you use frequently. See the improvement before expanding.

### 2. Use Enhancement
The LOCAL mode enhancement is free and significantly improves quality (2-3/10 → 8-9/10).

### 3. Update Regularly
Re-generate skills when frameworks release major updates:
```bash
# Quick update (uses cache)
nexus-core create --config configs/react.json --skip-scrape=false
```

### 4. Combine Multiple Sources
For production code, use unified scraping:
```json
{
  "name": "production-framework",
  "sources": [
    {"type": "documentation", "url": "..."},
    {"type": "github", "repo": "..."},
    {"type": "pdf", "path": "internal-docs.pdf"}
  ]
}
```

---

## 🔥 Real-World Examples

### Example 1: React Development with [Tool]

**Before Nexus Core:**
- [Tool] suggests outdated patterns
- Missing React 18 features
- Incomplete hook documentation

**After Nexus Core:**
```bash
nexus-core create  facebook/react --name react-skill
nexus-core enhance output/react-skill/ --mode LOCAL
```

**Result:**
- Complete React 18+ knowledge
- Current best practices
- All hooks documented with examples

### Example 2: Internal Framework Documentation

**Challenge:** Company has internal framework with custom docs

**Solution:**
```bash
# Scrape internal docs
nexus-core create --config configs/internal-framework.json

# Add code examples from repo
nexus-core create  company/internal-framework

# Merge both sources
nexus-core merge-sources output/internal-docs/ output/internal-framework/
```

**Result:** Complete internal knowledge base for [Tool]

### Example 3: Multi-Framework Project

**Challenge:** Project uses React + FastAPI + PostgreSQL

**Solution:**
```bash
# Generate skill for each
nexus-core create --config configs/react.json
nexus-core create --config configs/fastapi.json
nexus-core create --config configs/postgresql.json

# [Tool] now has complete knowledge of your stack
```

---

## 🐛 Troubleshooting

### Issue: [Common problem 1]
**Solution:** [How to fix]

### Issue: [Common problem 2]
**Solution:** [How to fix]

### Issue: Skill too large for [Tool]
**Solution:** Use router skills:
```bash
nexus-core generate-router output/[skill-name]/
```

---

## 📊 Before vs After Comparison

| Aspect | Before Nexus Core | After Nexus Core |
|--------|---------------------|---------------------|
| **Context Coverage** | 20-30% of framework | 95-100% of framework |
| **Code Quality** | Generic suggestions | Framework-specific patterns |
| **Documentation** | Fragmented | Complete and organized |
| **Examples** | Limited | Rich, real-world examples |
| **Best Practices** | Hit or miss | Always current |

---

## 🤝 Community & Support

- **Questions:** [GitHub Discussions](https://github.com/yusufkaraaslan/Nexus_Core/discussions)
- **Issues:** [GitHub Issues](https://github.com/yusufkaraaslan/Nexus_Core/issues)
- **Documentation:** [https://nexuscoreweb.com/](https://nexuscoreweb.com/)
- **Twitter:** [@_yUSyUS_](https://x.com/_yUSyUS_)

---

## 📚 Related Guides

- [MCP Setup Guide](../features/MCP_SETUP.md)
- [Enhancement Modes](../features/ENHANCEMENT_MODES.md)
- [Unified Scraping](../features/UNIFIED_SCRAPING.md)
- [Router Skills](../features/ROUTER_SKILLS.md)

---

**Last Updated:** [Date]
**Tested With:** [Tool Name] v[version]
**Nexus Core Version:** v2.8.0+
```

---

## 🎯 Case Study Template

Use this template for detailed case studies.

```markdown
# Case Study: [Tool/Company] + Nexus Core

**Company/Project:** [Name]
**Tool:** [Tool they use]
**Date:** [Date]
**Industry:** [Industry]

---

## 📋 Executive Summary

[2-3 paragraphs summarizing the case]

**Key Results:**
- [Metric 1]: X% improvement
- [Metric 2]: Y hours saved
- [Metric 3]: Z quality increase

---

## 🎯 The Challenge

### Background
[Describe the company/project and their situation]

### Specific Problems
1. **[Problem 1]:** [Description]
2. **[Problem 2]:** [Description]
3. **[Problem 3]:** [Description]

### Why It Mattered
[Impact of these problems on their workflow/business]

---

## ✨ The Solution

### Why Nexus Core
[Why they chose Nexus Core over alternatives]

### Implementation
[How they implemented it - step by step]

```bash
# Commands they used
[actual commands]
```

### Integration
[How they integrated with their existing tools/workflow]

---

## 📊 Results

### Quantitative Results
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [Metric 1] | X | Y | +Z% |
| [Metric 2] | X | Y | +Z% |
| [Metric 3] | X | Y | +Z% |

### Qualitative Results
- **[Aspect 1]:** [Description of improvement]
- **[Aspect 2]:** [Description of improvement]
- **[Aspect 3]:** [Description of improvement]

### Team Feedback
> "[Quote from team member]"
> — [Name], [Role]

---

## 🔍 Technical Details

### Architecture
[How they structured their skills/workflow]

### Workflow
```
Step 1: [Description]
  ↓
Step 2: [Description]
  ↓
Step 3: [Description]
```

### Best Practices They Discovered
1. [Practice 1]
2. [Practice 2]
3. [Practice 3]

---

## 💡 Lessons Learned

### What Worked Well
- [Lesson 1]
- [Lesson 2]
- [Lesson 3]

### What Could Be Improved
- [Learning 1]
- [Learning 2]

### Advice for Others
> "[Key advice for similar situations]"

---

## 🚀 Future Plans

[What they plan to do next with Nexus Core]

---

## 📞 Contact

- **Company:** [Link]
- **Tool Integration:** [Link to their integration]
- **Testimonial:** [Permission to quote?]

---

**Last Updated:** [Date]
**Status:** [Active/Reference]
**Industry:** [Industry]
```

---

## 📧 Outreach Email Template

Use this template for reaching out to tool maintainers.

```markdown
Subject: Partnership Opportunity - Nexus Core + [Tool Name]

Hi [Maintainer Name],

I'm [Your Name] from Nexus Core - we help developers convert documentation into AI-ready skills for platforms like Claude, Gemini, and ChatGPT.

**Why I'm Reaching Out:**

I noticed [Tool Name] helps developers with [what tool does], and we've built something complementary that solves a common pain point your users face: [specific problem like context limits].

**The Integration:**

We've created a comprehensive integration guide showing how [Tool Name] users can:
1. [Benefit 1]
2. [Benefit 2]
3. [Benefit 3]

**Example:**
[Concrete example with before/after]

**What We're Offering:**
- ✅ Complete integration guide (already written): [link]
- ✅ Technical support for your users
- ✅ Cross-promotion in our docs (24K+ GitHub views/month)
- ✅ Case study highlighting [Tool Name] (if interested)

**What We're Asking:**
- Optional mention in your docs/blog
- Feedback on integration UX
- [Any specific ask]

**See It In Action:**
[Link to integration guide]

Would you be open to a 15-minute call to discuss?

Best regards,
[Your Name]
[Contact info]

---

P.S. We already have a working integration - just wanted to make sure we're representing [Tool] accurately and see if you'd like to collaborate!
```

---

## 🐦 Social Media Post Templates

### Twitter/X Thread Template

```markdown
🚀 New: Using Nexus Core with [Tool Name]

[Tool] is amazing for [what it does], but hits limits with complex frameworks.

Here's how we solved it: 🧵

1/ The Problem
[Tool] can't load complete docs for frameworks like React/Vue/Django due to context limits.

Result: Incomplete suggestions, outdated patterns, missing features.

2/ The Solution
Generate comprehensive skills BEFORE using [Tool]:

```bash
nexus-core create  facebook/react
nexus-core enhance output/react/ --mode LOCAL
```

3/ The Result
✅ Complete framework knowledge
✅ No context limits
✅ Better code suggestions
✅ Current best practices

Before: 20-30% coverage
After: 95-100% coverage

4/ Why It Works
Nexus Core:
- Scrapes docs + GitHub repos
- Organizes into structured skills
- Handles large docs with router skills
- Free enhancement with LOCAL mode

5/ Try It
Full guide: [link]
5-minute setup
Works with any framework

What framework should we add next? 👇

#[Tool]  #AI  #DeveloperTools  #[Framework]
```

### Reddit Post Template

```markdown
**Title:** How I gave [Tool] complete [Framework] knowledge (no context limits)

**Body:**

I've been using [Tool] for [time period] and love it, but always hit context window limits with complex frameworks like [Framework].

**The Problem:**
- Can't load complete documentation
- Missing [Framework version] features
- Suggestions sometimes outdated

**The Solution I Found:**
I started using Nexus Core to generate comprehensive skills before using [Tool]. It:
1. Scrapes official docs + GitHub repos
2. Extracts real examples from tests (C3.x analysis)
3. Organizes everything intelligently
4. Handles large docs with router skills

**The Setup (5 minutes):**
```bash
pip install nexus-core
nexus-core create  [org]/[framework]
nexus-core enhance output/[framework]/ --mode LOCAL
```

**The Results:**
- Before: 20-30% framework coverage
- After: 95-100% coverage
- Code suggestions are way more accurate
- No more context window errors

**Example:**
[Concrete before/after example]

**Full Guide:**
[Link to integration guide]

Happy to answer questions!

**Edit:** Wow, thanks for the gold! For those asking about [common question], see my comment below 👇
```

---

## 📚 Related Documents

- [Integration Strategy](./INTEGRATION_STRATEGY.md)
- [DeepWiki Analysis](./DEEPWIKI_ANALYSIS.md)
- [Outreach Scripts](./OUTREACH_SCRIPTS.md)

---

**Last Updated:** February 2, 2026
**Usage:** Copy templates and customize for each integration
