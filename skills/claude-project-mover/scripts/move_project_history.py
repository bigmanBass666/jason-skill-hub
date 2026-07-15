#!/usr/bin/env python3
"""Claude Project Mover — 会话历史同步工具"""
import argparse, json, os, shutil, sys
from datetime import datetime

def path_to_dirname(project_path):
    """将项目路径转换为 Claude Code 的历史目录名。

    转换规则（通过实测验证）：
    1. 盘符标记 ':\\' 或 ':/'  → '--'
    2. 路径分隔符 '\\' 或 '/'   → '-'
    3. 其余所有非 [a-zA-Z0-9] 字符 → '-'
    """
    n = project_path.replace(':\\', '--').replace('\\', '-')
    n = n.replace(':/', '--').replace('/', '-')
    return ''.join(c if c == '-' or 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9' else '-' for c in n)

def get_project_dir_name(project_path):
    return path_to_dirname(project_path)

def get_claude_projects_dir():
    config_dir = os.environ.get('CLAUDE_CONFIG_DIR')
    if config_dir:
        return os.path.join(config_dir, 'projects')
    return os.path.join(os.path.expanduser('~'), '.claude', 'projects')

def resolve_history_dirs(old_project, new_project):
    base = get_claude_projects_dir()
    return (os.path.join(base, get_project_dir_name(old_project)),
            os.path.join(base, get_project_dir_name(new_project)))

def count_files(directory):
    fcount = dcount = size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        dcount += len(dirnames)
        for fn in filenames:
            fcount += 1
            try: size += os.path.getsize(os.path.join(dirpath, fn))
            except OSError: pass
    return fcount, dcount, size

def find_jsonl_files(directory):
    result = []
    for dirpath, _, filenames in os.walk(directory):
        for fn in filenames:
            if fn.endswith('.jsonl'): result.append(os.path.join(dirpath, fn))
    return result

def fix_cwd_in_jsonl(filepath, old_path, new_path):
    old_esc = old_path.replace('\\', '\\\\')
    new_esc = new_path.replace('\\', '\\\\')
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    if old_esc not in content: return False
    content = content.replace(old_esc, new_esc)
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)
    return True

def copy_and_fix(src_dir, dst_dir, old_path, new_path, dry_run=False):
    if dry_run: return (0, 0)
    os.makedirs(dst_dir, exist_ok=True)
    copied = fixed = 0
    for dirpath, dirnames, filenames in os.walk(src_dir):
        rel = os.path.relpath(dirpath, src_dir)
        dst_sub = os.path.join(dst_dir, rel)
        if not os.path.exists(dst_sub): os.makedirs(dst_sub)
        for fn in filenames:
            src_f = os.path.join(dirpath, fn); dst_f = os.path.join(dst_sub, fn)
            if os.path.exists(dst_f) and os.path.getsize(src_f) == os.path.getsize(dst_f): continue
            shutil.copy2(src_f, dst_f); copied += 1
            if fn.endswith('.jsonl') and fix_cwd_in_jsonl(dst_f, old_path, new_path): fixed += 1
    return (copied, fixed)

def cmd_check(args):
    src, dst = resolve_history_dirs(args.old_path, args.new_path)
    if not os.path.exists(src): print(f'FAIL: {src}'); sys.exit(1)
    fc, dc, sz = count_files(src)
    print(f'Source: {args.old_path}')
    print(f'  Dir: {src}')
    print(f'  Files: {fc}  |  Dirs: {dc}  |  Size: {sz/1024/1024:.1f} MB')
    if os.path.exists(dst):
        fc2, dc2, sz2 = count_files(dst)
        print(f'')
        print(f'Dest: {args.new_path}')
        print(f'  Dir: {dst}')
        print(f'  Files: {fc2}  |  Dirs: {dc2}  |  Size: {sz2/1024/1024:.1f} MB')
        print(f'  Note: dest exists, migrate will merge')
    else:
        print(f'')
        print(f'Dest: {args.new_path}')
        print(f'  Dir: {dst}')
        print(f'  Status: (not yet created)')
    jfs = find_jsonl_files(src)
    old_esc = args.old_path.replace('\\', '\\\\')
    need_fix = sum(1 for jf in jfs if old_esc in open(jf, 'r', encoding='utf-8').read())
    print(f'')
    print(f'JSONL sessions: {len(jfs)}')
    print(f'Need cwd fix: {need_fix}')
    print(f'')
    print(f'Summary: copy {fc} files, fix cwd paths to {dst}')
    if sz > 100*1024*1024: print(f'Note: large data ({sz/1024/1024:.0f} MB), may take time')

