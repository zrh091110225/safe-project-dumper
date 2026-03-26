# safe-project-dumper

> Extract project knowledge into structured Markdown documents without copying source code.

![safe-project-dumper](https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/ccv2%2F2026-03-22%2FMiniMax-M2%2F2028668750999327086%2Fd786eb112a8c2f5f3e72c5b6b4536b7bbe3d9d83cb5a9c7aa3e59271688f1e54..png?Expires=1774249980&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=s%2Fhu49zs6Dh7CjAsWUxr2ZD0cqQ%3D)

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

## Offline QR Split Tool

This repository now includes an offline document splitting tool for multi-QR workflows:

- Script: `tools/offline_qr_bundle.py`
- Mode: pure offline, split one document into multiple QR payloads
- Ordering: filename + embedded index (`name__003-of-012`)
- Integrity: chunk CRC32 + full document SHA256

### Pack (split to chunks + payload files)

```bash
python3 tools/offline_qr_bundle.py pack \
  --input ./docs/ARCHITECTURE.md \
  --outdir ./out/qr-chunks \
  --name architecture \
  --max-qr-chars 1200 \
  --no-png
```

Notes:
- By default, the tool writes `.txt` payloads for each chunk.
- If you want PNG QR images, remove `--no-png` and install dependency:
  `pip install qrcode[pil]`

### Unpack (reassemble)

```bash
python3 tools/offline_qr_bundle.py unpack \
  --indir ./out/qr-chunks \
  --output ./out/recovered-ARCHITECTURE.md
```

## Why This Tool?

1. **Security Compliant** - Generates documentation, not code
2. **Knowledge Transfer** - Preserves design intent and business logic
3. **Interview Prep** - Great for preparing project summaries
4. **Onboarding** - Helps new team members understand the system
5. **Reverse Engineering** - Detailed enough to rebuild the project

## Disclaimer / 免责声明

This tool is provided **free of charge** for legitimate knowledge-transfer and documentation purposes only.

Any use involving unauthorized access, data theft, credential abuse, privacy violations, or any other illegal activity is strictly prohibited.  
Users are solely responsible for how they use this tool and for complying with all applicable laws, company policies, and contractual obligations.  
The authors and contributors assume **no liability** for any losses, damages, legal disputes, or consequences arising from misuse, including but not limited to theft of information or other unlawful conduct.

For stricter legal wording in Chinese, see [DISCLAIMER.md](./DISCLAIMER.md).

## License

MIT

## Author

Created for employees who need to transfer knowledge when leaving a company.
