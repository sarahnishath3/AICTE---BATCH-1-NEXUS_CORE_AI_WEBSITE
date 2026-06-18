# Bulletproof Quick Start Guide

**Target Audience:** Complete beginners | Never used Python/git before? Start here!

**Time:** 15-30 minutes total (including all installations)

**Result:** Working Skill Seeker installation + your first Claude skill created

---

## 📋 What You'll Need

Before starting, you need:
- A computer (macOS, Linux, or Windows with WSL)
- Internet connection
- 30 minutes of time

That's it! We'll install everything else together.

---

## Step 1: Install Python (5 minutes)

### Check if You Already Have Python

Open Terminal (macOS/Linux) or Command Prompt (Windows) and type:

```bash
python3 --version
```

**✅ If you see:** `Python 3.10.x` or `Python 3.11.x` or higher → **Skip to Step 2!**

**❌ If you see:** `command not found` or version less than 3.10 → **Continue below**

### Install Python

#### macOS:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Verify:**
```bash
python3 --version
# Should show: Python 3.11.x or similar
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Verify:**
```bash
python3 --version
pip3 --version
```

#### Windows:
1. Download Python from: https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Open Command Prompt and verify:
```bash
python --version
```

**✅ Success looks like:**
```
Python 3.11.5
```

---

## Step 2: Install Git (3 minutes)

### Check if You Have Git

```bash
git --version
```

**✅ If you see:** `git version 2.x.x` → **Skip to Step 3!**

**❌ If not installed:**

#### macOS:
```bash
brew install git
```

#### Linux:
```bash
sudo apt install git
```

#### Windows:
Download from: https://git-scm.com/download/win

**Verify:**
```bash
git --version
# Should show: git version 2.x.x
```

---

## Step 3: Get Skill Seeker (2 minutes)

### Choose Where to Put It

Pick a location for the project. Good choices:
- macOS/Linux: `~/Projects/` or `~/Documents/`
  - Note: `~` means your home directory (`$HOME` or `/Users/yourname` on macOS, `/home/yourname` on Linux)
- Windows: `C:\Users\YourName\Projects\`

### Clone the Repository

```bash
# Create Projects directory (if it doesn't exist)
mkdir -p ~/Projects
cd ~/Projects

# Clone Skill Seeker
git clone https://github.com/yusufkaraaslan/Nexus_Core.git

# Enter the directory
cd Nexus_Core
```

**✅ Success looks like:**
```
Cloning into 'Nexus_Core'...
remote: Enumerating objects: 245, done.
remote: Counting objects: 100% (245/245), done.
```

**Verify you're in the right place:**
```bash
pwd
# Should show something like:
#   macOS: /Users/yourname/Projects/Nexus_Core
#   Linux: /home/yourname/Projects/Nexus_Core
# (Replace 'yourname' with YOUR actual username)

ls
# Should show: README.md, cli/, mcp/, configs/, etc.
```

**❌ If `git clone` fails:**
```bash
# Check internet connection
ping google.com

# Or download ZIP manually:
# https://github.com/yusufkaraaslan/Nexus_Core/archive/refs/heads/main.zip
# Then unzip and cd into it
```

---

## Step 4: Setup Virtual Environment & Install Nexus Core (3 minutes)

A virtual environment keeps Skill Seeker's dependencies isolated and prevents conflicts.

```bash
# Make sure you're in the Nexus_Core directory
cd ~/Projects/Nexus_Core  # ~ means your home directory ($HOME)
                             # Adjust if you chose a different location

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# Windows users: venv\Scripts\activate
```

**✅ Success looks like:**
```
(venv) username@computer Nexus_Core %
```
Notice `(venv)` appears in your prompt - this means the virtual environment is active!

```bash
# Now install Nexus Core package (this installs all dependencies automatically)
pip install -e .
```

**✅ Success looks like:**
```
Successfully installed nexus-core-2.7.4 requests-2.32.5 beautifulsoup4-4.14.2 anthropic-0.76.0 ...
Obtaining file:///path/to/Nexus_Core
Installing collected packages: nexus-core
Successfully installed nexus-core
```

**What just happened?**
- `pip install -e .` installs the package in "editable" mode
- The `.` means "current directory" (where pyproject.toml is)
- This automatically installs ALL required dependencies
- This registers the `nexus-core` command so you can use it from anywhere
- The `-e` flag means changes to the code take effect immediately (useful for development)

**Important Notes:**
- **Every time** you open a new terminal to use Skill Seeker, run `source venv/bin/activate` first (Windows: `venv\Scripts\activate`)
- You'll know it's active when you see `(venv)` in your terminal prompt
- To deactivate later: just type `deactivate`

**❌ If python3 not found:**
```bash
# Try without the 3
python -m venv venv
```

**❌ If permission denied:**
```bash
# Virtual environment approach doesn't need sudo - you might have the wrong path
# Make sure you're in the Nexus_Core directory:
pwd
# Should show something like:
#   macOS: /Users/yourname/Projects/Nexus_Core
#   Linux: /home/yourname/Projects/Nexus_Core
# (Replace 'yourname' with YOUR actual username)
```

**❌ If "pip: command not found":**
```bash
# Try with python -m pip instead
python3 -m pip install -e .
```

---

## Step 5: Test Your Installation (1 minute)

Let's make sure everything works:

```bash
# Test the CLI is installed correctly
nexus-core create --help
```

**✅ Success looks like:**
```
usage: nexus-core create [-h] ...
```

**❌ If you see "command not found":**
```bash
# Ensure the package is installed
pip install -e .

