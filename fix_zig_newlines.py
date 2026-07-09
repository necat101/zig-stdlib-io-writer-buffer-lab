#!/usr/bin/env python3
"""Fix stray literal newlines inside Zig string literals in generated case files.
Workaround for generate_cases.py bug where std.debug.print("...\n", ...)
emits a real newline instead of \n in the Zig output.
Safe to run multiple times – idempotent.
"""
import pathlib, sys
root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("generated_cases")
fixed = 0
for p in root.glob("*.zig"):
    s = p.read_text()
    out=[]; in_str=False; esc=False
    for ch in s:
        if ch == '"' and not esc:
            in_str = not in_str; out.append(ch)
        elif in_str and ch == '\n':
            out.append('\\n')
        else:
            out.append(ch)
        esc = (ch == '\\' and not esc)
    s2 = ''.join(out)
    if s != s2:
        p.write_text(s2)
        fixed += 1
        print(f"fixed {p.name}")
if fixed:
    print(f"Fixed {fixed} file(s)")
else:
    print("No fixes needed")
