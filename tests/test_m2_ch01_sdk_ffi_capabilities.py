"""Read-only SDK ABI/FFI capability audit for QGF Marathon 2 Chapter 1."""
from __future__ import annotations
import argparse
import ast
from pathlib import Path
import sys


def audit(sdk: Path) -> int:
    path = sdk / 'qrvm' / 'native_ffi.py'
    if not path.is_file():
        print('BLOCKED: missing SDK qrvm/native_ffi.py')
        return 2
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    table = next((n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == '_TYPES' for t in n.targets)), None)
    if table is None:
        print('BLOCKED: SDK scalar ABI table not found')
        return 2
    types = set()
    if isinstance(table.value, ast.Dict):
        types = {k.value for k in table.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    required = {'i32', 'u32', 'i64', 'u64', 'f32', 'f64'}
    print('SDK:', sdk)
    print('Native scalar types:', ', '.join(sorted(types)))
    if not required.issubset(types):
        print('BLOCKED: expected scalar ABI baseline missing')
        return 2
    print('PASS: basic scalar ABI adapter present')
    print('BLOCKED: direct C bool signature unsupported' if 'bool' not in types
          else 'AVAILABLE: bool scalar appears in ABI table; frontend still requires validation')
    print('UNTESTED: Visual Quar source-level extern declaration -> QRVM native call')
    print('UNTESTED: actual SDL3 initialization and shutdown')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    sys.exit(audit(parser.parse_args().sdk.expanduser().resolve()))
