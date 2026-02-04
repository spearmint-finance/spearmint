#!/usr/bin/env npx tsx
/**
 * MCP Tool Generator
 *
 * Generates MCP tool definitions from OpenAPI spec based on tool-config.json.
 * This enables auto-generation of tools when the API spec changes.
 *
 * Usage:
 *   npx tsx scripts/generate-tools.ts
 *   npx tsx scripts/generate-tools.ts --config path/to/config.json
 *   npx tsx scripts/generate-tools.ts --dry-run
 */

import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Types for the configuration
interface ParameterOverride {
  description?: string;
  type?: string;
  enum?: string[];
}

interface ToolConfig {
  name: string;
  operationId: string;
  path: string;
  method: string;
  description: string;
  usageHint?: string;
  parameterOverrides?: Record<string, ParameterOverride>;
  excludeParameters?: string[];
}

interface Config {
  description: string;
  openApiPath: string;
  outputDir: string;
  tools: ToolConfig[];
}

// OpenAPI types (simplified)
interface OpenAPIParameter {
  name: string;
  in: string;
  required?: boolean;
  schema: {
    type?: string;
    anyOf?: Array<{ type: string; format?: string; enum?: string[] }>;
    enum?: string[];
    format?: string;
    description?: string;
    default?: unknown;
    minimum?: number;
    maximum?: number;
  };
  description?: string;
}

interface OpenAPIOperation {
  operationId?: string;
  summary?: string;
  description?: string;
  parameters?: OpenAPIParameter[];
  responses?: Record<string, unknown>;
}

interface OpenAPISpec {
  openapi: string;
  info: { title: string; version: string };
  paths: Record<string, Record<string, OpenAPIOperation>>;
  components?: {
    schemas?: Record<string, unknown>;
  };
}

// Generated tool structure
interface MCPToolProperty {
  type: string;
  description?: string;
  enum?: string[];
}

interface MCPToolInputSchema {
  type: "object";
  properties: Record<string, MCPToolProperty>;
  required: string[];
}

interface GeneratedTool {
  name: string;
  description: string;
  usageHint?: string;
  inputSchema: MCPToolInputSchema;
  apiEndpoint: string;
  httpMethod: string;
}

/**
 * Convert OpenAPI parameter schema to MCP tool property
 */
function convertParameterToProperty(
  param: OpenAPIParameter,
  override?: ParameterOverride
): MCPToolProperty {
  let type = "string";
  let enumValues: string[] | undefined;

  // Handle anyOf (nullable types in OpenAPI 3.1)
  if (param.schema.anyOf) {
    const nonNullType = param.schema.anyOf.find((t) => t.type !== "null");
    if (nonNullType) {
      type = nonNullType.type || "string";
      enumValues = nonNullType.enum;
    }
  } else {
    type = param.schema.type || "string";
    enumValues = param.schema.enum;
  }

  // Map OpenAPI types to JSON Schema types
  if (type === "integer") {
    type = "number";
  }

  const property: MCPToolProperty = {
    type,
    description: override?.description || param.description || param.schema.description,
  };

  if (override?.enum) {
    property.enum = override.enum;
  } else if (enumValues) {
    property.enum = enumValues;
  }

  return property;
}

/**
 * Find an operation in the OpenAPI spec
 */
function findOperation(
  spec: OpenAPISpec,
  apiPath: string,
  method: string
): OpenAPIOperation | null {
  const pathObj = spec.paths[apiPath];
  if (!pathObj) {
    console.warn(`Path not found in OpenAPI spec: ${apiPath}`);
    return null;
  }

  const operation = pathObj[method.toLowerCase()];
  if (!operation) {
    console.warn(`Method ${method} not found for path: ${apiPath}`);
    return null;
  }

  return operation;
}

/**
 * Generate a single MCP tool from config and OpenAPI spec
 */
