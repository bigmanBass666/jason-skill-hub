#!/usr/bin/env python3
"""Claude Project Mover — 会话历史同步工具 (worktree-aware)"""
import argparse, json, os, re, shutil, sys
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


# ---------------------------------------------------------------------------
# Worktree support
# ---------------------------------------------------------------------------

def find_worktree_dirs(project_path):
    """扫描 ~/.claude/projects/ 下 <主目录名>--claude-worktrees-* 目录。

    返回 [(dirname, full_path), ...] 列表，按目录名排序。
    """
    base = get_claude_projects_dir()
    main_dirname = get_project_dir_name(project_path)
    prefix = main_dirname + '--claude-worktrees-'
    worktrees = []
    if not os.path.exists(base):
        return worktrees
    for entry in sorted(os.listdir(base)):
        full = os.path.join(base, entry)
        if os.path.isdir(full) and entry.startswith(prefix):
            worktrees.append((entry, full))
    return worktrees


def map_worktree_dirname(old_dirname, new_project_path):
    """将旧 worktree 目录名映射到新项目的 worktree 目录名。

    输入: "D--Working-...--claude-worktrees-cli-logs", "D:\\Work\\Projects\\AK-Switch"
    输出: "D--Work-...--claude-worktrees-cli-logs"
    """
    suffix = old_dirname.split('--claude-worktrees-', 1)[1]
    new_main = get_project_dir_name(new_project_path)
    return f"{new_main}--claude-worktrees-{suffix}"


def copy_session_to_main(session_id, wt_src_dir, main_dst_dir, old_path, new_path):
    """把 worktree 里的会话也复制一份到主项目目录（让 -r 能找到）。

    复制 JSONL 和附件目录，然后修复 cwd 路径。
    如果目标已有同大小文件则跳过（幂等）。
    """
    src_jsonl = os.path.join(wt_src_dir, session_id + '.jsonl')
    if not os.path.exists(src_jsonl):
        return False
    os.makedirs(main_dst_dir, exist_ok=True)
    dst_jsonl = os.path.join(main_dst_dir, session_id + '.jsonl')
    if not (os.path.exists(dst_jsonl) and os.path.getsize(src_jsonl) == os.path.getsize(dst_jsonl)):
        shutil.copy2(src_jsonl, dst_jsonl)
    fix_cwd_in_jsonl(dst_jsonl, old_path, new_path)
    # Attachments
    src_sub = os.path.join(wt_src_dir, session_id)
    if os.path.isdir(src_sub):
        dst_sub = os.path.join(main_dst_dir, session_id)
        if not os.path.exists(dst_sub):
            shutil.copytree(src_sub, dst_sub)
    return True


def _find_session(session_id, old_path):
    """在主项目目录和 worktree 目录中搜索会话。

    Returns (found_in_dir, worktree_name_or_None)
    Raises FileNotFoundError if not found.
    """
    base = get_claude_projects_dir()
    main_dir = os.path.join(base, get_project_dir_name(old_path))

    main_jsonl = os.path.join(main_dir, session_id + '.jsonl')
    if os.path.exists(main_jsonl):
        return (main_dir, None)

    worktrees = find_worktree_dirs(old_path)
    for wt_name, wt_src in worktrees:
        wt_jsonl = os.path.join(wt_src, session_id + '.jsonl')
        if os.path.exists(wt_jsonl):
            return (wt_src, wt_name)

    raise FileNotFoundError(
        f'Session {session_id} not found in main or worktree dirs')


# ---------------------------------------------------------------------------
# Existing helpers
# ---------------------------------------------------------------------------

def count_files(directory):
    fcount = dcount = size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        dcount += len(dirnames)
        for fn in filenames:
            fcount += 1
            try:
                size += os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                pass
    return fcount, dcount, size


# UUID v4 pattern for session ID filenames (36 hex chars + 4 hyphens + '.jsonl')
_SESSION_ID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.jsonl$')


