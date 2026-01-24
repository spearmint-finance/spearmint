# Ephemeral Worktree Implementation for Spearmint

## Overview

This document provides instructions for implementing ephemeral Git worktrees for the spearmint project. The goal is to enable multiple AI coding agents to work in parallel on the same codebase without conflicts.

**Key Design Principles:**
- **Fully automatic** - Names, branches, and ports are auto-generated
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Zero configuration** - Just run `worktree create` and start working
- **Portable** - Can be used in any project via npm

---

## Using in Other Projects

The worktree CLI is designed to be generic and portable. You can use it in any Git project.

### Quick Start (Any Project)

**Option 1: Install globally from npm**

```bash
npm install -g git-worktree-cli

# In your project directory
cd my-project
worktree init          # Creates worktree.toml
worktree create        # Creates a new worktree
```

**Option 2: Use npx (no install)**

```bash
cd my-project
npx git-worktree-cli init
npx git-worktree-cli create
```

**Option 3: Add as dev dependency**

```bash
cd my-project
npm install --save-dev git-worktree-cli

# Add to package.json scripts:
# "scripts": { "worktree": "worktree" }

npm run worktree -- init
npm run worktree -- create
```

### Configuration (worktree.toml)

After running `worktree init`, edit `worktree.toml` to customize for your project:

```toml
[project]
name = "my-project"
worktree_dir = ".worktrees"

[ports]
backend_base = 3000          # Your backend port
frontend_base = 3001         # Your frontend port
max_worktrees = 6

# Database isolation (optional)
[database]
pattern = "myapp_{name}.db"
env_var = "DATABASE_URL"
url_template = "sqlite:///./{pattern}"

# Environment variables for each worktree (optional)
[env]
API_URL = "http://localhost:{backend_port}/api"

# Post-create setup commands (optional)
[hooks]
post_create = [
    "npm install",
    "npm run db:migrate"
]

# Windows-specific hooks (optional)
[hooks]
post_create_windows = [
    "npm install",
    "npm run db:migrate"
]
```

### Example Configurations

**Node.js/Express Project:**
```toml
[project]
name = "my-express-app"
worktree_dir = ".worktrees"

[ports]
backend_base = 3000
frontend_base = 3001
max_worktrees = 4

[hooks]
post_create = ["npm install"]
```

**Python/Django Project:**
```toml
[project]
name = "my-django-app"
worktree_dir = ".worktrees"

[ports]
backend_base = 8000
frontend_base = 3000
max_worktrees = 4

[database]
pattern = "db_{name}.sqlite3"
env_var = "DATABASE_URL"
url_template = "sqlite:///./{pattern}"

[hooks]
post_create = [
    "python -m venv venv",
    "venv/bin/pip install -r requirements.txt",
    "venv/bin/python manage.py migrate"
]
post_create_windows = [
    "python -m venv venv",
    "venv\\Scripts\\pip install -r requirements.txt",
    "venv\\Scripts\\python manage.py migrate"
]
```

**Monorepo with Multiple Services:**
```toml
[project]
name = "my-monorepo"
worktree_dir = ".worktrees"

[ports]
backend_base = 4000
frontend_base = 3000
max_worktrees = 6

[env]
API_GATEWAY_PORT = "{backend_port}"
WEB_PORT = "{frontend_port}"
SERVICES_PORT_OFFSET = "{backend_port}"

[hooks]
post_create = [
    "pnpm install",
    "pnpm run setup"
]
```

### Don't Forget

After setting up, add `.worktrees/` to your `.gitignore`:

```bash
echo ".worktrees/" >> .gitignore
```

---

## Spearmint Project Structure

The spearmint project is a **monorepo** containing a full-stack financial analysis application:

```
D:\CodingProjects\spearmint\
├── .vscode/                     # VS Code configuration
├── src/
│   └── financial_analysis/
│       ├── api/                 # FastAPI backend (routes, schemas)
│       ├── database/            # SQLAlchemy models, migrations
│       ├── services/            # Business logic layer
│       └── utils/               # Utility functions
├── frontend/                    # React + TypeScript frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── api/                 # API client
│   │   └── types/               # TypeScript types
│   └── package.json
├── tests/                       # Backend tests
├── dev-tools/                   # Development utilities
├── scripts/                     # Shared scripts
├── venv/                        # Python virtual environment
├── requirements.txt             # Python dependencies
├── CLAUDE.md                    # Claude Code instructions
└── *.db                         # SQLite database files
```

## Key Considerations for Worktrees

### Port Management

Each worktree needs unique ports to avoid conflicts. Ports are **auto-assigned** by scanning existing worktrees:

| Component | Main Worktree | Worktrees |
|-----------|---------------|-----------|
| Backend API | :8000 | :8001, :8002, :8003... (auto-assigned) |
| Frontend Dev Server | :5173 | :5174, :5175, :5176... (auto-assigned) |

### Database Isolation

Each worktree uses its own SQLite database to prevent data conflicts:
- Main worktree: `financial_analysis.db`
- Worktrees: `financial_analysis_<name>.db` (auto-named based on worktree)

This is configured via environment variables in the `.env` file.

## Implementation Tasks

### Task 1: Create CLI Directory Structure

Create a standalone CLI package at the project root:

```
spearmint/
├── worktree-cli/                  # Standalone CLI (can be extracted/published)
│   ├── package.json
│   ├── tsconfig.json
│   ├── README.md
│   └── src/
│       ├── index.ts               # Entry point
│       ├── cli.ts                 # Command definitions (Commander)
│       ├── config.ts              # Load worktree.toml, port assignments
│       ├── operations.ts          # Create/remove/list/cleanup logic
│       ├── git.ts                 # Git worktree operations
│       └── utils.ts               # Name generation, port scanning
├── worktree.toml                  # Project-specific configuration
└── ...
```

### Task 2: Create package.json

Create `worktree-cli/package.json`:

```json
{
  "name": "git-worktree-cli",
  "version": "0.1.0",
  "description": "CLI for managing ephemeral Git worktrees for parallel AI agent development",
  "type": "module",
  "bin": {
    "worktree": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js",
    "lint": "eslint src/",
    "prepublishOnly": "npm run build"
  },
  "files": [
    "dist"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/git-worktree-cli"
  },
  "dependencies": {
    "chalk": "^5.3.0",
    "commander": "^12.0.0",
    "dotenv": "^16.4.0",
    "simple-git": "^3.22.0",
    "toml": "^3.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "typescript": "^5.3.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "keywords": [
    "git",
    "worktree",
    "cli",
    "ai",
    "parallel-development",
    "monorepo",
    "workspace"
  ],
  "license": "MIT"
}
```

### Task 2b: Create tsconfig.json

Create `worktree-cli/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Task 3: Create Project Configuration File

Create `worktree.toml` in the project root (this is project-specific):

```toml
# Worktree CLI configuration for spearmint
# This file makes the CLI work for this specific project