function generateTool(
  toolConfig: ToolConfig,
  spec: OpenAPISpec
): GeneratedTool | null {
  const operation = findOperation(spec, toolConfig.path, toolConfig.method);
  if (!operation) {
    return null;
  }

  const properties: Record<string, MCPToolProperty> = {};
  const required: string[] = [];
  const excludeSet = new Set(toolConfig.excludeParameters || []);

  // Process parameters from OpenAPI
  if (operation.parameters) {
    for (const param of operation.parameters) {
      // Skip excluded parameters
      if (excludeSet.has(param.name)) {
        continue;
      }

      // Only include query parameters (not path parameters)
      if (param.in !== "query") {
        continue;
      }

      const override = toolConfig.parameterOverrides?.[param.name];
      properties[param.name] = convertParameterToProperty(param, override);

      if (param.required) {
        required.push(param.name);
      }
    }
  }

  return {
    name: toolConfig.name,
    description: toolConfig.description,
    usageHint: toolConfig.usageHint,
    inputSchema: {
      type: "object",
      properties,
      required,
    },
    apiEndpoint: toolConfig.path,
    httpMethod: toolConfig.method.toUpperCase(),
  };
}

/**
 * Convert tool name to various case formats
 */
function toCase(name: string, format: "camel" | "pascal" | "constant"): string {
  const parts = name.split(/[_-]/);  // Split on underscore or dash

  switch (format) {
    case "camel":
      return parts[0] + parts.slice(1).map(capitalize).join("");
    case "pascal":
      return parts.map(capitalize).join("");
    case "constant":
      return parts.map((p) => p.toUpperCase()).join("_");
  }
}

function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Generate TypeScript code for a tool
 */
function generateToolTypeScript(tool: GeneratedTool): string {
  const toolVarName = `${toCase(tool.name, "camel")}Tool`;
  const inputTypeName = `${toCase(tool.name, "pascal")}Input`;

  // Generate input interface
  const interfaceProps = Object.entries(tool.inputSchema.properties)
    .map(([name, prop]) => {
      const optional = !tool.inputSchema.required.includes(name) ? "?" : "";
      const tsType = prop.enum
        ? prop.enum.map((e) => `"${e}"`).join(" | ")
        : prop.type === "number"
        ? "number"
        : prop.type === "boolean"
        ? "boolean"
        : "string";
      return `  ${name}${optional}: ${tsType};`;
    })
    .join("\n");

  // Generate input schema properties
  const schemaProps = Object.entries(tool.inputSchema.properties)
    .map(([name, prop]) => {
      let propDef = `      ${name}: {\n        type: "${prop.type}"`;
      if (prop.description) {
        propDef += `,\n        description: ${JSON.stringify(prop.description)}`;
      }
      if (prop.enum) {
        propDef += `,\n        enum: ${JSON.stringify(prop.enum)}`;
      }
      propDef += "\n      }";
      return propDef;
    })
    .join(",\n");

  return `/**
 * ${tool.name} Tool (Auto-generated)
 *
 * ${tool.description}
 * ${tool.usageHint ? `\n * Usage hint: "${tool.usageHint}"` : ""}
 *
 * API Endpoint: ${tool.httpMethod} ${tool.apiEndpoint}
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const ${toolVarName}: Tool = {
  name: "${tool.name}",
  description: ${JSON.stringify(tool.description)},
  inputSchema: {
    type: "object",
    properties: {
${schemaProps}
    },
    required: ${JSON.stringify(tool.inputSchema.required)}
  }
};

export interface ${inputTypeName} {
${interfaceProps || "  // No parameters"}
}

/**
 * Execute the ${tool.name} tool
 */
export async function execute${toCase(tool.name, "pascal")}(
  input: ${inputTypeName}
): Promise<unknown> {
  const params = new URLSearchParams();
${Object.keys(tool.inputSchema.properties)
  .map(
    (name) =>
      `  if (input.${name} !== undefined) params.append("${name}", String(input.${name}));`
  )
  .join("\n")}

  const url = \`\${SPEARMINT_API_URL}${tool.apiEndpoint}\${params.toString() ? \`?\${params}\` : ""}\`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(\`Failed to execute ${tool.name}: \${response.statusText}\`);
  }

  return await response.json();
}
`;
}

/**
 * Generate the index file that exports all tools
 */
