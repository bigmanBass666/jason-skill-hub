#!/usr/bin/env python3
"""move_project_history.py — Claude Project Mover

Syncs ~/.claude/projects/ chat history when a project folder is moved.
ALL operations write to copies; original files are never modified in-place.
Moving/deleting originals requires explicit user confirmation.

Usage:
    python move_project_history.py check          <source> <target>
    python move_project_history.py migrate        <source> <target> [--dry-run] [--no-backup]
    python move_project_history.py sync-session   <source> <target> [--session <uuid>] [--dry-run]
    python move_project_history.py rollback       <snapshot.tar.gz> <target_dir>
    python move_project_history.py encode         <path>
"""
import argparse
import io
import json
import os
import shutil
import sys
import tarfile
from pathlib import Path

MAX_SANITIZED_LENGTH = 200


class PathEncoder:
    """Authority on Claude Code's project path → directory name encoding."""

    @staticmethod
    def encode(path: str) -> str:
        """Encode a Windows project path to ~/.claude/projects/ directory name.

        Encoding rules (in order):
            1. :\\ → --
            2. \\  → -
            3. .  → -
            4. _  → -
        Paths > 200 chars get -djb2hash suffix (matches leaked source).
        """
        path = path.replace("/", os.sep)
        sanitized = path.replace(":\\", "--").replace("\\", "-").replace(".", "-").replace("_", "-")
        if len(sanitized) <= MAX_SANITIZED_LENGTH:
            return sanitized
        h = PathEncoder._djb2(path)
        return sanitized[:MAX_SANITIZED_LENGTH] + "-" + h

    @staticmethod
    def _djb2(s: str) -> str:
        h = 0
        for c in s:
            h = ((h << 5) - h + ord(c)) & 0xFFFFFFFF
        return hex(h)[2:]


class FixResult:
    __slots__ = ("fixed", "errors")

    def __init__(self, fixed=0, errors=None):
        self.fixed = fixed
        self.errors = errors or []


class JsonlFixer:
    """Fix cwd fields in a JSONL file. Never modifies the original in-place."""

    def fix_file(self, filepath: Path, old_cwd: str, new_cwd: str, backup_path: Path = None):
        """Returns (FixResult, list_of_output_lines)."""
        original = filepath.read_text(encoding="utf-8")
        lines = original.splitlines(keepends=True)
        result = FixResult()
        out = []
        has_fixes = False

        for i, line in enumerate(lines):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                result.errors.append(f"{filepath.name}:{i+1}")
                out.append(line)
                continue
            if record.get("cwd") == old_cwd:
                record["cwd"] = new_cwd
                result.fixed += 1
                has_fixes = True
            out.append(json.dumps(record, ensure_ascii=False) + "\n")

        if has_fixes and backup_path and not backup_path.exists():
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            bio = io.BytesIO(original.encode("utf-8"))
            data = bio.getvalue()
            info = tarfile.TarInfo(name=filepath.name)
            info.size = len(data)
            bio.seek(0)
            with tarfile.open(backup_path, "w:gz") as tar:
                tar.addfile(info, bio)

        return result, out