[project]
name = "spearmint"
worktree_dir = ".worktrees"      # Relative to project root

[ports]
backend_base = 8000              # Main project backend port
frontend_base = 5173             # Main project frontend port
max_worktrees = 6                # Max concurrent worktrees

[database]
# Pattern for database file naming ({name} replaced with worktree name)
pattern = "financial_analysis_{name}.db"
env_var = "DATABASE_URL"
url_template = "sqlite:///./{pattern}"

[env]
# Additional environment variables added to each worktree's .env
API_HOST = "127.0.0.1"
VITE_API_URL = "http://localhost:{backend_port}/api"

[hooks]
# Commands to run after worktree creation (in order)
post_create = [
    "python -m venv venv",
    "venv/bin/pip install -r requirements.txt",
    "cd frontend && npm install",
    "venv/bin/python -m src.financial_analysis.database.init_db"
]

# Commands for Windows (used instead of post_create on Windows)
post_create_windows = [
    "python -m venv venv",
    "venv\\Scripts\\pip install -r requirements.txt",
    "cd frontend && npm install",
    "venv\\Scripts\\python -m src.financial_analysis.database.init_db"
]
```

### Task 3b: Create Configuration Module

Create `worktree-cli/src/config.ts`:

```typescript
import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { parse as parseToml } from 'toml';
import { execSync } from 'child_process';

export interface ProjectConfig {
  project: {
    name: string;
    worktree_dir: string;
  };
  ports: {
    backend_base: number;
    frontend_base: number;
    max_worktrees: number;
  };
  database?: {
    pattern: string;
    env_var: string;
    url_template: string;
  };
  env?: Record<string, string>;
  hooks?: {
    post_create?: string[];
    post_create_windows?: string[];
  };
}

export interface WorktreeConfig {
  name: string;
  branch: string;
  baseBranch: string;
  backendPort: number;
  frontendPort: number;
  projectRoot: string;
  worktreePath: string;
  projectConfig: ProjectConfig;
}

const DEFAULT_CONFIG: ProjectConfig = {
  project: {
    name: 'project',
    worktree_dir: '.worktrees',
  },
  ports: {
    backend_base: 8000,
    frontend_base: 5173,
    max_worktrees: 6,
  },
};

export function findProjectRoot(): string {
  let current = process.cwd();

  while (current !== dirname(current)) {
    if (existsSync(join(current, '.git'))) {
      return current;
    }
    current = dirname(current);
  }

  throw new Error('Could not find project root (no .git directory found)');
}

export function loadProjectConfig(projectRoot: string): ProjectConfig {
  const configPath = join(projectRoot, 'worktree.toml');

  if (!existsSync(configPath)) {
    console.warn('No worktree.toml found, using defaults');
    return DEFAULT_CONFIG;
  }

  const content = readFileSync(configPath, 'utf-8');
  const parsed = parseToml(content) as ProjectConfig;

  return { ...DEFAULT_CONFIG, ...parsed };
}

export function generateName(): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let suffix = '';
  for (let i = 0; i < 4; i++) {
    suffix += chars[Math.floor(Math.random() * chars.length)];
  }
  return `wt-${suffix}`;
}

export function generateBranchName(worktreeName: string): string {
  const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  return `worktree/${worktreeName}-${date}`;
}

export function getExistingWorktrees(projectRoot: string): Array<{ path: string; branch?: string }> {
  try {
    const output = execSync('git worktree list --porcelain', {
      cwd: projectRoot,
      encoding: 'utf-8',
    });

    const worktrees: Array<{ path: string; branch?: string }> = [];
    let current: { path?: string; branch?: string } = {};

    for (const line of output.trim().split('\n')) {
      if (line.startsWith('worktree ')) {
        if (current.path) worktrees.push(current as { path: string });
        current = { path: line.slice(9) };
      } else if (line.startsWith('branch ')) {
        current.branch = line.slice(7);
      }
    }

    if (current.path) worktrees.push(current as { path: string });
    return worktrees;
  } catch {
    return [];
  }
}

export function getUsedPorts(projectRoot: string): Set<number> {
  const config = loadProjectConfig(projectRoot);
  const usedPorts = new Set([config.ports.backend_base, config.ports.frontend_base]);

  const worktrees = getExistingWorktrees(projectRoot);

  for (const wt of worktrees) {
    const envPath = join(wt.path, '.env');
    if (existsSync(envPath)) {
      const content = readFileSync(envPath, 'utf-8');

      const apiMatch = content.match(/API_PORT=(\d+)/);
      if (apiMatch) usedPorts.add(parseInt(apiMatch[1], 10));

      const viteMatch = content.match(/VITE_PORT=(\d+)/);
      if (viteMatch) usedPorts.add(parseInt(viteMatch[1], 10));
    }
  }

  return usedPorts;
}

export function findNextAvailablePorts(projectRoot: string): { backend: number; frontend: number } {
  const config = loadProjectConfig(projectRoot);
  const usedPorts = getUsedPorts(projectRoot);

  let backend = config.ports.backend_base + 1;
  while (usedPorts.has(backend)) backend++;

  let frontend = config.ports.frontend_base + 1;
  while (usedPorts.has(frontend)) frontend++;

  return { backend, frontend };
}

export function getWorktreeConfig(options: {
  name?: string;
  branch?: string;
  baseBranch?: string;
  backendPort?: number;
  frontendPort?: number;
}): WorktreeConfig {
  const projectRoot = findProjectRoot();
  const projectConfig = loadProjectConfig(projectRoot);

  const name = options.name ?? generateName();
  const branch = options.branch ?? generateBranchName(name);
  const baseBranch = options.baseBranch ?? 'main';

  let { backendPort, frontendPort } = options;
  if (!backendPort || !frontendPort) {
    const ports = findNextAvailablePorts(projectRoot);
    backendPort = backendPort ?? ports.backend;
    frontendPort = frontendPort ?? ports.frontend;
  }

  const worktreesDir = join(projectRoot, projectConfig.project.worktree_dir);
  const worktreePath = join(worktreesDir, name);

  return {
    name,
    branch,
    baseBranch,
    backendPort,
    frontendPort,
    projectRoot,
    worktreePath,
    projectConfig,
  };
}