function generateIndexFile(tools: GeneratedTool[]): string {
  const imports = tools
    .map((tool) => {
      const varName = `${toCase(tool.name, "camel")}Tool`;
      const executeName = `execute${toCase(tool.name, "pascal")}`;
      const fileName = tool.name.replace(/_/g, "-");
      return `export { ${varName}, ${executeName} } from "./${fileName}.js";`;
    })
    .join("\n");

  const toolNames = tools
    .map((tool) => {
      const constName = toCase(tool.name, "constant");
      return `  ${constName}: "${tool.name}"`;
    })
    .join(",\n");

  return `/**
 * Generated MCP Tools Index
 *
 * Auto-generated by generate-tools.ts
 * DO NOT EDIT MANUALLY - changes will be overwritten
 */

${imports}

export const GENERATED_TOOL_NAMES = {
${toolNames}
} as const;

export type GeneratedToolName = typeof GENERATED_TOOL_NAMES[keyof typeof GENERATED_TOOL_NAMES];
`;
}

/**
 * Generate JSON file for AI optimizer
 */
function generateToolsJson(tools: GeneratedTool[]): string {
  const toolsObj: Record<string, unknown> = {};

  for (const tool of tools) {
    toolsObj[tool.name] = {
      description: tool.description,
      usageHint: tool.usageHint,
      inputSchema: tool.inputSchema,
    };
  }

  return JSON.stringify(toolsObj, null, 2);
}

/**
 * Main function
 */
async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const configArgIndex = args.indexOf("--config");
  const configPath =
    configArgIndex >= 0
      ? args[configArgIndex + 1]
      : path.join(__dirname, "tool-config.json");

  console.log("MCP Tool Generator");
  console.log("==================");
  console.log(`Config: ${configPath}`);
  console.log(`Dry run: ${dryRun}`);
  console.log("");

  // Load configuration
  const config: Config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
  console.log(`Loaded config with ${config.tools.length} tool definitions`);

  // Load OpenAPI spec
  const openApiPath = path.resolve(path.dirname(configPath), config.openApiPath);
  console.log(`Loading OpenAPI spec from: ${openApiPath}`);

  if (!fs.existsSync(openApiPath)) {
    console.error(`OpenAPI spec not found at: ${openApiPath}`);
    process.exit(1);
  }

  const spec: OpenAPISpec = JSON.parse(fs.readFileSync(openApiPath, "utf-8"));
  console.log(`OpenAPI spec loaded: ${spec.info.title} v${spec.info.version}`);
  console.log("");

  // Generate tools
  const generatedTools: GeneratedTool[] = [];

  for (const toolConfig of config.tools) {
    console.log(`Generating: ${toolConfig.name}`);
    const tool = generateTool(toolConfig, spec);

    if (tool) {
      generatedTools.push(tool);
      console.log(
        `  ✓ ${Object.keys(tool.inputSchema.properties).length} parameters`
      );
    } else {
      console.log(`  ✗ Failed to generate`);
    }
  }

  console.log("");
  console.log(`Generated ${generatedTools.length}/${config.tools.length} tools`);

  if (dryRun) {
    console.log("\n--- DRY RUN - No files written ---\n");
    console.log("Generated tools JSON:");
    console.log(generateToolsJson(generatedTools));
    return;
  }

  // Create output directory
  const outputDir = path.resolve(path.dirname(configPath), config.outputDir);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`Created output directory: ${outputDir}`);
  }

  // Write individual tool files
  for (const tool of generatedTools) {
    const fileName = tool.name.replace(/_/g, "-") + ".ts";
    const filePath = path.join(outputDir, fileName);
    const content = generateToolTypeScript(tool);
    fs.writeFileSync(filePath, content);
    console.log(`Wrote: ${fileName}`);
  }

  // Write index file
  const indexPath = path.join(outputDir, "index.ts");
  fs.writeFileSync(indexPath, generateIndexFile(generatedTools));
  console.log(`Wrote: index.ts`);

  // Write JSON for AI optimizer
  const jsonPath = path.join(outputDir, "tools.json");
  fs.writeFileSync(jsonPath, generateToolsJson(generatedTools));
  console.log(`Wrote: tools.json`);

  console.log("");
  console.log("Generation complete!");
}

main().catch((error) => {
  console.error("Error:", error);
  process.exit(1);
});