# Verify installation
nexus-core --version
```

---

## Step 6: Create Your First Skill! (5-10 minutes)

Let's create a simple skill using a preset configuration.

### Option A: Small Test (Recommended First Time)

```bash
# Create a config for a small site first
cat > configs/test.json << 'EOF'
{
  "name": "test-skill",
  "description": "Test skill creation",
  "base_url": "https://tailwindcss.com/docs/installation",
  "selectors": {
    "main_content": "#content-wrapper",
    "title": "h1, h2, h3",
    "code_blocks": "pre code"
  },
  "max_pages": 5,
  "rate_limit": 0.5
}
EOF

# Run the scraper
nexus-core create --config configs/test.json
```

**Note for Windows users:** The `cat > file << 'EOF'` syntax doesn't work in PowerShell. Instead, create the file manually:

```powershell
# In PowerShell, create configs/test.json with this content:
@"
{
  "name": "test-skill",
  "description": "Test skill creation",
  "base_url": "https://tailwindcss.com/docs/installation",
  "selectors": {
    "main_content": "#content-wrapper",
    "title": "h1, h2, h3",
    "code_blocks": "pre code"
  },
  "max_pages": 5,
  "rate_limit": 0.5
}
"@ | Out-File -FilePath configs/test.json -Encoding utf8

# Then run the scraper
nexus-core create --config configs/test.json
```

**What happens:**
1. Scrapes 5 pages from Tailwind CSS docs
2. Creates `output/test-skill/` directory
3. Generates SKILL.md and reference files

**⏱️ Time:** ~30 seconds

**✅ Success looks like:**
```
Scraping: https://tailwindcss.com/docs/installation
Page 1/5: Installation
Page 2/5: Editor Setup
...
✅ Skill created at: output/test-skill/
```

### Option B: Full Example (React Docs)

```bash
# Use the React preset
nexus-core create --config configs/react.json --max-pages 50
```

**⏱️ Time:** ~5 minutes

**What you get:**
- `output/react/SKILL.md` - Main skill file
- `output/react/references/` - Organized documentation

### Verify It Worked

```bash
# Check the output
ls output/test-skill/
# Should show: SKILL.md, references/, scripts/, assets/

# Look at the generated skill
head output/test-skill/SKILL.md
```

---

## Step 7: Package for Claude (30 seconds)

```bash
# Package the skill
nexus-core package output/test-skill/
```

**✅ Success looks like:**
```
✅ Skill packaged successfully!
📦 Created: output/test-skill.zip
📏 Size: 45.2 KB

Ready to upload to Claude AI!
```

**Now you have:** `output/test-skill.zip` ready to upload to Claude!

---

## Step 8: Upload to Claude (2 minutes)

1. Go to https://claude.ai
2. Click your profile → Settings
3. Click "Knowledge" or "Skills"
4. Click "Upload Skill"
5. Select `output/test-skill.zip`
6. Done! Claude can now use this skill

---

## 🎉 Success! What's Next?

You now have a working Skill Seeker installation! Here's what you can do:

### Try Other Presets

```bash
# See all available presets
ls configs/

# Try Vue.js
nexus-core create --config configs/vue.json --max-pages 50

# Try Django
nexus-core create --config configs/django.json --max-pages 50
```

### Try Other Source Types (17 Supported!)

```bash
# Auto-detect source type with the `create` command
nexus-core create https://docs.example.com   # Documentation
nexus-core create facebook/react              # GitHub repo
nexus-core create manual.pdf                  # PDF
nexus-core create report.docx                 # Word document
nexus-core create book.epub                   # EPUB book
nexus-core create analysis.ipynb              # Jupyter Notebook
nexus-core create spec.yaml                   # OpenAPI/Swagger spec
nexus-core create slides.pptx                 # PowerPoint

