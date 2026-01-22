import { writeFileSync } from 'fs';
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
    try {
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
        try {
          execSync(`code "${config.worktreePath}"`, { stdio: 'inherit' });
        } catch {
          console.log(chalk.yellow('Could not open VS Code automatically'));
        }
      }

      process.exit(success ? 0 : 1);
    } catch (error) {
      console.log(chalk.red(`Error: ${error}`));
      process.exit(1);
    }
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
    try {
      const success = removeWorktree(options.name, {
        deleteBranch: options.deleteBranch,
        deleteRemote: options.deleteRemote,
        keepDatabase: options.keepDb,
        force: options.force,
      });

      process.exit(success ? 0 : 1);
    } catch (error) {
      console.log(chalk.red(`Error: ${error}`));
      process.exit(1);
    }
  });

program
  .command('list')
  .description('List all worktrees')
  .option('-d, --detailed', 'Show ports, database info, and git status')
  .action((options) => {
    try {
      listWorktrees(options.detailed);
    } catch (error) {
      console.log(chalk.red(`Error: ${error}`));
      process.exit(1);
    }
  });

program
  .command('cleanup')
  .description('Remove ALL worktrees (except main)')
  .option('-f, --force', 'Skip confirmation, discard uncommitted changes')
  .option('--keep-dbs', 'Keep all database files')
  .action((options) => {
    try {
      cleanupAll(options.force, options.keepDbs);
    } catch (error) {
      console.log(chalk.red(`Error: ${error}`));
      process.exit(1);
    }
  });

export { program };
