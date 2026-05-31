import sys

def count_chars(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    char_count = len(content)
    line_count = content.count('\n') + 1
    print(f"File: {filepath}")
    print(f"Characters: {char_count}")
    print(f"Lines: {line_count}")
    if char_count > 10000:
        print(f"WARNING: Exceeds 10,000 character limit by {char_count - 10000}")
    else:
        print(f"Within 10,000 character limit (remaining: {10000 - char_count})")
    return char_count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python char_count.py <filepath>")
        sys.exit(1)
    count_chars(sys.argv[1])