# More source types
nexus-core create --video-url https://youtube.com/watch?v=abc  # Video
nexus-core create --space-key DOCS                            # Confluence wiki
nexus-core create --database-id DB_ID                         # Notion
nexus-core create feed.rss                                    # RSS feed
nexus-core create grep.1                                      # Man page
nexus-core create --chat-export-path ./slack-export           # Slack/Discord
```

### Create Custom Skills

```bash
# Interactive mode - answer questions
nexus-core create --interactive

# Or create config for any website
nexus-core scrape \
  --name myframework \
  --url https://docs.myframework.com/ \
  --description "My favorite framework"
```

### Where to Save Custom Configs

You have three options for placing your custom config files:

**Option 1: User Config Directory (Recommended)**

```bash
# Create config in your home directory
mkdir -p ~/.config/nexus-core/configs
cat > ~/.config/nexus-core/configs/myproject.json << 'EOF'
{
  "name": "myproject",
  "base_url": "https://docs.myproject.com/",
  "max_pages": 50
}
EOF

# Use it
nexus-core create --config myproject.json
```

**Option 2: Current Directory (Project-Specific)**

```bash
# Create config in your project
mkdir -p configs
nano configs/myproject.json

# Use it
nexus-core create --config configs/myproject.json
```

**Option 3: Absolute Path**

```bash
# Use any file path
nexus-core create --config /full/path/to/config.json
```

The tool searches in this order: exact path → `./configs/` → `~/.config/nexus-core/configs/` → API presets

### Use with Claude Code (Advanced)

If you have Claude Code installed:

```bash
# One-time setup
./setup_mcp.sh

# Then use natural language in Claude Code:
# "Generate a skill for Svelte docs"
# "Package the skill at output/svelte/"
```

**See:** [docs/guides/MCP_SETUP.md](docs/guides/MCP_SETUP.md) for full MCP setup

---

## 🔧 Troubleshooting

### "Command not found" errors

**Problem:** `python3: command not found`

**Solution:** Python not installed or not in PATH
- macOS/Linux: Reinstall Python with brew/apt
- Windows: Reinstall Python, check "Add to PATH"
- Try `python` instead of `python3`

### "Permission denied" errors

**Problem:** Can't install packages

**Solution:**
```bash
# Use --user flag for pip
pip3 install --user nexus-core

# Or use a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### "No such file or directory"

**Problem:** CLI not found or config file path incorrect

**Solution:** Ensure you're using the CLI command correctly
```bash
# Verify installation
nexus-core --version
# Should show version 3.6.0+

# Verify config file exists at expected path
ls configs/
```

### "ModuleNotFoundError" or "command not found: nexus-core"

**Problem:** Package not installed or virtual environment not activated

**Solution:**
```bash
# Install the package in editable mode
pip install -e .

# Or if you need dev tools
pip install -e ".[dev]"
```

### Scraping is slow or fails

**Problem:** Takes forever or gets errors

**Solution:**
```bash
# Use smaller max_pages for testing
nexus-core create --config configs/react.json --max-pages 10

# Check internet connection
ping google.com

# Check the website is accessible
curl -I https://docs.yoursite.com
```

### Still stuck?

1. **Check our detailed troubleshooting guide:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Open an issue:** https://github.com/yusufkaraaslan/Nexus_Core/issues
3. **Include this info:**
   - Operating system (macOS 13, Ubuntu 22.04, Windows 11, etc.)
   - Python version (`python3 --version`)
   - Full error message
   - What command you ran

---

## 📚 Next Steps

- **Read the full README:** [README.md](README.md)
- **Learn about presets:** [configs/](configs/)
- **Try MCP integration:** [docs/guides/MCP_SETUP.md](docs/guides/MCP_SETUP.md)
- **Advanced usage:** [docs/](docs/)

---

## ✅ Quick Reference

```bash
# Your typical workflow:

# 1. Create/use a config
nexus-core create --config configs/react.json --max-pages 50

# 2. Package it
nexus-core package output/react/

# 3. Upload output/react.zip to Claude

# Done! 🎉
```

**Common locations:**
- **Configs:** `configs/*.json`
- **Output:** `output/skill-name/`
- **Packaged skills:** `output/skill-name.zip`

**Time estimates:**
- Small skill (5-10 pages): 30 seconds
- Medium skill (50-100 pages): 3-5 minutes
- Large skill (500+ pages): 15-30 minutes

---

**Still confused?** That's okay! Open an issue and we'll help you get started: https://github.com/yusufkaraaslan/Nexus_Core/issues/new