export function generateConfigTemplate(projectName: string): string {
  return `# Worktree CLI configuration for ${projectName}
# Documentation: https://github.com/yourusername/git-worktree-cli

[project]
name = "${projectName}"
worktree_dir = ".worktrees"      # Relative to project root

[ports]
backend_base = 8000              # Main project backend port
frontend_base = 5173             # Main project frontend port
max_worktrees = 6                # Max concurrent worktrees

# Optional: Database configuration
# Uncomment and customize if your project uses a database per worktree
# [database]
# pattern = "${projectName}_{name}.db"
# env_var = "DATABASE_URL"
# url_template = "sqlite:///./{pattern}"

# Optional: Additional environment variables for each worktree's .env
# [env]
# API_HOST = "127.0.0.1"
# VITE_API_URL = "http://localhost:{backend_port}/api"

# Optional: Commands to run after worktree creation
# [hooks]
# post_create = [
#     "npm install",
#     "npm run db:setup"
# ]

# Optional: Windows-specific hooks (used instead of post_create on Windows)
# [hooks.post_create_windows]
# post_create_windows = [
#     "npm install",
#     "npm run db:setup"
# ]
`;
}

export function configExists(projectRoot: string): boolean {
  return existsSync(join(projectRoot, 'worktree.toml'));
}
```

### Task 4: Create Git Operations Module

Create `worktree-cli/src/git.ts`:

```typescript
import { execSync, ExecSyncOptions } from 'child_process';
import { existsSync, rmSync } from 'fs';

export interface GitExecOptions {
  cwd?: string;
  silent?: boolean;
}

export function gitExec(args: string[], options: GitExecOptions = {}): string {
  const execOptions: ExecSyncOptions = {
    cwd: options.cwd,
    encoding: 'utf-8',
    stdio: options.silent ? 'pipe' : 'inherit',
  };

  try {
    return execSync(`git ${args.join(' ')}`, execOptions) as string;
  } catch (error) {
    if (options.silent) return '';
    throw error;
  }
}

export function fetchOrigin(cwd: string): void {
  gitExec(['fetch', 'origin'], { cwd, silent: true });
}

export function branchExists(branch: string, cwd: string): boolean {
  const local = gitExec(['branch', '--list', branch], { cwd, silent: true });
  const remote = gitExec(['branch', '-r', '--list', `origin/${branch}`], { cwd, silent: true });
  return Boolean(local.trim() || remote.trim());
}

export function getCurrentBranch(cwd: string): string {
  return gitExec(['branch', '--show-current'], { cwd, silent: true }).trim();
}

export function hasUncommittedChanges(cwd: string): boolean {
  const status = gitExec(['status', '--porcelain'], { cwd, silent: true });
  return Boolean(status.trim());
}

export function createWorktree(
  worktreePath: string,
  branch: string,
  baseBranch: string,
  cwd: string
): void {
  if (branchExists(branch, cwd)) {
    gitExec(['worktree', 'add', worktreePath, branch], { cwd });
  } else {
    gitExec(['worktree', 'add', worktreePath, '-b', branch, `origin/${baseBranch}`], { cwd });
  }
}

export function removeWorktree(worktreePath: string, cwd: string): void {
  gitExec(['worktree', 'remove', worktreePath, '--force'], { cwd, silent: true });
  gitExec(['worktree', 'prune'], { cwd, silent: true });

  // Fallback: manual removal if still exists
  if (existsSync(worktreePath)) {
    rmSync(worktreePath, { recursive: true, force: true });
  }
}