class ProjectMigrator:
    """Orchestrate migration. Writes to dst_dir only; src_dir untouched."""

    def __init__(self, home: Path = None):
        self.home = home or Path.home()
        self.projects = self.home / ".claude" / "projects"

    def find_dir(self, cwd: str) -> Path | None:
        encoded = PathEncoder.encode(cwd)
        candidate = self.projects / encoded
        return candidate if candidate.is_dir() else None

    def check(self, source: str, target: str) -> dict:
        """Inspect only — no writes."""
        src_dir = self.find_dir(source)
        if src_dir is None:
            return {"exists": False, "files": [], "src_dir": None}
        files = sorted(f for f in src_dir.iterdir() if f.suffix == ".jsonl")
        return {
            "exists": True,
            "src_dir": str(src_dir),
            "dst_dir": str(self.projects / PathEncoder.encode(target)),
            "file_count": len(files),
            "files": [f.name for f in files],
        }

    def migrate(self, source: str, target: str, *, dry_run=False, no_backup=False) -> dict:
        """Write fixed copies to dst_dir. src_dir originals are never touched."""
        src_dir = self.find_dir(source)
        if src_dir is None:
            print(f"No history directory found for: {source}")
            return {"ok": False, "reason": "no_history"}

        dst_dir = self.projects / PathEncoder.encode(target)
        if dst_dir.exists() and dst_dir != src_dir:
            print(f"ERROR: target already exists: {dst_dir}")
            return {"ok": False, "reason": "target_exists"}

        old_cwd = os.path.normpath(source.rstrip("/\\"))
        new_cwd = os.path.normpath(target.rstrip("/\\"))
        fixer = JsonlFixer()
        total_fixed = 0
        total_errors = []
        results = []

        os.makedirs(dst_dir, exist_ok=True)

        for f in sorted(src_dir.iterdir()):
            if f.suffix != ".jsonl":
                continue
            backup = None if no_backup else dst_dir / (f.name + ".bak.gz")
            r, out_lines = fixer.fix_file(f, old_cwd, new_cwd, backup)
            results.append((f.name, r.fixed))
            total_fixed += r.fixed
            total_errors.extend(r.errors)

            if not dry_run:
                (dst_dir / f.name).write_text("".join(out_lines), encoding="utf-8")

        for name, count in results:
            tag = f"{count} fixed" if count else "no cwd match"
            print(f"  {name}: {tag}")

        if total_errors:
            print(f"WARNING: {len(total_errors)} corrupted JSONL lines skipped")
        print(f"Total: {total_fixed} cwd entries fixed across {len(results)} files")
        return {"ok": True, "fixed": total_fixed, "errors": total_errors}

    def rollback(self, snapshot: str, target_dir: str) -> bool:
        snap = Path(snapshot)
        target = Path(target_dir)
        if not snap.exists():
            print(f"Snapshot not found: {snap}")
            return False
        os.makedirs(target, exist_ok=True)
        with tarfile.open(snap, "r:gz") as t:
            t.extractall(target)
        print(f"Restored to {target}")
        return True

    def find_latest_jsonl(self, src_dir: Path) -> Path | None:
        """Return the most recently modified JSONL file in a directory."""
        jsonl_files = [f for f in src_dir.iterdir() if f.suffix == ".jsonl"]
        return max(jsonl_files, key=lambda f: f.stat().st_mtime) if jsonl_files else None

    def find_session_jsonl(self, src_dir: Path, session_uuid: str) -> Path | None:
        """Return a JSONL file matching a session UUID prefix."""
        for f in src_dir.iterdir():
            if f.suffix == ".jsonl" and f.stem.startswith(session_uuid):
                return f
        return None

    def sync_session(self, source: str, target: str, *, session: str = None, dry_run=False) -> dict:
        """Copy a single session JSONL file, fixing cwd. Does not reject existing target dir."""
        src_dir = self.find_dir(source)
        if src_dir is None:
            print(f"No history directory found for: {source}")
            return {"ok": False, "reason": "no_history"}

        dst_dir = self.projects / PathEncoder.encode(target)
        old_cwd = os.path.normpath(source.rstrip("/\\"))
        new_cwd = os.path.normpath(target.rstrip("/\\"))
        fixer = JsonlFixer()

        # Find the JSONL file (explicit session or latest)
        jsonl_file = None
        if session:
            jsonl_file = self.find_session_jsonl(src_dir, session)
            if jsonl_file is None:
                print(f"No session found matching: {session}")
                return {"ok": False, "reason": "session_not_found"}
        else:
            jsonl_file = self.find_latest_jsonl(src_dir)
            if jsonl_file is None:
                print(f"No JSONL files found in: {src_dir}")
                return {"ok": False, "reason": "no_jsonl_files"}

        # Backup existing target file before overwriting
        target_file = dst_dir / jsonl_file.name
        backup_path = dst_dir / (jsonl_file.name + ".bak.gz")
        if target_file.exists() and not backup_path.exists() and not dry_run:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            target_data = target_file.read_bytes()
            info = tarfile.TarInfo(name=target_file.name)
            info.size = len(target_data)
            with tarfile.open(backup_path, "w:gz") as tar:
                bio = io.BytesIO(target_data)
                tar.addfile(info, bio)

        # Fix cwd in source file (no internal backup — we already handled it above)
        r, out_lines = fixer.fix_file(jsonl_file, old_cwd, new_cwd)

        tag = f"{r.fixed} fixed" if r.fixed else "no cwd match"
        print(f"  {jsonl_file.name}: {tag}")

        if not dry_run:
            os.makedirs(dst_dir, exist_ok=True)
            (dst_dir / jsonl_file.name).write_text("".join(out_lines), encoding="utf-8")

        if r.errors:
            print(f"WARNING: {len(r.errors)} corrupted JSONL lines skipped")
        print(f"Total: {r.fixed} cwd entries fixed")
        return {"ok": True, "fixed": r.fixed, "errors": r.errors}


def build_cli():
    p = argparse.ArgumentParser(description="Claude Project Mover — copy-only history migration")
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("check", help="Check if history exists (read-only)")
    c.add_argument("source")
    c.add_argument("target")

    c = sub.add_parser("migrate", help="Write fixed copies to target dir (does not touch source)")
    c.add_argument("source")
    c.add_argument("target")
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--no-backup", action="store_true")

    c = sub.add_parser("rollback", help="Restore from backup snapshot")
    c.add_argument("snapshot")
    c.add_argument("target_dir")

    c = sub.add_parser("encode", help="Encode a path (debug/verify)")
    c.add_argument("path")

    c = sub.add_parser("sync-session", help="Copy a single session JSONL, fixing cwd")
    c.add_argument("source")
    c.add_argument("target")
    c.add_argument("--session", help="Session UUID (prefix match); defaults to latest")
    c.add_argument("--dry-run", action="store_true")

    return p


def main():
    parser = build_cli()
    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    migrator = ProjectMigrator()

    if args.cmd == "check":
        r = migrator.check(args.source, args.target)
        if r["exists"]:
            print(f"History dir: {r['src_dir']}")
            print(f"Target dir:  {r['dst_dir']}")
            print(f"Files: {r['file_count']}")
            for f in r["files"]:
                print(f"  {f}")
        else:
            print("No history directory found. Nothing to migrate.")

    elif args.cmd == "migrate":
        tag = "[dry-run] " if args.dry_run else ""
        print(f"{tag}Writing copies to target dir (source left intact): {args.source} -> {args.target}")
        r = migrator.migrate(args.source, args.target, dry_run=args.dry_run, no_backup=args.no_backup)
        if r["ok"]:
            print("Verify the target dir, then run Move-Item and delete old history when confirmed.")
        sys.exit(0 if r["ok"] else 1)

    elif args.cmd == "rollback":
        ok = migrator.rollback(args.snapshot, args.target_dir)
        sys.exit(0 if ok else 1)

    elif args.cmd == "encode":
        print(PathEncoder.encode(args.path))

    elif args.cmd == "sync-session":
        tag = "[dry-run] " if args.dry_run else ""
        print(f"{tag}Syncing session to target dir (source left intact): {args.source} -> {args.target}")
        r = migrator.sync_session(args.source, args.target, session=args.session, dry_run=args.dry_run)
        sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
