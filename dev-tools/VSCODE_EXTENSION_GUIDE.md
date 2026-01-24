# Claude API Studio - VS Code Extension Guide

## Can This Run in VS Code?

**YES!** This can absolutely run as a VS Code extension. In fact, VS Code is arguably the **best platform** for this tool because:

✅ Developers already work in VS Code
✅ Direct access to your codebase (read patterns, write files)
✅ Rich webview API for custom UIs
✅ Terminal integration for running validations
✅ Git integration built-in
✅ Extension marketplace for easy distribution

## VS Code Extension Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VS Code Window                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────┐  ┌──────────────────────────────────┐ │
│  │  Sidebar       │  │  Editor Area                     │ │
│  │  (Tree View)   │  │                                  │ │
│  │                │  │  ┌────────────────────────────┐  │ │
│  │  📁 Endpoints  │  │  │  Webview Panel             │  │ │
│  │   └ Scenarios  │  │  │  (HTML/CSS/JS UI)          │  │ │
│  │   └ Budgets    │  │  │                            │  │ │
│  │   └ Accounts   │  │  │  [Chat Interface]          │  │ │
│  │                │  │  │  [Visual API Preview]      │  │ │
│  │  + New API...  │  │  │  [Interactive Playground]  │  │ │
│  │                │  │  │  [Export Buttons]          │  │ │
│  │                │  │  └────────────────────────────┘  │ │
│  │                │  │                                  │ │
│  └────────────────┘  └──────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Terminal (Validation Output)                        │  │
│  │  ✅ Spectral validation passed                       │  │
│  │  ✅ Postman governance passed                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Extension Backend (TypeScript/Node.js)
├── Pattern Analyzer (reads your codebase)
├── Claude API Integration (Anthropic SDK)
├── Validation Runner (spawns Spectral/Postman CLI)
├── File Writer (creates schemas/routes)
└── Postman Exporter (generates collection JSON)
```

## How It Would Work

### 1. Installation

```bash
# From VS Code Extensions marketplace
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search "Claude API Studio"
4. Click Install
5. Configure API key in settings
```

### 2. Daily Workflow

```
1. Open your Spearmint project in VS Code
2. Click "🤖 Claude API Studio" icon in sidebar
3. Click "+ New API Endpoint" button
4. Describe endpoint in chat panel
5. Visual preview appears instantly
6. Click tabs to explore (Overview, Playground, Flow)
7. Click "Export to Postman" or "Generate FastAPI Code"
8. Files written directly to your project
9. Git changes show up in Source Control tab
10. Commit with VS Code's built-in git
```

### 3. Key Features in VS Code

#### **Sidebar Panel** (Tree View)
- List all API endpoints in your project
- Click endpoint → Opens visual preview
- Right-click → "Edit with Claude", "Export to Postman", "Generate Mock"
- Filter by tag, method, status

#### **Webview Panel** (Main UI)
- Exact UI from the HTML demo
- Chat interface on the left
- Visual tabs on the right
- Everything runs locally

#### **Command Palette** (Ctrl+Shift+P)
- `Claude API Studio: Design New Endpoint`
- `Claude API Studio: Export to Postman`
- `Claude API Studio: Validate All APIs`
- `Claude API Studio: Generate Mock Server`

#### **Status Bar**
- Shows validation status
- Click to open validation panel
- Example: `✅ API: 12 endpoints valid`

## VS Code Extension vs Jupyter Notebook

| Feature | VS Code Extension | Jupyter Notebook | Web App |
|---------|------------------|------------------|---------|
| **Installation** | One-click from marketplace | Requires Python setup | Separate server |
| **Integration** | Native file access | Manual file paths | API calls |
| **Git** | Built-in | External | External |
| **UX** | Seamless workflow | Context switching | Context switching |
| **Distribution** | Marketplace | Share .ipynb file | Deploy server |
| **Updates** | Auto-update | Manual pull | Manual deploy |
| **Team Adoption** | Easy (everyone has VS Code) | Requires Jupyter | Requires URL |

**Recommendation:** VS Code Extension is the best choice for your team.

## Implementation: VS Code Extension

### Tech Stack

```json
{
  "framework": "VS Code Extension API",
  "language": "TypeScript",
  "ui": "Webview (HTML/CSS/JS or React)",
  "backend": "Node.js",
  "ai": "Anthropic SDK (TypeScript)",
  "validation": "Child process (Spectral CLI, Postman CLI)",
  "file-operations": "VS Code Workspace API"
}
```

### Project Structure

```
claude-api-studio-vscode/
├── package.json                  # Extension manifest
├── src/
│   ├── extension.ts              # Main extension entry point
│   ├── panels/
│   │   └── ApiDesignerPanel.ts   # Webview panel controller
│   ├── providers/
│   │   └── EndpointsProvider.ts  # Sidebar tree view provider
│   ├── services/
│   │   ├── ClaudeService.ts      # Claude API integration
│   │   ├── PatternAnalyzer.ts    # Analyzes existing code
│   │   ├── ValidationService.ts  # Runs Spectral/Postman
│   │   ├── FileWriter.ts         # Writes schemas/routes
│   │   └── PostmanExporter.ts    # Exports to Postman
│   └── webview/
│       ├── index.html            # Webview UI (the HTML demo)
│       ├── main.js               # Webview logic
│       └── styles.css            # VS Code theme-aware styles
├── media/                        # Icons and images
└── test/                         # Extension tests
```

### Key Code Examples

#### **extension.ts** (Entry Point)

```typescript
import * as vscode from 'vscode';
import { ApiDesignerPanel } from './panels/ApiDesignerPanel';
import { EndpointsProvider } from './providers/EndpointsProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('Claude API Studio activated!');

    // Register tree view provider
    const endpointsProvider = new EndpointsProvider(vscode.workspace.rootPath);
    vscode.window.registerTreeDataProvider('claudeApiStudio.endpoints', endpointsProvider);

    // Register command: Design new endpoint
    const designCommand = vscode.commands.registerCommand(
        'claudeApiStudio.designEndpoint',
        () => {
            ApiDesignerPanel.createOrShow(context.extensionUri);
        }
    );

    // Register command: Export to Postman
    const exportCommand = vscode.commands.registerCommand(
        'claudeApiStudio.exportPostman',
        async () => {
            const result = await exportToPostman();
            vscode.window.showInformationMessage(`✅ Exported to Postman: ${result.collectionName}`);
        }
    );

    context.subscriptions.push(designCommand, exportCommand);
}
```

#### **ApiDesignerPanel.ts** (Webview Controller)

```typescript
import * as vscode from 'vscode';
import { ClaudeService } from '../services/ClaudeService';