export function deleteBranch(branch: string, cwd: string, deleteRemote: boolean = false): void {
  gitExec(['branch', '-D', branch], { cwd, silent: true });

  if (deleteRemote) {
    gitExec(['push', 'origin', '--delete', branch], { cwd, silent: true });
  }
}
```

### Task 4b: Create Operations Module

Create `worktree-cli/src/operations.ts`:

```typescript
import { existsSync, mkdirSync, writeFileSync, readFileSync, copyFileSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { execSync } from 'child_process';
import chalk from 'chalk';
import {
  WorktreeConfig,
  findProjectRoot,
  loadProjectConfig,
  getExistingWorktrees,
} from './config.js';
import {
  fetchOrigin,
  createWorktree as gitCreateWorktree,
  removeWorktree as gitRemoveWorktree,
  getCurrentBranch,
  hasUncommittedChanges,
  deleteBranch,
} from './git.js';

function log(message: string): void {
  console.log(message);
}

function logSuccess(message: string): void {
  console.log(chalk.green('✓ ' + message));
}

function logWarning(message: string): void {
  console.log(chalk.yellow('⚠ ' + message));
}

function logError(message: string): void {
  console.log(chalk.red('✗ ' + message));
}

function logDim(message: string): void {
  console.log(chalk.dim(message));
}

export function createWorktree(config: WorktreeConfig, force: boolean = false): boolean {
  const { name, branch, baseBranch, backendPort, frontendPort, projectRoot, worktreePath, projectConfig } = config;

  // Print setup info
  console.log();
  console.log(chalk.cyan.bold('Creating Worktree'));
  console.log(chalk.dim('─'.repeat(40)));
  console.log(`  Name:          ${chalk.white(name)}`);
  console.log(`  Branch:        ${chalk.white(branch)}`);
  console.log(`  Backend Port:  ${chalk.white(backendPort)}`);
  console.log(`  Frontend Port: ${chalk.white(frontendPort)}`);
  console.log(`  Path:          ${chalk.white(worktreePath)}`);
  console.log();

  // Check if worktree already exists
  if (existsSync(worktreePath)) {
    if (force) {
      logWarning('Removing existing worktree...');
      gitRemoveWorktree(worktreePath, projectRoot);
    } else {
      logError(`Worktree already exists: ${worktreePath}`);
      log('Use --force to replace it, or remove it first.');
      return false;
    }
  }

  // Ensure worktrees directory exists
  const worktreesDir = dirname(worktreePath);
  if (!existsSync(worktreesDir)) {
    mkdirSync(worktreesDir, { recursive: true });
  }

  // Fetch latest
  logDim('Fetching latest from remote...');
  fetchOrigin(projectRoot);

  // Create worktree
  try {
    gitCreateWorktree(worktreePath, branch, baseBranch, projectRoot);
    logSuccess('Worktree created');
  } catch (error) {
    logError(`Failed to create worktree: ${error}`);
    return false;
  }

  // Create .env file
  createEnvFile(config);

  // Copy .env.local if exists
  const envLocalSrc = join(projectRoot, '.env.local');
  const envLocalDst = join(worktreePath, '.env.local');
  if (existsSync(envLocalSrc) && !existsSync(envLocalDst)) {
    copyFileSync(envLocalSrc, envLocalDst);
    logSuccess('Copied .env.local');
  }

  // Run post-create hooks
  runPostCreateHooks(config);

  // Print success message
  printSuccessMessage(config);

  return true;
}

function createEnvFile(config: WorktreeConfig): void {
  const { name, backendPort, frontendPort, worktreePath, projectConfig } = config;

  let envContent = `# Worktree configuration for ${name}
# Auto-generated by worktree-cli

# Backend settings
API_PORT=${backendPort}

# Frontend settings
VITE_PORT=${frontendPort}

# Worktree identifier
WORKTREE_NAME=${name}
`;

  // Add database config if specified
  if (projectConfig.database) {
    const dbPattern = projectConfig.database.pattern.replace('{name}', name);
    const dbUrl = projectConfig.database.url_template.replace('{pattern}', dbPattern);
    envContent += `\n# Database\n${projectConfig.database.env_var}=${dbUrl}\n`;
  }

  // Add custom env vars
  if (projectConfig.env) {
    envContent += '\n# Project-specific settings\n';
    for (const [key, value] of Object.entries(projectConfig.env)) {
      const resolvedValue = value
        .replace('{backend_port}', String(backendPort))
        .replace('{frontend_port}', String(frontendPort))
        .replace('{name}', name);
      envContent += `${key}=${resolvedValue}\n`;
    }
  }

  writeFileSync(join(worktreePath, '.env'), envContent);
  logSuccess('Environment configured (.env)');
}

function runPostCreateHooks(config: WorktreeConfig): void {
  const { worktreePath, projectConfig } = config;
  const isWindows = process.platform === 'win32';

  const hooks = isWindows
    ? projectConfig.hooks?.post_create_windows ?? projectConfig.hooks?.post_create
    : projectConfig.hooks?.post_create;

  if (!hooks || hooks.length === 0) return;

  logDim('Running post-create hooks...');

  for (const hook of hooks) {
    try {
      logDim(`  → ${hook}`);
      execSync(hook, { cwd: worktreePath, stdio: 'inherit' });
    } catch (error) {
      logWarning(`Hook failed: ${hook}`);
    }
  }

  logSuccess('Post-create hooks completed');
}

function printSuccessMessage(config: WorktreeConfig): void {
  const { name, branch, backendPort, frontendPort, worktreePath } = config;

  console.log();
  console.log(chalk.green.bold('Worktree Ready!'));
  console.log(chalk.dim('─'.repeat(40)));
  console.log(`  ${chalk.bold('Name:')}   ${name}`);
  console.log(`  ${chalk.bold('Path:')}   ${worktreePath}`);
  console.log(`  ${chalk.bold('Branch:')} ${branch}`);
  console.log();
  console.log(`  ${chalk.bold('To work in this worktree:')}`);
  console.log(chalk.cyan(`    cd ${worktreePath}`));
  console.log();
  console.log(`  ${chalk.bold('URLs:')}`);
  console.log(`    API:      http://localhost:${backendPort}`);
  console.log(`    Frontend: http://localhost:${frontendPort}`);
  console.log();
}

export function removeWorktree(
  name: string,
  options: {
    deleteBranch?: boolean;
    deleteRemote?: boolean;
    keepDatabase?: boolean;
    force?: boolean;
  } = {}
): boolean {
  const projectRoot = findProjectRoot();
  const projectConfig = loadProjectConfig(projectRoot);
  const worktreesDir = join(projectRoot, projectConfig.project.worktree_dir);
  const worktreePath = join(worktreesDir, name);

  if (!existsSync(worktreePath)) {
    logWarning(`Worktree does not exist: ${worktreePath}`);
    return true;
  }

  // Get branch name before removal
  const branchName = getCurrentBranch(worktreePath);

  console.log();
  console.log(chalk.yellow.bold('Removing Worktree'));
  console.log(chalk.dim('─'.repeat(40)));
  console.log(`  Name:   ${name}`);
  console.log(`  Branch: ${branchName}`);
  console.log(`  Path:   ${worktreePath}`);
  console.log();

  // Check for uncommitted changes
  if (!options.force && hasUncommittedChanges(worktreePath)) {
    logWarning('Worktree has uncommitted changes!');
    log('Use --force to discard changes, or commit them first.');
    return false;
  }

  // Remove worktree
  logDim('Removing worktree...');
  gitRemoveWorktree(worktreePath, projectRoot);
  logSuccess('Worktree removed');

  // Remove database
  if (!options.keepDatabase && projectConfig.database) {
    const dbPattern = projectConfig.database.pattern.replace('{name}', name);
    const dbFile = join(projectRoot, dbPattern);
    if (existsSync(dbFile)) {
      unlinkSync(dbFile);
      logSuccess('Database removed');
    }
  }

  // Delete branch
  if (options.deleteBranch && branchName) {
    logDim(`Deleting branch: ${branchName}`);
    deleteBranch(branchName, projectRoot, options.deleteRemote);
    logSuccess('Branch deleted');
  }

  console.log();
  console.log(chalk.green.bold('Cleanup complete!'));
  return true;
}

export function listWorktrees(detailed: boolean = false): void {
  const projectRoot = findProjectRoot();
  const projectConfig = loadProjectConfig(projectRoot);
  const worktreesDir = join(projectRoot, projectConfig.project.worktree_dir);

  console.log();
  console.log(chalk.cyan.bold(`${projectConfig.project.name} Worktrees`));
  console.log(chalk.dim('─'.repeat(40)));

  const worktrees = getExistingWorktrees(projectRoot);
  let wtCount = 0;

  for (const wt of worktrees) {
    const isMain = wt.path === projectRoot;
    const name = isMain ? null : wt.path.split('/').pop();

    if (isMain) {
      console.log(`${chalk.bold.white('[MAIN]')} ${wt.branch || 'unknown'}`);
    } else {
      console.log(`${chalk.bold.magenta(`[${name}]`)} ${wt.branch || 'unknown'}`);
      wtCount++;
    }

    console.log(chalk.dim(`       Path: ${wt.path}`));

    if (detailed && !isMain && existsSync(wt.path)) {
      const envPath = join(wt.path, '.env');
      if (existsSync(envPath)) {
        const content = readFileSync(envPath, 'utf-8');
        const apiMatch = content.match(/API_PORT=(\d+)/);
        const viteMatch = content.match(/VITE_PORT=(\d+)/);
        if (apiMatch) console.log(chalk.dim(`       Backend:  http://localhost:${apiMatch[1]}`));
        if (viteMatch) console.log(chalk.dim(`       Frontend: http://localhost:${viteMatch[1]}`));
      }

      const hasChanges = hasUncommittedChanges(wt.path);
      if (hasChanges) {
        console.log(chalk.yellow('       Status: has uncommitted changes'));
      } else {
        console.log(chalk.dim('       Status: clean'));
      }
    }

    console.log();
  }

  console.log(`${chalk.bold('Total worktrees:')} ${wtCount}`);

  if (wtCount === 0) {
    console.log();
    console.log(chalk.dim('No worktrees. Create one with:'));
    console.log(chalk.yellow('  npx worktree-cli create'));
  }
}

export function cleanupAll(force: boolean = false, keepDatabases: boolean = false): void {
  const projectRoot = findProjectRoot();
  const projectConfig = loadProjectConfig(projectRoot);
  const worktreesDir = join(projectRoot, projectConfig.project.worktree_dir);

  const worktrees = getExistingWorktrees(projectRoot);
  let removed = 0;

  for (const wt of worktrees) {
    // Skip main worktree
    if (wt.path === projectRoot) continue;

    // Check if it's in our worktrees directory
    if (wt.path.startsWith(worktreesDir)) {
      const name = wt.path.split('/').pop()!;
      logDim(`Removing ${name}...`);
      removeWorktree(name, { force, keepDatabase: keepDatabases });
      removed++;
    }
  }

  if (removed === 0) {
    logWarning('No worktrees to clean up.');
  } else {
    console.log();
    console.log(chalk.green.bold(`Cleaned up ${removed} worktree(s).`));
  }
}
```

### Task 5: Create Main CLI

Create `worktree-cli/src/cli.ts`:

```typescript
import { writeFileSync, existsSync } from 'fs';
import { join, basename } from 'path';
import { Command } from 'commander';
import chalk from 'chalk';
import {
  getWorktreeConfig,
  findProjectRoot,
  generateConfigTemplate,
  configExists,
} from './config.js';
import {
  createWorktree,
  removeWorktree,
  listWorktrees,
  cleanupAll,
} from './operations.js';

const program = new Command();

program
  .name('worktree')
  .description('CLI for managing ephemeral Git worktrees for parallel AI agent development')
  .version('0.1.0');

program
  .command('init')
  .description('Initialize worktree.toml configuration in the current project')
  .option('-f, --force', 'Overwrite existing worktree.toml')
  .option('-n, --name <name>', 'Project name (defaults to directory name)')
  .action((options) => {
    try {
      const projectRoot = findProjectRoot();
      const configPath = join(projectRoot, 'worktree.toml');

      if (configExists(projectRoot) && !options.force) {
        console.log(chalk.yellow('worktree.toml already exists.'));
        console.log(chalk.dim('Use --force to overwrite.'));
        process.exit(1);
      }

      const projectName = options.name ?? basename(projectRoot);
      const template = generateConfigTemplate(projectName);

      writeFileSync(configPath, template);

      console.log();
      console.log(chalk.green.bold('Initialized worktree.toml'));
      console.log(chalk.dim('─'.repeat(40)));
      console.log(`  Project: ${chalk.white(projectName)}`);
      console.log(`  Config:  ${chalk.white(configPath)}`);
      console.log();
      console.log(chalk.dim('Next steps:'));
      console.log(chalk.cyan('  1. Edit worktree.toml to customize settings'));
      console.log(chalk.cyan('  2. Add .worktrees/ to .gitignore'));
      console.log(chalk.cyan('  3. Run: worktree create'));
      console.log();
    } catch (error) {
      console.log(chalk.red(`Error: ${error}`));
      process.exit(1);
    }
  });

program
  .command('create')
  .description('Create a new worktree (auto-generates name, branch, ports by default)')
  .option('-n, --name <name>', 'Worktree name (auto-generated if not provided)')
  .option('-b, --branch <branch>', 'Branch name (auto-generated if not provided)')
  .option('--base <branch>', 'Base branch to create from', 'main')
  .option('--backend-port <port>', 'Backend API port (auto-assigned if not provided)', parseInt)
  .option('--frontend-port <port>', 'Frontend port (auto-assigned if not provided)', parseInt)
  .option('-f, --force', 'Replace existing worktree if it exists')
  .option('--code', 'Open worktree in VS Code after creation')
  .action(async (options) => {
    const config = getWorktreeConfig({
      name: options.name,
      branch: options.branch,
      baseBranch: options.base,
      backendPort: options.backendPort,
      frontendPort: options.frontendPort,
    });

    const success = createWorktree(config, options.force);

    if (success && options.code) {
      const { execSync } = await import('child_process');
      execSync(`code ${config.worktreePath}`, { stdio: 'inherit' });
    }

    process.exit(success ? 0 : 1);
  });

program
  .command('remove')
  .description('Remove a worktree by name')
  .requiredOption('-n, --name <name>', 'Worktree name to remove')
  .option('-d, --delete-branch', 'Also delete the Git branch')
  .option('--delete-remote', 'Also delete the remote branch (requires --delete-branch)')
  .option('--keep-db', 'Keep the worktree database file')
  .option('-f, --force', 'Skip confirmation, discard uncommitted changes')
  .action((options) => {
    const success = removeWorktree(options.name, {
      deleteBranch: options.deleteBranch,
      deleteRemote: options.deleteRemote,
      keepDatabase: options.keepDb,
      force: options.force,
    });

    process.exit(success ? 0 : 1);
  });

program
  .command('list')
  .description('List all worktrees')
  .option('-d, --detailed', 'Show ports, database info, and git status')
  .action((options) => {
    listWorktrees(options.detailed);
  });

program
  .command('cleanup')
  .description('Remove ALL worktrees (except main)')
  .option('-f, --force', 'Skip confirmation, discard uncommitted changes')
  .option('--keep-dbs', 'Keep all database files')
  .action((options) => {
    cleanupAll(options.force, options.keepDbs);
  });

export { program };
```

### Task 6: Create Entry Point

Create `worktree-cli/src/index.ts`:

```typescript
#!/usr/bin/env node

import { program } from './cli.js';

program.parse();
```

### Task 7: Install and Link CLI

The CLI is automatically available via npm. No wrapper scripts needed.

**Development (from project root):**

```bash
# Install dependencies
cd worktree-cli
npm install

# Build TypeScript
npm run build

# Link globally for development
npm link

# Now 'worktree' command is available globally
worktree --help
```

**Using without global install:**

```bash
# From project root (where worktree-cli/ is)
npx ./worktree-cli create

# Or use npm scripts in main package.json
npm run worktree -- create
```

**Optional: Add to main package.json for convenience:**

```json
{
  "scripts": {
    "worktree": "node ./worktree-cli/dist/index.js"
  }
}
```

Then use: `npm run worktree -- create`

### Task 8: Create VS Code Tasks

Update or create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Worktree: Create",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "create"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    },
    {
      "label": "Worktree: Create with Name",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "create", "-n", "${input:worktreeName}"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    },
    {
      "label": "Worktree: Create and Open in VS Code",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "create", "--code"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    },
    {
      "label": "Worktree: Remove",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "remove", "-n", "${input:worktreeName}"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    },
    {
      "label": "Worktree: List",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "list"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "shared" }
    },
    {
      "label": "Worktree: List (Detailed)",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "list", "-d"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "shared" }
    },
    {
      "label": "Worktree: Cleanup All",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "cleanup"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    },
    {
      "label": "Worktree: Init (Create Config)",
      "type": "shell",
      "command": "npx",
      "args": ["git-worktree-cli", "init"],
      "problemMatcher": [],
      "presentation": { "reveal": "always", "panel": "new" }
    }
  ],
  "inputs": [
    {
      "id": "worktreeName",
      "type": "promptString",
      "description": "Worktree name (e.g., my-feature, wt-a3f2). Use 'worktree list' to see existing names."
    }
  ]
}
```

### Task 9: Update Backend to Support Custom Ports

Ensure `run_api.py` supports the `--port` argument and reads from environment:

```python
# In run_api.py, ensure this pattern:
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=int(os.getenv('API_PORT', 8000)))
    parser.add_argument('--host', default=os.getenv('API_HOST', '127.0.0.1'))
    args = parser.parse_args()

    uvicorn.run("src.financial_analysis.api.main:app", host=args.host, port=args.port, reload=True)
```

### Task 10: Update Database Configuration

Ensure `src/financial_analysis/database/` reads the `DATABASE_URL` environment variable:

```python
# In database configuration, ensure this pattern:
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./financial_analysis.db')
```

### Task 10b: Update .gitignore

Add `.worktrees/` to `.gitignore` to exclude worktrees from version control:

```gitignore
# Worktrees (managed by worktree CLI)
.worktrees/
```

### Task 11: Create README for Worktree CLI

Create `worktree-cli/README.md`:

```markdown
# Worktree CLI

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
git clone https://github.com/yourusername/git-worktree-cli
cd git-worktree-cli
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

### Initialize a New Project

```bash
# Create worktree.toml with defaults
worktree init

# Specify project name
worktree init --name my-awesome-project

# Overwrite existing config
worktree init --force
```

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
spearmint/
├── .devcontainer/                 # Dev container config
├── .worktrees/                    # All worktrees here (gitignored)
│   ├── wt-a3f2/                   # First worktree
│   │   ├── src/
│   │   ├── frontend/
│   │   ├── financial_analysis_wt-a3f2.db
│   │   └── .env                   # Worktree-specific config
│   └── wt-b7c1/                   # Second worktree
├── src/
├── frontend/
├── worktree-cli/                  # CLI tool (TypeScript)
├── worktree.toml                  # Project configuration
├── financial_analysis.db          # Main database
└── .gitignore                     # Contains: .worktrees/
```

### Cleanup All Worktrees

```bash
# Remove all worktrees at once
worktree cleanup

# Force cleanup (skip confirmations)
worktree cleanup --force
```

## Workflow Example

### Parallel Development with Two Worktrees

```bash
# Terminal 1: Create first worktree (auto-generates everything)
worktree create
# Note the name printed, e.g., "wt-a3f2"
cd .worktrees/wt-a3f2
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python run_api.py  # Runs on auto-assigned port (e.g., :8001)
claude  # Start Claude Code

# Terminal 2: Create second worktree
worktree create
# Note the name printed, e.g., "wt-b7c1"
cd .worktrees/wt-b7c1
python run_api.py  # Runs on :8002
```

### After Work is Complete

```bash
# Commit and push from worktree
cd .worktrees/wt-a3f2
git add .
git commit -m "feat: refactor API endpoints"
git push origin worktree/wt-a3f2-20260121  # your auto-generated branch

# Return to main and clean up
cd ../..
worktree remove -n wt-a3f2 -d

# Or clean up ALL worktrees at once
worktree cleanup
```

## Configuration (worktree.toml)

The CLI reads project-specific settings from `worktree.toml` in the project root:

```toml
[project]
name = "spearmint"
worktree_dir = ".worktrees"

[ports]
backend_base = 8000
frontend_base = 5173
max_worktrees = 6

[database]
pattern = "financial_analysis_{name}.db"
env_var = "DATABASE_URL"
url_template = "sqlite:///./{pattern}"

[hooks]
post_create = [
    "python -m venv venv",
    "venv/bin/pip install -r requirements.txt",
    "cd frontend && npm install"
]
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

### Database not found errors
Run the database initialization:
```bash
cd .worktrees/wt-a3f2
source venv/bin/activate
python -m src.financial_analysis.database.init_db
```
```

### Task 12: Update CLAUDE.md

Add the following section to the existing `CLAUDE.md`:

```markdown
## Worktree Management

This project supports parallel AI agent development using Git worktrees. The CLI is built with TypeScript/Node.js.

### Setup (one-time)

```bash
# Build and link the CLI
cd worktree-cli && npm install && npm run build && npm link
cd ..

# Or use npx without installing globally
npx ./worktree-cli --help
```

### Creating a Worktree for Yourself

If you need to work in isolation (e.g., for a long-running task or to avoid conflicts with another agent):

```bash
# Auto-generate everything (name, branch, ports)
worktree create

# Output shows name (e.g., wt-a3f2) and ports

# Or specify a branch
worktree create -b feature/my-feature

# Using npx (if not linked globally)
npx worktree-cli create
```

Then work in the new directory (shown in output, e.g., `.worktrees/wt-a3f2`)

Your worktree will have:
- Auto-assigned backend port (e.g., 8001)
- Auto-assigned frontend port (e.g., 5174)
- Isolated database: `financial_analysis_<name>.db`

### Starting Services in a Worktree

```bash
# Backend
cd .worktrees/wt-a3f2
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python run_api.py  # Uses port from .env

# Frontend (separate terminal)
cd .worktrees/wt-a3f2/frontend
npm run dev  # Uses port from .env
```

### Checking Existing Worktrees

```bash
worktree list --detailed

# Or with npx
npx worktree-cli list --detailed
```

### Cleanup After Work

```bash
# Remove worktree and delete the branch (use name from 'worktree list')
worktree remove -n wt-a3f2 --delete-branch

# Or cleanup ALL worktrees at once
worktree cleanup
```
```

---

## Dev Container Implementation

The dev container provides a consistent development environment. You open the **main project** in a dev container, then create and manage worktrees from inside it.

### Architecture: Single Container, Multiple Worktrees

```
┌─────────────────────────────────────────────────────────────────┐
│                VS Code Dev Container                            │
│                (main spearmint folder)                          │
│                                                                 │
│  /workspace/                    ← Main project mounted here     │
│  ├── src/                                                       │
│  ├── frontend/                                                  │
│  ├── .worktrees/                ← Worktrees created here        │
│  │   ├── wt-a3f2/              (each has its own .env)         │
│  │   └── wt-b7c1/                                              │
│  └── scripts/worktree/          ← CLI tool                      │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ Terminal 1      │  │ Terminal 2      │                      │
│  │ cd .worktrees/  │  │ cd .worktrees/  │                      │
│  │    wt-a3f2      │  │    wt-b7c1      │                      │
│  │ python run_api  │  │ claude          │                      │
│  │ (port 8001)     │  │ (port 8002)     │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- One VS Code window manages everything
- Worktrees share the container environment
- No Docker overhead per worktree
- Agents work in terminal tabs

### Task 11: Create Dev Container Configuration

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "Spearmint",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    },
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/git:1": {}
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/workspace/venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "editor.formatOnSave": true
      }
    }
  },

  "forwardPorts": [8000, 8001, 8002, 8003, 8004, 8005, 5173, 5174, 5175, 5176, 5177, 5178],

  "postCreateCommand": "bash .devcontainer/post-create.sh",

  "postStartCommand": "bash .devcontainer/post-start.sh"
}
```

### Task 12: Create Docker Compose

Create `.devcontainer/docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
      - venv:/workspace/venv
      - node_modules:/workspace/frontend/node_modules
    ports:
      # Main project
      - "8000:8000"
      - "5173:5173"
      # Worktrees (8001-8005 backend, 5174-5178 frontend)
      - "8001:8001"
      - "8002:8002"
      - "8003:8003"
      - "8004:8004"
      - "8005:8005"
      - "5174:5174"
      - "5175:5175"
      - "5176:5176"
      - "5177:5177"
      - "5178:5178"
    command: sleep infinity

volumes:
  venv:
  node_modules:
```

### Task 13: Create Dockerfile

Create `.devcontainer/Dockerfile`:

```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Install additional tools
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["sleep", "infinity"]
```

### Task 14: Create Post-Create Script

Create `.devcontainer/post-create.sh`:

```bash
#!/bin/bash
set -e

echo "==================================="
echo "  Setting up Spearmint Dev Container"
echo "==================================="

# Create Python virtual environment
if [ ! -d "/workspace/venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv /workspace/venv
fi

# Install Python dependencies
echo "Installing Python dependencies..."
source /workspace/venv/bin/activate
pip install --upgrade pip
pip install -r /workspace/requirements.txt

# Install frontend dependencies
if [ -f "/workspace/frontend/package.json" ]; then
    echo "Installing frontend dependencies..."
    cd /workspace/frontend
    npm install
    cd /workspace
fi

# Build and link worktree CLI
if [ -f "/workspace/worktree-cli/package.json" ]; then
    echo "Building worktree CLI..."
    cd /workspace/worktree-cli
    npm install
    npm run build
    npm link
    cd /workspace
fi

# Initialize main database
echo "Initializing database..."
python -m src.financial_analysis.database.init_db || true

# Create .worktrees directory
mkdir -p /workspace/.worktrees

echo ""
echo "==================================="
echo "  Setup Complete!"
echo ""
echo "  Main project: http://localhost:8000"
echo "  Worktrees:    .worktrees/"
echo "  CLI:          worktree --help"
echo "==================================="
```

### Task 15: Create Post-Start Script

Create `.devcontainer/post-start.sh`:

```bash
#!/bin/bash

# Auto-activate venv in new terminals
if ! grep -q "source /workspace/venv/bin/activate" ~/.bashrc; then
    echo "source /workspace/venv/bin/activate" >> ~/.bashrc
fi

echo ""
echo "==================================="
echo "  Spearmint Dev Container Ready"
echo "==================================="
echo ""
echo "  Create a worktree:  worktree create"
echo "                      (or: npx worktree-cli create)"
echo "  List worktrees:     worktree list"
echo "  Start main API:     python run_api.py"
echo ""
```

### Workflow: Working with Worktrees in Dev Container

#### 1. Open Project in Dev Container

```bash
# From host machine
code spearmint/

# VS Code prompts: "Reopen in Container" → Click it
```

#### 2. Create Worktrees from Inside Container

```bash
# Inside dev container terminal
worktree create
# Output:
#   Name: wt-a3f2
#   Branch: worktree/wt-a3f2-20260121
#   Backend Port: 8001
#   Frontend Port: 5174
#   Path: /workspace/.worktrees/wt-a3f2
```

#### 3. Work in a Worktree

```bash
# Open new terminal tab in VS Code (Ctrl+Shift+`)
cd .worktrees/wt-a3f2

