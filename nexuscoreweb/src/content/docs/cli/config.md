---
title: config - Configuration Management
description: Interactive configuration wizard for GitHub tokens, API keys, rate limit settings, and resume preferences
section: cli
order: 9
---

# config - Configuration Management

Interactive wizard for managing Nexus Core configuration including GitHub tokens, API keys, and system settings.

## Basic Usage

```bash
nexus-core config [OPTIONS]
```

## Quick Examples

```bash
# Launch interactive configuration menu
nexus-core config

# Direct to GitHub token setup
nexus-core config --github

# Set up API keys
nexus-core config --api-keys

# View current configuration
nexus-core config --show

# Test all connections
nexus-core config --test
```

## Options

### Optional Flags

- `--github` - Direct to GitHub token setup
- `--api-keys` - Direct to API keys configuration
- `--show` - Display current configuration
- `--test` - Test all configured connections
- `--clean` - Clean up old progress files

## Interactive Menu

The main configuration menu provides 7 options:

### 1. GitHub Token Setup

Manage multiple GitHub profiles for flexible token management:

```bash
nexus-core config --github
```

**Features:**
- Add/remove GitHub profiles (personal, work, OSS, etc.)
- Set default profile
- Configure rate limit strategy per profile
- Browser integration - opens GitHub token creation page
- Token validation with format checking
- Automatic timeout configuration

**Rate Limit Strategies:**
- `prompt` - Ask user what to do (default, interactive)
- `wait` - Auto-wait with countdown timer
- `switch` - Automatically try another profile
- `fail` - Fail immediately with clear error

### 2. API Keys Configuration

Set up API keys for AI enhancement:

```bash
nexus-core config --api-keys
```

**Supported Platforms:**
- **Claude (Anthropic)** - For AI enhancement
- **Google Gemini** - For Gemini platform export
- **OpenAI ChatGPT** - For OpenAI platform export

**Features:**
- Browser integration - opens API key creation pages
- Environment variable fallback support
- Secure config file storage (600 permissions)
- Test connections after setup

### 3. Rate Limit Settings

Configure rate limit behavior:

**Options:**
- Default rate limit strategy (prompt/wait/switch/fail)
- Timeout per profile (default: 30 minutes)
- Non-interactive mode for CI/CD

### 4. Resume Settings

Configure resumable job preferences:

**Options:**
- Auto-save interval (default: 60 seconds)
- Auto-cleanup age (default: 7 days)
- Progress file location

### 5. View Current Configuration

Display all current settings:

```bash
nexus-core config --show
```

**Shows:**
- GitHub profiles and default
- API keys (masked for security)
- Rate limit strategies
- Resume settings
- Configuration file locations

### 6. Test Connections

Verify all configured tokens and API keys:

```bash
nexus-core config --test
```

**Tests:**
- GitHub token validity and rate limits
- API key authentication
- Network connectivity
- Permission scopes

### 7. Clean Up Old Progress Files

Remove old resumable job files:

```bash
nexus-core config --clean
```

Removes progress files older than configured cleanup age (default: 7 days).

## Configuration Storage

### Config File Location

```
~/.config/nexus-core/config.json
```

**Permissions:** 600 (read/write for owner only)

### Config File Structure

```json
{
  "github_profiles": {
    "personal": {
      "token": "ghp_...",
      "description": "Personal projects",
      "rate_limit_strategy": "prompt",
      "timeout": 1800
    },
    "work": {
      "token": "github_pat_...",
      "description": "Work projects",
      "rate_limit_strategy": "switch",
      "timeout": 900
    }
  },
  "default_github_profile": "personal",
  "api_keys": {
    "anthropic": "sk-ant-...",
    "google": "AIza...",
    "openai": "sk-..."
  },
  "resume": {
    "auto_save_interval": 60,
    "auto_cleanup_days": 7
  }
}
```

### Environment Variable Fallback

If not in config file, Nexus Core checks these environment variables:

```bash
# GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# API keys
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=AIza...
export OPENAI_API_KEY=sk-...
```

## GitHub Token Setup

### Creating a GitHub Token

1. Run `nexus-core config --github`
2. Select "Add New Profile"
3. Browser opens to: https://github.com/settings/tokens
4. Click "Generate new token (classic)"
5. **Required scopes:**
   - `repo` - Full control of private repositories
   - OR `public_repo` - Access public repositories (if only using public repos)
6. Copy token and paste into wizard
7. Set profile description and rate limit strategy

### Token Formats

Nexus Core accepts these GitHub token formats:

- **Classic PAT:** `ghp_...` (40 characters)
- **Fine-grained PAT:** `github_pat_...` (93+ characters)

### Rate Limits

**Without token:** 60 requests/hour
**With token:** 5000 requests/hour

The configuration wizard shows an upfront warning if no token is configured.

## Multi-Profile Workflow

### Use Case: Personal + Work Accounts

```bash
# Add profiles
nexus-core config --github

# Profile 1: Personal (unlimited timeout, prompt strategy)
name: personal
token: ghp_personal_token
strategy: prompt
timeout: unlimited

# Profile 2: Work (15 min timeout, auto-switch)
name: work
token: ghp_work_token
strategy: switch
timeout: 900

# Set default
default: personal
```

### Profile Switching

When a profile hits rate limits:

1. **prompt strategy** - Asks user what to do
2. **wait strategy** - Shows countdown timer, waits for reset
3. **switch strategy** - Automatically tries next available profile
4. **fail strategy** - Exits immediately with error

### Selecting Profile

```bash
# Use specific profile
nexus-core github --repo owner/repo --profile work

# Use default profile (from config)
nexus-core github --repo owner/repo
```

## API Keys Setup

### Claude (Anthropic)

```bash
nexus-core config --api-keys
# Select "Claude (Anthropic)"
# Browser opens to: https://console.anthropic.com/settings/keys
```

**Required for:**
- AI enhancement with Claude API
- Alternative to LOCAL enhancement

### Google Gemini

```bash
nexus-core config --api-keys
# Select "Google Gemini"
# Browser opens to: https://aistudio.google.com/app/apikey
```

**Required for:**
- Gemini platform export
- AI enhancement with Gemini API

### OpenAI ChatGPT

```bash
nexus-core config --api-keys
# Select "OpenAI ChatGPT"
# Browser opens to: https://platform.openai.com/api-keys
```

**Required for:**
- OpenAI platform export
- AI enhancement with GPT-4o

## First-Run Experience

On first installation, Nexus Core shows a welcome message with setup options:

```
Welcome to Nexus Core! 🎯

Choose your installation profile:
1. CLI Only (no MCP dependencies)
2. MCP Integration (full Claude Code support)
3. All Features (everything enabled)

Run 'nexus-core config' to set up GitHub tokens and API keys.
```

Stored at: `~/.config/nexus-core/.setup_shown`

## Testing Configuration

### Test All Connections

```bash
nexus-core config --test
```

**Output:**
```
Testing GitHub Tokens:
✓ personal (ghp_...) - 4,987/5,000 requests remaining
✓ work (github_pat_...) - 4,999/5,000 requests remaining

Testing API Keys:
✓ Claude (Anthropic) - Connected
✓ Google Gemini - Connected
× OpenAI ChatGPT - Not configured

Testing Network:
✓ GitHub API - Reachable
✓ Anthropic API - Reachable
✓ Google AI API - Reachable
```

### Test Individual Connections

The interactive menu provides real-time connection testing for each service.

## CI/CD Mode

For automated pipelines, use environment variables instead of interactive config:

```bash
# GitHub Actions example
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# Run in non-interactive mode
nexus-core github --repo owner/repo --non-interactive
```

**Non-interactive mode:**
- Fails fast on rate limits (no prompts)
- Uses `fail` strategy automatically
- Clear error messages for logs
- Exit codes for pipeline integration

## Troubleshooting

### Config File Not Found

```bash
# Create config directory
mkdir -p ~/.config/nexus-core

# Run config wizard
nexus-core config
```

### Permission Errors

```bash
# Fix config file permissions
chmod 600 ~/.config/nexus-core/config.json
```

### Token Validation Failed

```bash
# Test token manually
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/user

# Re-run config wizard
nexus-core config --github
```

### API Key Not Working

```bash
# Test connection
nexus-core config --test

# Remove and re-add key
nexus-core config --api-keys
```

## Security Best Practices

1. **Never commit tokens** to version control
2. **Use fine-grained tokens** when possible (least privilege)
3. **Set token expiration** for security
4. **Use separate profiles** for different projects
5. **Store tokens in config file** (not environment variables in production)
6. **Set file permissions** to 600 (read/write owner only)
7. **Rotate tokens regularly** (every 90 days recommended)

## See Also

- [resume command](/docs/cli/resume) - Resume interrupted jobs
- [github command](/docs/cli/github) - GitHub repository scraping
- [Multi-Token Configuration Guide](/docs/guides/multi-token-config) - Detailed configuration guide
- [Rate Limit Management Guide](/docs/guides/rate-limit-management) - Rate limit handling strategies