def _file_contains(filepath, text):
    """Check if file contains given text. Uses 'with' for proper handle management."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return text in f.read()


def find_jsonl_files(directory):
    result = []
    for dirpath, _, filenames in os.walk(directory):
        for fn in filenames:
            if fn.endswith('.jsonl'):
                result.append(os.path.join(dirpath, fn))
    return result


def fix_cwd_in_jsonl(filepath, old_path, new_path):
    old_esc = old_path.replace('\\', '\\\\')
    new_esc = new_path.replace('\\', '\\\\')
    if old_esc == new_esc:
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_esc not in content:
        return False
    content = content.replace(old_esc, new_esc)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def copy_and_fix(src_dir, dst_dir, old_path, new_path, dry_run=False):
    if dry_run:
        return (0, 0)
    os.makedirs(dst_dir, exist_ok=True)
    copied = fixed = 0
    for dirpath, dirnames, filenames in os.walk(src_dir):
        rel = os.path.relpath(dirpath, src_dir)
        dst_sub = os.path.join(dst_dir, rel)
        if not os.path.exists(dst_sub):
            os.makedirs(dst_sub)
        for fn in filenames:
            src_f = os.path.join(dirpath, fn)
            dst_f = os.path.join(dst_sub, fn)
            if os.path.exists(dst_f) and os.path.getsize(src_f) == os.path.getsize(dst_f):
                continue
            shutil.copy2(src_f, dst_f)
            copied += 1
            if fn.endswith('.jsonl') and fix_cwd_in_jsonl(dst_f, old_path, new_path):
                fixed += 1
    return (copied, fixed)


def _sync_one_session(session_id, src_dir, dst_dir, old_path, new_path):
    src_jsonl = os.path.join(src_dir, session_id + '.jsonl')
    if not os.path.exists(src_jsonl):
        print(f'FAIL: {src_jsonl}')
        return False
    os.makedirs(dst_dir, exist_ok=True)
    dst_jsonl = os.path.join(dst_dir, session_id + '.jsonl')
    shutil.copy2(src_jsonl, dst_jsonl)
    fix_cwd_in_jsonl(dst_jsonl, old_path, new_path)
    print(f'  JSONL: {dst_jsonl}')
    src_sub = os.path.join(src_dir, session_id)
    if os.path.isdir(src_sub):
        dst_sub = os.path.join(dst_dir, session_id)
        if os.path.exists(dst_sub):
            shutil.rmtree(dst_sub)
        shutil.copytree(src_sub, dst_sub)
        print(f'  Attachments: {dst_sub}')
    return True


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check(args):
    src, dst = resolve_history_dirs(args.old_path, args.new_path)
    if not os.path.exists(src):
        print(f'FAIL: {src}')
        sys.exit(1)

    fc, dc, sz = count_files(src)
    print(f'Source: {args.old_path}')
    print(f'  Dir: {src}')
    print(f'  Files: {fc}  |  Dirs: {dc}  |  Size: {sz / 1024 / 1024:.1f} MB')
    if os.path.exists(dst):
        fc2, dc2, sz2 = count_files(dst)
        print('')
        print(f'Dest: {args.new_path}')
        print(f'  Dir: {dst}')
        print(f'  Files: {fc2}  |  Dirs: {dc2}  |  Size: {sz2 / 1024 / 1024:.1f} MB')
        print('  Note: dest exists, migrate will merge')
    else:
        print('')
        print(f'Dest: {args.new_path}')
        print(f'  Dir: {dst}')
        print('  Status: (not yet created)')

    jfs = find_jsonl_files(src)
    old_esc = args.old_path.replace('\\', '\\\\')
    need_fix = sum(
        1 for jf in jfs if _file_contains(jf, old_esc))
    print('')
    print(f'JSONL sessions: {len(jfs)}')
    print(f'Need cwd fix: {need_fix}')
    print('')
    print(f'Summary: copy {fc} files, fix cwd paths to {dst}')
    if sz > 100 * 1024 * 1024:
        print(f'Note: large data ({sz / 1024 / 1024:.0f} MB), may take time')

    # Worktree info
    worktrees = find_worktree_dirs(args.old_path)
    if worktrees:
        print('')
        print(f'Worktrees: {len(worktrees)}')
        for wt_name, wt_src in worktrees:
            wt_fc, wt_dc, wt_sz = count_files(
                wt_src) if os.path.exists(wt_src) else (0, 0, 0)
            wt_jfs = find_jsonl_files(
                wt_src) if os.path.exists(wt_src) else []
            wt_dst_name = map_worktree_dirname(wt_name, args.new_path)
            wt_need_fix = sum(
                1 for jf in wt_jfs if _file_contains(jf, old_esc))
            print(f'  {wt_name}')
            print(f'    Source: {wt_src} ({wt_fc} files, {wt_sz / 1024 / 1024:.1f} MB)')
            print(f'    Dest:   {wt_dst_name}')
            print(f'    Sessions: {len(wt_jfs)}, need cwd fix: {wt_need_fix}')
    else:
        print('')
        print('Worktrees: none')


def cmd_migrate(args):
    src, dst = resolve_history_dirs(args.old_path, args.new_path)
    if not os.path.exists(src):
        print(f'FAIL: {src}')
        sys.exit(1)

    # Backup existing destination
    if os.path.exists(dst) and not args.no_backup:
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup = dst.rstrip('/\\') + '.backup.' + stamp
        if args.dry_run:
            print(f'[DRY-RUN] backup: {backup}')
        else:
            print(f'Backup: {backup}')
            shutil.copytree(dst, backup)

    # Main project migration
    if args.dry_run:
        print('[DRY-RUN] migrate:')
        print(f'  {src} -> {dst}')
        print(f'  cwd: {args.old_path} -> {args.new_path}')
    else:
        copied, fixed = copy_and_fix(src, dst, args.old_path, args.new_path)
        print('Main project:')
        print(f'  Copied: {copied}')
        print(f'  Fixed:  {fixed}')
        print(f'  Dest:   {dst}')

    # Worktree migration
    worktrees = find_worktree_dirs(args.old_path)
    if worktrees:
        if args.dry_run:
            print(f'\n[DRY-RUN] worktrees: {len(worktrees)}')
            for wt_name, wt_src in worktrees:
                wt_dst_name = map_worktree_dirname(wt_name, args.new_path)
                wt_dst = os.path.join(get_claude_projects_dir(), wt_dst_name)
                print(f'  {wt_name}')
                print(f'    {wt_src} -> {wt_dst}')
        else:
            print(f'\nWorktrees: {len(worktrees)}')
            for wt_name, wt_src in worktrees:
                wt_dst_name = map_worktree_dirname(wt_name, args.new_path)
                wt_dst = os.path.join(get_claude_projects_dir(), wt_dst_name)
                wt_copied, wt_fixed = copy_and_fix(
                    wt_src, wt_dst, args.old_path, args.new_path)
                print(f'  {wt_name}')
                print(f'    Copied: {wt_copied}, Fixed: {wt_fixed}')
                print(f'    Dest:   {wt_dst}')
                # Copy sessions to main project dir for -r discovery
                wt_jfs = find_jsonl_files(wt_src)
                for jf in wt_jfs:
                    sid = os.path.basename(jf)[:-6]
                    copy_session_to_main(
                        sid, wt_src, dst, args.old_path, args.new_path)
                    print(f'    Session {sid} copied to main (for -r)')


def cmd_sync_session(args):
    if args.session:
        session_id = args.session
        try:
            src_dir, wt_name = _find_session(session_id, args.old_path)
        except FileNotFoundError as e:
            print(f'FAIL: {e}')
            sys.exit(1)

        if wt_name:
            # Session is in a worktree — sync to both worktree and main
            new_wt_name = map_worktree_dirname(wt_name, args.new_path)
            dst_wt_dir = os.path.join(get_claude_projects_dir(), new_wt_name)
            dst_main_dir = os.path.join(
                get_claude_projects_dir(), get_project_dir_name(args.new_path))

            if args.dry_run:
                print(
                    f'[DRY-RUN] sync session {session_id} from worktree {wt_name}')
                print(f'  -> worktree: {dst_wt_dir}')
                print(f'  -> main:     {dst_main_dir}')
            else:
                print(f'Sync session {session_id} from worktree {wt_name}')
                _sync_one_session(
                    session_id, src_dir, dst_wt_dir, args.old_path, args.new_path)
                copy_session_to_main(
                    session_id, src_dir, dst_main_dir, args.old_path, args.new_path)
                print('  Also copied to main project dir (for -r)')
        else:
            dst_main_dir = os.path.join(
                get_claude_projects_dir(), get_project_dir_name(args.new_path))
            if args.dry_run:
                print(f'[DRY-RUN] sync session {session_id}')
                print(f'  -> main: {dst_main_dir}')
            else:
                print(f'Sync session: {session_id}')
                _sync_one_session(
                    session_id, src_dir, dst_main_dir, args.old_path, args.new_path)
        return

    # No session ID specified — sync latest from main project dir
    src, dst = resolve_history_dirs(args.old_path, args.new_path)
    if not os.path.exists(src):
        print(f'FAIL: {src}')
        sys.exit(1)

    candidates = []
    for fn in os.listdir(src):
        if _SESSION_ID_PATTERN.match(fn):
            fpath = os.path.join(src, fn)
            candidates.append((os.path.getmtime(fpath), fn))
    if not candidates:
        print('No sessions found')
        sys.exit(1)
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
        ('migrate', 'Full migration', ['old_path', 'new_path'],
         [('--dry-run', {'action': 'store_true'}),
          ('--no-backup', {'action': 'store_true'})]),
        ('sync-session', 'Sync single session', ['old_path', 'new_path'],
         [('--session', {}),
          ('--dry-run', {'action': 'store_true'})]),
    ]:
        sp = sub.add_parser(name, help=help_text)
        for a in pos_args:
            sp.add_argument(a)
        for a, kwargs in opt_args:
            sp.add_argument(a, **kwargs)
    args = p.parse_args()
    if not args.command:
        p.print_help()
        sys.exit(1)
    cmds = {'check': cmd_check, 'migrate': cmd_migrate,
            'sync-session': cmd_sync_session}
    cmds[args.command](args)


if __name__ == '__main__':
    main()