# Start the API for this worktree
python run_api.py  # Uses port 8001 from .env

# Or start an AI agent
claude  # Works directly in the worktree
```

#### 4. Run Multiple Agents in Parallel

```bash
# Terminal 1: First worktree
cd .worktrees/wt-a3f2
python run_api.py  # Port 8001

# Terminal 2: Second worktree
worktree create    # Creates wt-b7c1
cd .worktrees/wt-b7c1
python run_api.py  # Port 8002

# Terminal 3: Agent in first worktree
cd .worktrees/wt-a3f2
claude

# Terminal 4: Different agent in second worktree
cd .worktrees/wt-b7c1
cursor  # or any other agent
```

#### 5. Access Services from Host Browser

All ports are forwarded to your host machine:

| Worktree | API URL | Frontend URL |
|----------|---------|--------------|
| main | http://localhost:8000 | http://localhost:5173 |
| wt-a3f2 | http://localhost:8001 | http://localhost:5174 |
| wt-b7c1 | http://localhost:8002 | http://localhost:5175 |

#### 6. Cleanup

```bash
# Remove a specific worktree
worktree remove -n wt-a3f2 --delete-branch

# Remove ALL worktrees
worktree cleanup --force
```

### Port Allocation

Ports are auto-assigned sequentially:

| Component | Main | Worktree 1 | Worktree 2 | Worktree 3 |
|-----------|------|------------|------------|------------|
| Backend API | 8000 | 8001 | 8002 | 8003 |
| Frontend | 5173 | 5174 | 5175 | 5176 |

The container forwards ports 8000-8005 and 5173-5178, supporting up to 6 concurrent worktrees.

### Database Isolation

Each worktree gets its own SQLite database:

```
/workspace/
├── financial_analysis.db           # Main project
└── .worktrees/
    ├── wt-a3f2/
    │   └── financial_analysis_wt-a3f2.db
    └── wt-b7c1/
        └── financial_analysis_wt-b7c1.db