export class ApiDesignerPanel {
    public static currentPanel: ApiDesignerPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _claudeService: ClaudeService;

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._claudeService = new ClaudeService();

        // Set HTML content
        this._panel.webview.html = this._getHtmlContent(this._panel.webview, extensionUri);

        // Handle messages from webview
        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'generateEndpoint':
                        const endpoint = await this._claudeService.generateEndpoint(message.description);
                        this._panel.webview.postMessage({
                            command: 'endpointGenerated',
                            data: endpoint
                        });
                        break;

                    case 'exportPostman':
                        await this._exportToPostman(message.endpoint);
                        break;

                    case 'writeFiles':
                        await this._writeFilesToWorkspace(message.files);
                        break;
                }
            },
            undefined
        );
    }

    public static createOrShow(extensionUri: vscode.Uri) {
        // If panel already exists, reveal it
        if (ApiDesignerPanel.currentPanel) {
            ApiDesignerPanel.currentPanel._panel.reveal(vscode.ViewColumn.One);
            return;
        }

        // Create new panel
        const panel = vscode.window.createWebviewPanel(
            'claudeApiDesigner',
            '🤖 Claude API Studio',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')]
            }
        );

        ApiDesignerPanel.currentPanel = new ApiDesignerPanel(panel, extensionUri);
    }

    private _getHtmlContent(webview: vscode.Webview, extensionUri: vscode.Uri): string {
        // Load the HTML from the demo file (with VS Code theming)
        const htmlPath = vscode.Uri.joinPath(extensionUri, 'src', 'webview', 'index.html');
        // ... load and return HTML with proper asset URIs
        return htmlContent;
    }

    private async _exportToPostman(endpoint: any) {
        const postmanCollection = this._claudeService.generatePostmanCollection(endpoint);

        // Save to workspace
        const workspaceRoot = vscode.workspace.rootPath;
        const outputPath = `${workspaceRoot}/postman-collections/${endpoint.name}.json`;

        await vscode.workspace.fs.writeFile(
            vscode.Uri.file(outputPath),
            Buffer.from(JSON.stringify(postmanCollection, null, 2))
        );

        vscode.window.showInformationMessage(`✅ Exported to ${outputPath}`);
    }

    private async _writeFilesToWorkspace(files: any[]) {
        for (const file of files) {
            const uri = vscode.Uri.file(file.path);
            await vscode.workspace.fs.writeFile(uri, Buffer.from(file.content));
        }

        vscode.window.showInformationMessage(`✅ Created ${files.length} files`);

        // Refresh file explorer
        vscode.commands.executeCommand('workbench.files.action.refreshFilesExplorer');
    }
}
```

#### **ClaudeService.ts** (AI Integration)

```typescript
import Anthropic from '@anthropic-ai/sdk';
import * as vscode from 'vscode';