def cmd_migrate(args):
    src, dst = resolve_history_dirs(args.old_path, args.new_path)
    if not os.path.exists(src): print(f'FAIL: {src}'); sys.exit(1)
    if os.path.exists(dst) and not args.no_backup:
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup = dst.rstrip('/\\') + '.backup.' + stamp
        if args.dry_run: print(f'[DRY-RUN] backup: {backup}')
        else: print(f'Backup: {backup}'); shutil.copytree(dst, backup)
    if args.dry_run:
        print(f'[DRY-RUN] migrate:')
        print(f'  {src} -> {dst}')
        print(f'  cwd: {args.old_path} -> {args.new_path}')
        return
    copied, fixed = copy_and_fix(src, dst, args.old_path, args.new_path)
    print(f'Done')
    print(f'  Copied: {copied}')
    print(f'  Fixed: {fixed}')
    print(f'  Dest: {dst}')

def _sync_one_session(session_id, src_dir, dst_dir, old_path, new_path):
    src_jsonl = os.path.join(src_dir, session_id + '.jsonl')
    if not os.path.exists(src_jsonl): print(f'FAIL: {src_jsonl}'); return False
    os.makedirs(dst_dir, exist_ok=True)
    dst_jsonl = os.path.join(dst_dir, session_id + '.jsonl')
    shutil.copy2(src_jsonl, dst_jsonl); fix_cwd_in_jsonl(dst_jsonl, old_path, new_path)
    print(f'  JSONL: {dst_jsonl}')
    src_sub = os.path.join(src_dir, session_id)
    if os.path.isdir(src_sub):
        dst_sub = os.path.join(dst_dir, session_id)
        if os.path.exists(dst_sub): shutil.rmtree(dst_sub)
        shutil.copytree(src_sub, dst_sub); print(f'  Attachments: {dst_sub}')
    return True

def cmd_sync_session(args):
    src, dst = resolve_history_dirs(args.old_path, args.new_path)
    if not os.path.exists(src): print(f'FAIL: {src}'); sys.exit(1)
    if args.session:
        if args.dry_run: print(f'[DRY-RUN] sync session {args.session}')
        else:
            print(f'Sync session: {args.session}')
            _sync_one_session(args.session, src, dst, args.old_path, args.new_path)
        return
    candidates = []
    for fn in os.listdir(src):
        if fn.endswith('.jsonl') and len(fn) == 42:
            fpath = os.path.join(src, fn)
            candidates.append((os.path.getmtime(fpath), fn))
    if not candidates: print('No sessions found'); sys.exit(1)
    candidates.sort(key=lambda x: x[0], reverse=True)
    session_id = candidates[0][1][:-6]
    if args.dry_run:
        print(f'[DRY-RUN] sync latest session: {session_id}')
        return
    print(f'Sync latest session: {session_id}')
    _sync_one_session(session_id, src, dst, args.old_path, args.new_path)

def main():
    p = argparse.ArgumentParser(description='Claude Project Mover')
    sub = p.add_subparsers(dest='command')
    for name, help_text, pos_args, opt_args in [
        ('check', 'Preview migration', ['old_path', 'new_path'], []),
        ('migrate', 'Full migration', ['old_path', 'new_path'], [('--dry-run', {'action': 'store_true'}), ('--no-backup', {'action': 'store_true'})]),
        ('sync-session', 'Sync single session', ['old_path', 'new_path'], [('--session', {}), ('--dry-run', {'action': 'store_true'})]),
    ]:
        sp = sub.add_parser(name, help=help_text)
        for a in pos_args: sp.add_argument(a)
        for a, kwargs in opt_args: sp.add_argument(a, **kwargs)
    args = p.parse_args()
    if not args.command: p.print_help(); sys.exit(1)
    cmds = {'check': cmd_check, 'migrate': cmd_migrate, 'sync-session': cmd_sync_session}
    cmds[args.command](args)

if __name__ == '__main__': main()