```

---

## Verification Checklist

After implementation, verify:

### CLI Installation
- [ ] `worktree-cli/` directory exists with TypeScript source
- [ ] `npm install` and `npm run build` succeed in `worktree-cli/`
- [ ] `npm link` makes `worktree` command available globally
- [ ] `worktree --help` shows available commands
- [ ] `npx ./worktree-cli --help` works from project root

### CLI Commands
- [ ] `worktree init` creates `worktree.toml` with sensible defaults
- [ ] `worktree init --name my-project` uses specified project name
- [ ] `worktree init --force` overwrites existing config
- [ ] `worktree create` creates worktree with auto-generated name, branch, and ports
- [ ] `worktree create -n my-feature -b feature/x` creates worktree with specified name/branch
- [ ] `.env` file is generated with correct port and database settings
- [ ] `worktree remove -n wt-a3f2` cleans up worktree and database
- [ ] `worktree list` shows all worktrees
- [ ] `worktree list -d` shows detailed info (ports, db, status)
- [ ] `worktree cleanup` removes all worktrees

### Configuration
- [ ] `worktree.toml` exists in project root (or can be created with `worktree init`)
- [ ] CLI reads project settings from `worktree.toml`
- [ ] CLI works with default settings when no `worktree.toml` exists
- [ ] Post-create hooks run correctly
- [ ] Windows-specific hooks run on Windows

### VS Code Integration
- [ ] VS Code tasks appear in task list (`Ctrl+Shift+P` > "Tasks: Run Task")
- [ ] "Worktree: Create" task works (uses npx)
- [ ] "Worktree: Create and Open in VS Code" task works
- [ ] "Worktree: Cleanup All" task works

### Runtime Isolation
- [ ] Backend starts on correct port from worktree
- [ ] Frontend starts on correct port from worktree
- [ ] Database is isolated per worktree

### Cross-Platform
- [ ] CLI works on Windows (PowerShell/CMD)
- [ ] CLI works on macOS/Linux (bash/zsh)
- [ ] Path handling works correctly on both platforms

### Dev Container
- [ ] `.devcontainer/devcontainer.json` exists
- [ ] `.devcontainer/docker-compose.yml` exists
- [ ] `.devcontainer/Dockerfile` exists
- [ ] `.devcontainer/post-create.sh` is executable
- [ ] `.devcontainer/post-start.sh` is executable
- [ ] Dev container builds successfully
- [ ] Dev container forwards ports 8000-8005 and 5173-5178
- [ ] Python venv is created inside container
- [ ] npm dependencies install inside container
- [ ] Worktree CLI is built and linked in container
- [ ] Main database initializes inside container
- [ ] `.worktrees/` directory is created
- [ ] Worktrees can be created from inside container
- [ ] Multiple worktrees work simultaneously inside single container

### .gitignore
- [ ] `.worktrees/` is added to `.gitignore`

### Portability (Other Projects)
- [ ] `npm install -g git-worktree-cli` installs globally
- [ ] `npx git-worktree-cli init` works in any Git project
- [ ] Generated `worktree.toml` template is valid
- [ ] CLI works without `worktree.toml` (uses defaults)
- [ ] Project-specific hooks in `worktree.toml` execute correctly

## Usage Examples

### Example 1: Dev Container with Multiple Worktrees

```bash
# 1. Open project in VS Code and reopen in container
code spearmint/
# Click "Reopen in Container" when prompted