export class ClaudeService {
    private client: Anthropic;

    constructor() {
        // Get API key from VS Code settings
        const config = vscode.workspace.getConfiguration('claudeApiStudio');
        const apiKey = config.get<string>('anthropicApiKey');

        if (!apiKey) {
            throw new Error('Anthropic API key not configured. Please set it in VS Code settings.');
        }

        this.client = new Anthropic({ apiKey });
    }

    async generateEndpoint(description: string): Promise<GeneratedEndpoint> {
        // Analyze existing patterns in workspace
        const patterns = await this.analyzePatterns();

        // Build context-rich prompt
        const prompt = this.buildPrompt(description, patterns);

        // Call Claude API
        const response = await this.client.messages.create({
            model: 'claude-sonnet-4-5-20250929',
            max_tokens: 8192,
            messages: [{ role: 'user', content: prompt }]
        });

        // Parse structured response
        const endpoint = this.parseClaudeResponse(response.content[0].text);

        // Validate
        const validation = await this.validateEndpoint(endpoint);
        endpoint.validation = validation;

        return endpoint;
    }

    private async analyzePatterns(): Promise<CodebasePatterns> {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
        if (!workspaceRoot) {
            throw new Error('No workspace folder open');
        }

        // Read existing schemas and routes
        const schemaFiles = await vscode.workspace.findFiles('**/schemas/*.py');
        const routeFiles = await vscode.workspace.findFiles('**/routes/*.py');

        // Analyze patterns using AST or regex
        // ... pattern analysis logic ...

        return patterns;
    }

    private buildPrompt(description: string, patterns: CodebasePatterns): string {
        return `You are an API design assistant for Spearmint...

        PROJECT CONTEXT:
        ${JSON.stringify(patterns, null, 2)}

        USER REQUEST:
        ${description}

        Generate: schemas, routes, openapi, examples`;
    }
}
```

### Message Passing (Extension ↔ Webview)

```typescript
// In webview (webview/main.js)
const vscode = acquireVsCodeApi();

function generateEndpoint() {
    const description = document.getElementById('chat-input').value;

    // Send message to extension
    vscode.postMessage({
        command: 'generateEndpoint',
        description: description
    });
}

// Listen for messages from extension
window.addEventListener('message', event => {
    const message = event.data;

    switch (message.command) {
        case 'endpointGenerated':
            displayEndpoint(message.data);
            break;
    }
});
```

```typescript
// In extension (ApiDesignerPanel.ts)
this._panel.webview.onDidReceiveMessage(async (message) => {
    if (message.command === 'generateEndpoint') {
        const endpoint = await this._claudeService.generateEndpoint(message.description);

        // Send back to webview
        this._panel.webview.postMessage({
            command: 'endpointGenerated',
            data: endpoint
        });
    }
});
```

## Configuration (settings.json)

```json
{
  "claudeApiStudio.anthropicApiKey": "sk-ant-...",
  "claudeApiStudio.postmanWorkspaceId": "12345",
  "claudeApiStudio.postmanApiKey": "PMAK-...",
  "claudeApiStudio.enableAutoValidation": true,
  "claudeApiStudio.spectralRuleset": ".spectral-google.yaml",
  "claudeApiStudio.codegenMode": "incremental"
}
```

## Development Timeline

### Phase 1: Basic Extension (2 weeks)
- ✅ Extension scaffolding
- ✅ Webview panel with HTML UI
- ✅ Claude API integration
- ✅ Basic endpoint generation
- ✅ Message passing

### Phase 2: Visual Features (2 weeks)
- ✅ All 4 visualization tabs
- ✅ Interactive playground
- ✅ Flow diagram
- ✅ Syntax highlighting

### Phase 3: Integration (2 weeks)
- ✅ Pattern analyzer (reads existing code)
- ✅ Spectral validation integration
- ✅ Postman export
- ✅ File writing to workspace

### Phase 4: Polish (1 week)
- ✅ Sidebar tree view
- ✅ Command palette commands
- ✅ Status bar integration
- ✅ Error handling
- ✅ Settings UI

**Total: 7 weeks for VS Code extension**

## Publishing to VS Code Marketplace

```bash
# 1. Install vsce (VS Code Extension Manager)
npm install -g @vscode/vsce

