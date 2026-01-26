# Git Worktree CLI

Cross-platform CLI for managing ephemeral Git worktrees to enable parallel AI agent development.

## Installation

**Option 1: Install from npm (recommended)**

```bash
npm install -g git-worktree-cli
worktree --help
```

**Option 2: npx (no install needed)**

```bash
npx git-worktree-cli --help
```

**Option 3: From source**

```bash
git clone https://github.com/spearmint-finance/spearmint
cd spearmint/worktree-cli
npm install && npm run build && npm link
```

## Quick Start (New Project)

```bash
cd my-project
worktree init           # Creates worktree.toml configuration
# Edit worktree.toml to customize ports, hooks, etc.
echo ".worktrees/" >> .gitignore
worktree create         # Create your first worktree
```

## Quick Start (Existing Setup)

### Create a Worktree

```bash
# Auto-generate everything (name, branch, ports)
worktree create

# Output:
#   Name: wt-a3f2
#   Branch: worktree/wt-a3f2-20260121
#   Backend Port: 8001
#   Frontend Port: 5174

# Specify a custom name
worktree create --name my-feature

# Specify a branch name
worktree create -b feature/new-endpoint

# Open in VS Code automatically
worktree create --code

# Custom ports (rarely needed - auto-assigned by default)
worktree create --backend-port 8010 --frontend-port 5185
```

### List All Worktrees

```bash
# Simple list
worktree list

# With port/database details
worktree list --detailed
```

### Remove a Worktree

```bash
# Remove worktree by name
worktree remove -n wt-a3f2

# Remove worktree and delete branch
worktree remove -n wt-a3f2 --delete-branch

# Force remove without prompts
worktree remove -n wt-a3f2 --force
```

### Cleanup All Worktrees

```bash
# Remove all worktrees at once
worktree cleanup

# Force cleanup (skip confirmations)
worktree cleanup --force
```

### Initialize a New Project

```bash
# Create worktree.toml with defaults
worktree init

# Specify project name
worktree init --name my-awesome-project

# Overwrite existing config
worktree init --force
```

### Start Development Servers

```bash
# Start from main project (uses ports 8000/5173)
worktree dev

# Start from inside a worktree (auto-detects ports from .env)
cd .worktrees/wt-a3f2
worktree dev

# Start a specific worktree from anywhere
worktree dev -n wt-a3f2
```

This command:
1. Auto-detects if you're in main project or a worktree
2. Configures VS Code tasks with correct ports
3. Opens VS Code with the project
4. Creates "Start Dev Servers" task that runs backend + frontend in parallel

**In VS Code:** Press `Ctrl+Shift+P` → "Tasks: Run Task" → "Start Dev Servers"

## Port Assignments

Ports are **auto-assigned** by scanning existing worktrees:

| Worktree | Backend (API) | Frontend (Vite) |
|----------|---------------|-----------------|
| Main     | 8000          | 5173            |
| 1st      | 8001          | 5174            |
| 2nd      | 8002          | 5175            |
| 3rd      | 8003          | 5176            |
| ...      | 8000+N        | 5173+N          |

The CLI automatically finds the next available ports.

## Directory Structure

Worktrees are organized inside the project in a `.worktrees/` folder (gitignored):

```
my-project/
├── .worktrees/                    # All worktrees here (gitignored)
│   ├── wt-a3f2/                   # First worktree
│   │   ├── src/
│   │   └── .env                   # Worktree-specific config
│   └── wt-b7c1/                   # Second worktree
├── src/
├── worktree-cli/                  # CLI tool (TypeScript)
├── worktree.toml                  # Project configuration
└── .gitignore                     # Contains: .worktrees/
```

## Configuration (worktree.toml)

The CLI reads project-specific settings from `worktree.toml` in the project root:

```toml
[project]
name = "my-project"
worktree_dir = ".worktrees"

[ports]
backend_base = 8000
frontend_base = 5173
max_worktrees = 6

[database]
pattern = "myapp_{name}.db"
env_var = "DATABASE_URL"
url_template = "sqlite:///./{pattern}"

[env]
API_HOST = "127.0.0.1"
VITE_API_URL = "http://localhost:{backend_port}/api"

[hooks]
post_create = [
    "python3 -m venv venv",
    "./venv/bin/pip install -r requirements.txt",
    "npm install --prefix frontend"
]

post_create_windows = [
    "python -m venv venv",
    ".\\venv\\Scripts\\pip.exe install -r requirements.txt",
    "npm install --prefix frontend"
]
```

## Workflow Examples

### Parallel Development with Two Worktrees

```bash
# Terminal 1: Create first worktree
worktree create
# Note the name (e.g., wt-a3f2)
cd .worktrees/wt-a3f2
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python run_api.py  # Runs on auto-assigned port (e.g., :8001)

# Terminal 2: Create second worktree
worktree create
# Note the name (e.g., wt-b7c1)
cd .worktrees/wt-b7c1
python run_api.py  # Runs on :8002
```

### After Work is Complete

```bash
# Commit and push from worktree
cd .worktrees/wt-a3f2
git add .
git commit -m "feat: refactor API endpoints"
git push origin worktree/wt-a3f2-20260121

# Return to main and clean up
cd ../..
worktree remove -n wt-a3f2 -d

# Or clean up ALL worktrees at once
worktree cleanup
```

### Parallel AI Agents

```bash
# Terminal 1: Claude Code
worktree create
cd .worktrees/wt-a3f2
claude  # Claude works on backend

# Terminal 2: Another agent
worktree create
cd .worktrees/wt-b7c1
cursor  # Cursor works on frontend

# Both agents work simultaneously with isolated:
# - Branches
# - Ports
# - Databases
```

## Notes

- Worktrees share Git history but have independent working files
- Each worktree gets a unique `.env` file with port and database configuration
- Dependencies (node_modules, venv) are installed per worktree via hooks
- Databases are isolated per worktree to prevent data conflicts
- Works on Windows, macOS, and Linux

## Troubleshooting

### "Branch already exists"

The CLI will use the existing branch. For a fresh start, use `--force`:

```bash
worktree create -n my-feature -b feature/x --force
```

### "Worktree directory already exists"

Use `--force` to replace it:

```bash
worktree create -n my-feature --force
```

### Port already in use

Ports are auto-assigned, so conflicts are rare. Check existing worktrees:

```bash
worktree list -d
```

If needed, specify custom ports:

```bash
worktree create --backend-port 8050 --frontend-port 5200
```

### Hook failures

Check your `worktree.toml` hooks match your project structure. Common issues:
- Wrong paths to requirements.txt or package.json
- Missing `post_create_windows` for Windows-specific commands

## License

MIT