# 2. Inside container, create worktrees
worktree create
# Output: Name: wt-a3f2, Ports: 8001/5174

worktree create
# Output: Name: wt-b7c1, Ports: 8002/5175

# 3. Work in worktrees (open new terminal tabs)
# Terminal 1:
cd .worktrees/wt-a3f2
python run_api.py  # :8001

# Terminal 2:
cd .worktrees/wt-b7c1
python run_api.py  # :8002

# 4. Access from host browser:
# - http://localhost:8001 (wt-a3f2)
# - http://localhost:8002 (wt-b7c1)

# 5. Cleanup
worktree cleanup
```

### Example 2: Quick Feature Branch

```bash
# Create worktree with specific branch
worktree create -b fix/typo-in-api
# Note the name from output (e.g., wt-c9d3)

# Work in the worktree
cd .worktrees/wt-c9d3
# Make changes...
git add . && git commit -m "fix: typo in API response"
git push origin fix/typo-in-api

# Clean up
cd ../..
worktree remove -n wt-c9d3 -d
```

### Example 3: Parallel AI Agents

```bash
# Inside dev container, create worktrees for different agents

# Terminal 1: Claude Code
worktree create
cd .worktrees/wt-a3f2
claude  # Claude works on backend refactor

# Terminal 2: Another agent
worktree create
cd .worktrees/wt-b7c1
cursor  # Cursor works on frontend

