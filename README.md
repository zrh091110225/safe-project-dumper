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

### How It Works

1. Read the input document as bytes
2. Compress once (zlib)
3. Split compressed bytes into chunks that fit `--max-qr-chars`
4. Write one payload per chunk (`.txt`, and optional `.png`)
5. Rebuild by collecting all chunks, validating CRC/SHA256, then decompressing

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
- For camera scanning stability, start with `--max-qr-chars 600~1200`.

### Pack Parameters

| Param | Description | Default |
|------|-------------|---------|
| `--input` | Input document path | Required |
| `--outdir` | Output directory for chunk files | Required |
| `--name` | Chunk filename prefix | input filename stem |
| `--max-qr-chars` | Max characters per QR payload | `1200` |
| `--compress-level` | zlib compression level (`0-9`) | `9` |
| `--ecc` | QR error correction (`L/M/Q/H`) | `M` |
| `--no-png` | Write text payload only (no PNG) | disabled |

### Unpack (reassemble)

```bash
python3 tools/offline_qr_bundle.py unpack \
  --indir ./out/qr-chunks \
  --output ./out/recovered-ARCHITECTURE.md
```

Optional:
- `--doc-id <id>` to rebuild only one target document when multiple docs are mixed in one directory.

### Output Files

- `name__001-of-016.txt`: QR payload text for one chunk
- `name__001-of-016.png`: QR image (only when not using `--no-png`)
- `name__manifest.json`: metadata summary (chunk count, config)

### Verification and Failure Cases

- Missing chunks: unpack fails with a clear missing-index error
- Mixed documents: unpack fails on metadata mismatch
- Tampered payload: unpack fails on chunk CRC or doc SHA256 mismatch

### End-to-End Example

```bash
# pack
python3 tools/offline_qr_bundle.py pack \
  --input README.md \
  --outdir ./out/qr-demo \
  --name readme \
  --max-qr-chars 350 \
  --no-png

# rebuild
python3 tools/offline_qr_bundle.py unpack \
  --indir ./out/qr-demo \
  --output ./out/recovered-README.md

# verify
shasum -a 256 README.md ./out/recovered-README.md
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
