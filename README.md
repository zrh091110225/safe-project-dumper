# safe-project-dumper

> Extract project knowledge into structured Markdown documents without copying source code.

A AI coding assistant skill that analyzes source code to generate architecture docs, API docs, database design, and flow diagrams. Designed for knowledge transfer when employees leave a company - they can take the documentation, not the code.

## Supported Platforms

- **Claude Code** - Use `/project-dumper` or describe your need
- **Codex** - Use `/project-dumper` or describe your need
- **GStack** - Use `/project-dumper` or describe your need

## Use Case

When employees leave a company, they often can't copy source code due to security policies. This tool helps them extract:

- Architecture design
- API documentation
- Database schema
- Business flows
- Design highlights

This is **knowledge transfer**, not code theft.

## Features

- **Automatic Analysis** - Scans project structure, detects language/framework
- **Multi-document Output** - README, ARCHITECTURE, API, DATABASE, FLOWS
- **Mermaid Diagrams** - Architecture diagrams, flow charts, state machines
- **AI Skill** - Easy to use with AI coding assistants (Claude Code, Codex, GStack)
- **No Code Copying** - Only generates documentation, not source code
- **Reverse Engineering Friendly** - Detailed enough to rebuild the project

## Usage

```bash
# Basic usage (analyze current directory)
/project-dumper

# Specify output directory
/project-dumper -o ./docs

# Specify project directory
/project-dumper -p /path/to/project -o ./output

# Full options
/project-dumper --project /path/to/project --output ./docs
```

## Output Files

The tool generates these Markdown files:

| File | Description |
|------|-------------|
| `README.md` | Project overview, tech stack |
| `ARCHITECTURE.md` | Architecture design, layers, patterns |
| `API.md` | API endpoints documentation |
| `DATABASE.md` | Database schema and models |
| `FLOWS.md` | Business flows with Mermaid diagrams |

## Supported Projects

- Java / Spring Boot
- JavaScript / TypeScript / Node.js
- Python
- Go
- And more...

## Examples

See the `examples/` directory for sample output.

- [mall-ecommerce](./examples/mall/) - Spring Boot e-commerce system
- [boss-auto-apply](./examples/boss-auto-apply/) - Chrome extension

## Installation

### For Claude Code

```bash
# Copy SKILL.md to your Claude Code skills directory
cp SKILL.md ~/.claude/skills/project-dumper/
```

### For Codex

```bash
# Copy SKILL.md to your Codex skills directory
cp SKILL.md ~/.codex/skills/project-dumper/
```

### For GStack

```bash
# Copy to GStack skills directory
cp SKILL.md ~/.claude/skills/project-dumper/
```

## Technical Details

- **Language**: Skill definition (works with Claude Code, Codex, GStack)
- **Framework**: AI Assistant Skill API
- **Output**: Markdown files with Mermaid diagrams

## Why This Tool?

1. **Security Compliant** - Generates documentation, not code
2. **Knowledge Transfer** - Preserves design intent and business logic
3. **Interview Prep** - Great for preparing project summaries
4. **Onboarding** - Helps new team members understand the system
5. **Reverse Engineering** - Detailed enough to rebuild the project

## License

MIT

## Author

Created for employees who need to transfer knowledge when leaving a company.