# Both agents work simultaneously with isolated:
# - Branches
# - Ports
# - Databases

# When done
worktree cleanup --force
```

### Example 4: Local Development (No Container)

```bash
# Setup CLI first (one-time)
cd worktree-cli && npm install && npm run build && npm link && cd ..

# Now create worktrees
worktree create
cd .worktrees/wt-a3f2

# Activate local venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\Activate.ps1  # Windows

python run_api.py  # Uses port from .env
```

---

## Appendix A: Future Enhancements

### VS Code Extension Support for Worktrees

**Current Limitation:**
The current implementation is optimized for CLI-based AI agents (like Claude Code) that work in terminal sessions. VS Code extension-based tools (Copilot, Cursor, Augment) operate on the active workspace, not the terminal's working directory. This means extensions in the main VS Code window won't automatically "see" worktree code.

**Potential Solutions to Explore:**

#### Option 1: Multi-Root Workspace Integration

Add CLI support for automatically configuring VS Code multi-root workspaces:

```bash
# Future CLI command
worktree create --add-to-workspace

# This would:
# 1. Create the worktree as usual
# 2. Modify .code-workspace file to include the worktree
# 3. VS Code extensions can then see all worktrees
```

Implementation considerations:
- Create/update a `spearmint.code-workspace` file
- Add each worktree as a workspace folder
- Configure per-folder settings (Python interpreter, etc.)
- Handle cleanup when worktree is removed

Example `.code-workspace` structure:
```json
{
  "folders": [
    { "path": ".", "name": "main" },
    { "path": ".worktrees/wt-a3f2", "name": "wt-a3f2" },
    { "path": ".worktrees/wt-b7c1", "name": "wt-b7c1" }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
  }
}
```

#### Option 2: Separate VS Code Windows (Same Container)

Add CLI support for opening worktrees in separate VS Code windows:

```bash
# Future CLI command
worktree create --open-window

# Opens a new VS Code window connected to the same container
# but with the worktree as the workspace root
```

This would allow:
- Each VS Code window has its own workspace
- Extensions in each window work on different code
- All windows share the same container resources

#### Option 3: VS Code Extension for Worktree Management

Create a dedicated VS Code extension that:
- Provides a sidebar panel showing all worktrees
- Allows quick switching between worktrees
- Integrates with existing AI extensions to set context
- Manages worktree lifecycle from the GUI

#### Option 4: Workspace-Aware AI Extension Configuration

Some AI extensions support workspace configuration. Future enhancement could:
- Auto-generate extension-specific config files per worktree
- Configure `.cursorrules`, `.github/copilot-instructions.md`, etc.
- Scope AI context to the active worktree folder

### Implementation Priority

For teams primarily using CLI-based agents (Claude Code), the current implementation is sufficient. Consider implementing VS Code extension support when:

1. Team adopts extension-based AI tools as primary workflow
2. Multiple developers need GUI-based parallel development
3. Specific extension features require workspace-level integration

### Related GitHub Issues

*(To be created when pursuing these enhancements)*

- [ ] `worktree create --add-to-workspace` - Multi-root workspace integration
- [ ] `worktree create --open-window` - Separate VS Code window support
- [ ] VS Code extension for worktree management
- [ ] Per-worktree AI extension configuration