# 2. Package extension
vsce package

# 3. Publish to marketplace
vsce publish
```

Users can then install with one click from the marketplace!

## Comparison: Different Visualization Approaches

### 1. **Schema Tree View** (Current Demo)
- ✅ Clear hierarchical structure
- ✅ Easy to scan
- ✅ Shows types and constraints
- ❌ Not as visual/graphical

### 2. **Form-Based Editor** (Alternative)
```
┌─────────────────────────────────────────────┐
│  Field Name:  [horizonMonths            ]  │
│  Type:        [Integer ▼]                  │
│  Required:    [✓] Yes  [ ] No              │
│  Min:         [1     ]  Max: [60    ]      │
│  Description: [Forecast period...       ]  │
│  [ + Add Field ]                           │
└─────────────────────────────────────────────┘
```
- ✅ Easiest for non-technical users
- ✅ Guided input
- ❌ Takes more screen space
- ❌ Slower for experienced developers

### 3. **Visual Graph/Flow** (Alternative)
```
    Request                  Response
      ┌────┐                   ┌────┐
      │name│────┐         ┌────│baseline│
      └────┘    │         │    └────────┘
      ┌────────┐│         │    ┌────────┐
      │horizon │├────→ [API] ─→│scenario│
      └────────┘│         │    └────────┘
      ┌────────┐│         │    ┌────────┐
      │adjusters├┘         └────│kpis    │
      └────────┘                └────────┘
```
- ✅ Very visual
- ✅ Shows relationships
- ❌ Hard to implement
- ❌ Doesn't scale to complex schemas

### 4. **Split View: Visual + Code** (Alternative)
```
┌──────────────────┬──────────────────┐
│  Visual Schema   │  Generated Code  │
│                  │                  │
│  name: string    │  class Request:  │
│  horizon: int    │    name: str     │
│  adjusters: []   │    horizon: int  │
│                  │    adjusters: [] │
│  [Edit Schema]   │                  │
└──────────────────┴──────────────────┘
```
- ✅ See both representations
- ✅ Real-time sync
- ❌ Requires more screen space

### 5. **Interactive Playground** (In Demo)
```
┌──────────────────┬──────────────────┐
│  Request JSON    │  Response JSON   │
│  (Editable)      │  (Live Preview)  │
│                  │                  │
│  { "name": ... } │  { "baseline"... │
│                  │                  │
│  [Send Request]  │  200 OK          │
└──────────────────┴──────────────────┘
```
- ✅ Test immediately
- ✅ See real examples
- ✅ Great for understanding
- ❌ Requires mock server

**Recommendation:** **Hybrid approach** (what the demo has):
1. **Schema Tree** for overview (scannable, complete)
2. **Interactive Playground** for testing (with examples)
3. **Flow Diagram** for understanding (request → processing → response)
4. **Swagger UI** for documentation (industry standard)

## Next Steps

### Option 1: Try the Visual Demo First
```bash
# Open the new visual demo
d:\CodingProjects\spearmint\dev-tools\claude-studio-visual-demo.html
```

Explore:
- 📋 API Overview tab (schema tree)
- 🎮 Interactive Playground tab (test with examples)
- 🔄 Flow Diagram tab (visual flow)
- 📤 Export panel (Postman export)

### Option 2: Build VS Code Extension Prototype
I can create a minimal working VS Code extension (1-2 weeks):
- Chat interface with Claude
- Visual API preview (HTML webview)
- Export to Postman
- File writing to workspace

### Option 3: Start with Postman AI (Quick Win)
Test Postman's AI features first, then build custom solution if needed.

## Questions to Consider

1. **Does the visual demo feel more useful than code-only?**
2. **Which tab (Overview/Playground/Flow) is most helpful?**
3. **Would you prefer this in VS Code or as a separate web app?**
4. **Is "Export to Postman" sufficient, or do you need full code generation?**
5. **Would your team use a VS Code extension daily?**

Let me know what you think after exploring the visual demo!
