---
name: project-dumper
version: 1.1.0
description: |
  Extract project knowledge into structured Markdown documents. Analyzes source code
  to generate architecture docs, API docs, database design, and flow diagrams.
  Use when: "dump project", "extract project docs", "generate project knowledge",
  "项目文档", or when you need to extract project structure and design.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# project-dumper

Generate structured Markdown documentation from project source code. This skill helps extract project knowledge (architecture, API, database, flows) without copying source code.

## Usage

```
/project-dumper [--output DIR] [--project PATH]

Examples:
/project-dumper                                    # Use current directory
/project-dumper --output ./docs                   # Output to ./docs
/project-dumper --project /path/to/project        # Analyze specific project
/project-dumper -o ./my-docs -p ./my-project    # Full options
```

## Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| --output | -o | Output directory for generated docs | ./project-docs |
| --project | -p | Project directory to analyze | Current directory |

## Workflow

Follow these phases to analyze the project:

### Phase 1: Project Structure Analysis

1. Scan the project directory to understand:
   - Project type (language, framework)
   - Directory structure
   - Key configuration files (package.json, pom.xml, requirements.txt, etc.)
   - Module/package organization

2. Identify the main entry points and key modules

### Phase 2: API & Database Analysis

For each API layer found (REST controllers, routes, endpoints):
- List all endpoints with HTTP method, path, and description
- Document request/response formats

For each database layer found (entities, models, schemas):
- List all entities/tables with fields and relationships
- Document primary keys, indexes, and constraints

### Phase 3: Architecture & Design Analysis

Analyze and document:
- Layered architecture (presentation, business, data, etc.)
- Design patterns used
- Technology stack and why
- Key architectural decisions

### Phase 4: Core Flows & Diagrams

Document key business flows:
- User interactions
- Data processing pipelines
- External integrations

Generate Mermaid diagrams for:
- System architecture
- Data flow
- Sequence diagrams for key operations

## Output Format

Generate these Markdown files in the output directory:

1. **README.md** - Project overview, tech stack, quick start
2. **ARCHITECTURE.md** - Architecture design, layers, patterns
3. **API.md** - API endpoints documentation
4. **DATABASE.md** - Database schema and models
5. **FLOWS.md** - Business flows with Mermaid diagrams

## Guidelines

- **DO NOT copy source code** - Only summarize and describe
- **Use Mermaid diagrams** for visual representation
- **Include code snippets only as examples**, not full files
- **Focus on design intent** - Why was it built this way?
- **Be concise** - Use bullet points and tables
- **Language**: Use the same language as the project comments/docs, default to English
- **Depth**: For architecture docs, include specific code examples, configuration, and implementation details that enable reverse engineering

## Output Directory

**Default**: `./project-docs/`

**Custom output**:
```bash
# Example 1: Output to current directory's docs folder
/project-dumper -o ./docs

# Example 2: Output to home directory
/project-dumper -o ~/project-docs

# Example 3: Absolute path
/project-dumper -o /Users/name/Documents/my-project-docs
```

**Note**: The output directory will be created if it doesn't exist.

## Edge Cases

- If project has no clear API layer: Document what interfaces the project exposes
- If project has no database: Skip DATABASE.md
- If project is too large: Prioritize main modules, note that full analysis requires multiple runs
- If language/framework not recognized: Ask user for clarification
- If output directory is not writable: Report error with suggested fix
