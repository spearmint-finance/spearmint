import { readFileSync, existsSync } from 'fs';
import { join, dirname, basename, sep } from 'path';
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
  const parsed = parseToml(content) as Partial<ProjectConfig>;

  // Deep merge with defaults
  return {
    project: { ...DEFAULT_CONFIG.project, ...parsed.project },
    ports: { ...DEFAULT_CONFIG.ports, ...parsed.ports },
    database: parsed.database,
    env: parsed.env,
    hooks: parsed.hooks,
  };
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
# Documentation: https://github.com/spearmint-finance/spearmint

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
# [hooks]
# post_create_windows = [
#     "npm install",
#     "npm run db:setup"
# ]
`;
}

export function configExists(projectRoot: string): boolean {
  return existsSync(join(projectRoot, 'worktree.toml'));
}

export function getWorktreeName(worktreePath: string): string {
  // Handle both Windows and Unix path separators
  const parts = worktreePath.split(/[/\\]/);
  return parts[parts.length - 1];
}
