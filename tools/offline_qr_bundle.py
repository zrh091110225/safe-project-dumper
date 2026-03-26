#!/usr/bin/env python3
"""Offline document pack/unpack tool for multi-QR workflows.

Features:
- compress whole file then split into chunks
- each chunk carries doc_id + total + index + chunk CRC32 + doc SHA256
- writes text payloads per chunk (QR-ready)
- optional PNG QR output (requires qrcode library)
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import zlib
from dataclasses import dataclass
from typing import Iterable, List, Sequence


SCHEMA_VERSION = 1
FILE_PATTERN = re.compile(r"^(?P<name>.+)__(?P<idx>\d+)-of-(?P<total>\d+)\.txt$")


class BundleError(Exception):
    pass


@dataclass
class ChunkRecord:
    v: int
    doc: str
    n: int
    i: int
    h: str
    c: str
    d: str

    @classmethod
    def from_json(cls, payload: str) -> "ChunkRecord":
        try:
            obj = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise BundleError(f"Invalid JSON chunk: {exc}") from exc

        required = {"v", "doc", "n", "i", "h", "c", "d"}
        missing = required - set(obj)
        if missing:
            raise BundleError(f"Chunk missing fields: {sorted(missing)}")

        return cls(
            v=int(obj["v"]),
            doc=str(obj["doc"]),
            n=int(obj["n"]),
            i=int(obj["i"]),
            h=str(obj["h"]),
            c=str(obj["c"]),
            d=str(obj["d"]),
        )

    def to_json(self) -> str:
        obj = {
            "v": self.v,
            "doc": self.doc,
            "n": self.n,
            "i": self.i,
            "h": self.h,
            "c": self.c,
            "d": self.d,
        }
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=True)


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64url_decode(text: str) -> bytes:
    padding = "=" * ((4 - len(text) % 4) % 4)
    try:
        return base64.urlsafe_b64decode(text + padding)
    except binascii.Error as exc:
        raise BundleError(f"Base64URL decode failed: {exc}") from exc


def _crc32_hex(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def _doc_id(doc_hash: str) -> str:
    return doc_hash[:12]


def _split_bytes(data: bytes, chunk_size: int) -> List[bytes]:
    if chunk_size <= 0:
        raise BundleError("chunk_size must be > 0")
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)] or [b""]


def _build_payloads(comp: bytes, doc_hash: str, chunk_size: int) -> List[str]:
    doc = _doc_id(doc_hash)
    chunks = _split_bytes(comp, chunk_size)
    total = len(chunks)
    payloads: List[str] = []
    for idx, chunk in enumerate(chunks, start=1):
        rec = ChunkRecord(
            v=SCHEMA_VERSION,
            doc=doc,
            n=total,
            i=idx,
            h=doc_hash,
            c=_crc32_hex(chunk),
            d=_b64url_encode(chunk),
        )
        payloads.append(rec.to_json())
    return payloads


def _max_payload_len(payloads: Sequence[str]) -> int:
    return max((len(x) for x in payloads), default=0)


def choose_chunk_size(comp: bytes, doc_hash: str, max_qr_chars: int) -> int:
    if max_qr_chars < 256:
        raise BundleError("max_qr_chars too small, suggest >= 256")

    left, right = 1, max(1, len(comp))
    best = 1
    while left <= right:
        mid = (left + right) // 2
        payloads = _build_payloads(comp, doc_hash, mid)
        if _max_payload_len(payloads) <= max_qr_chars:
            best = mid
            left = mid + 1
        else:
            right = mid - 1
    return best


def pack_bytes(raw: bytes, max_qr_chars: int = 1200, level: int = 9) -> List[str]:
    comp = zlib.compress(raw, level)
    doc_hash = hashlib.sha256(raw).hexdigest()
    chunk_size = choose_chunk_size(comp, doc_hash, max_qr_chars)
    payloads = _build_payloads(comp, doc_hash, chunk_size)

    if _max_payload_len(payloads) > max_qr_chars:
        raise BundleError("Cannot fit payload under max_qr_chars; increase the limit")

    return payloads


def _parse_chunk_records(payloads: Iterable[str]) -> List[ChunkRecord]:
    records = [ChunkRecord.from_json(x) for x in payloads]
    if not records:
        raise BundleError("No chunks provided")

    first = records[0]
    for rec in records:
        if rec.v != SCHEMA_VERSION:
            raise BundleError(f"Unsupported schema version: {rec.v}")
        if rec.doc != first.doc or rec.h != first.h or rec.n != first.n:
            raise BundleError("Chunk metadata mismatch; mixed documents detected")

    indices = {rec.i for rec in records}
    expected = set(range(1, first.n + 1))
    if indices != expected:
        missing = sorted(expected - indices)
        dup = len(records) - len(indices)
        msg = []
        if missing:
            msg.append(f"Missing chunks {missing}")
        if dup > 0:
            msg.append(f"Duplicate chunks: {dup}")
        raise BundleError("; ".join(msg) or "Invalid chunk indices")

    records.sort(key=lambda r: r.i)
    return records


def unpack_payloads(payloads: Iterable[str]) -> bytes:
    records = _parse_chunk_records(payloads)
    comp_parts: List[bytes] = []
    for rec in records:
        chunk = _b64url_decode(rec.d)
        if _crc32_hex(chunk) != rec.c:
            raise BundleError(f"Chunk {rec.i} CRC check failed")
        comp_parts.append(chunk)

    comp = b"".join(comp_parts)
    try:
        raw = zlib.decompress(comp)
    except zlib.error as exc:
        raise BundleError(f"Decompress failed: {exc}") from exc

    doc_hash = hashlib.sha256(raw).hexdigest()
    if doc_hash != records[0].h:
        raise BundleError("Document SHA256 mismatch")

    return raw


def _write_qr_png(payload: str, path: pathlib.Path, ecc: str) -> None:
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q
    except Exception as exc:  # noqa: BLE001
        raise BundleError("PNG generation needs qrcode library: pip install qrcode[pil]") from exc

    ecc_map = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }
    if ecc not in ecc_map:
        raise BundleError("ecc must be one of L/M/Q/H")

    qr = qrcode.QRCode(
        version=None,
        error_correction=ecc_map[ecc],
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)


def _ensure_qrcode(auto_install: bool) -> tuple[bool, str | None]:
    try:
        import qrcode  # noqa: F401
        return True, None
    except Exception:
        pass

    if not auto_install:
        return False, "qrcode library not found; writing .txt payloads only"

    cmd = [sys.executable, "-m", "pip", "install", "qrcode[pil]"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        detail = tail[-1] if tail else "unknown pip error"
        return False, f"auto-install failed ({detail}); writing .txt payloads only"

    try:
        import qrcode  # noqa: F401
        return True, None
    except Exception:
        return False, "auto-install completed but qrcode import still failed; writing .txt payloads only"


def cmd_pack(args: argparse.Namespace) -> int:
    input_path = pathlib.Path(args.input)
    out_dir = pathlib.Path(args.outdir)
    name = args.name or input_path.stem

    raw = input_path.read_bytes()
    payloads = pack_bytes(raw, max_qr_chars=args.max_qr_chars, level=args.compress_level)

    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(payloads)
    width = max(3, len(str(total)))

    png_enabled = not args.no_png
    png_error: str | None = None

    if png_enabled:
        png_enabled, png_error = _ensure_qrcode(auto_install=args.auto_install_qrcode)
        if png_error:
            print(f"Warning: {png_error}", file=sys.stderr)

    for idx, payload in enumerate(payloads, start=1):
        base = f"{name}__{idx:0{width}d}-of-{total:0{width}d}"
        txt_path = out_dir / f"{base}.txt"
        txt_path.write_text(payload, encoding="utf-8")

        if png_enabled:
            png_path = out_dir / f"{base}.png"
            _write_qr_png(payload, png_path, args.ecc)

    manifest = {
        "name": name,
        "input": str(input_path),
        "chunks": total,
        "max_qr_chars": args.max_qr_chars,
        "compress_level": args.compress_level,
        "ecc": args.ecc,
        "png_enabled": png_enabled,
    }
    if png_error:
        manifest["png_note"] = png_error
    (out_dir / f"{name}__manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Pack complete: {total} chunks -> {out_dir}")
    return 0


def _read_payloads_from_dir(indir: pathlib.Path, doc: str | None) -> List[str]:
    payloads: List[str] = []
    for path in sorted(indir.glob("*.txt")):
        m = FILE_PATTERN.match(path.name)
        if not m:
            continue
        payload = path.read_text(encoding="utf-8").strip()
        if not payload:
            continue
        if doc:
            rec = ChunkRecord.from_json(payload)
            if rec.doc != doc:
                continue
        payloads.append(payload)

    if not payloads:
        raise BundleError("No valid .txt chunk payloads found")

    return payloads


def cmd_unpack(args: argparse.Namespace) -> int:
    in_dir = pathlib.Path(args.indir)
    out_file = pathlib.Path(args.output)

    payloads = _read_payloads_from_dir(in_dir, args.doc_id)
    raw = unpack_payloads(payloads)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(raw)

    print(f"Rebuild complete: {out_file} ({len(raw)} bytes)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline multi-QR pack/unpack")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pack = sub.add_parser("pack", help="Pack file into chunk payloads")
    p_pack.add_argument("--input", required=True, help="Input file path")
    p_pack.add_argument("--outdir", required=True, help="Output directory")
    p_pack.add_argument("--name", help="Output name prefix, default is input stem")
    p_pack.add_argument("--max-qr-chars", type=int, default=1200, help="Max chars per QR payload")
    p_pack.add_argument("--compress-level", type=int, default=9, help="zlib level 0-9")
    p_pack.add_argument("--ecc", default="M", choices=["L", "M", "Q", "H"], help="QR error correction level")
    p_pack.add_argument("--no-png", action="store_true", help="Only write .txt payloads")
    p_pack.add_argument(
        "--auto-install-qrcode",
        action="store_true",
        help="Auto install qrcode[pil] when PNG generation is requested and dependency is missing",
    )
    p_pack.set_defaults(func=cmd_pack)

    p_unpack = sub.add_parser("unpack", help="Rebuild file from chunk payloads")
    p_unpack.add_argument("--indir", required=True, help="Input chunk directory")
    p_unpack.add_argument("--output", required=True, help="Output rebuilt file")
    p_unpack.add_argument("--doc-id", help="Optional doc_id filter")
    p_unpack.set_defaults(func=cmd_unpack)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except BundleError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
