#!/usr/bin/env python3
"""Check the extracted source snapshot and its complete local import closure."""

import hashlib
import json
from pathlib import Path
import re
import sys


def without_comments(text):
    out = []
    i, depth = 0, 0
    quoted = False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                i += 2
            else:
                if text[i] == '\n':
                    out.append('\n')
                i += 1
        elif not quoted and text.startswith('/-', i):
            depth = 1
            i += 2
            out.append(' ')
        elif not quoted and text.startswith('--', i):
            j = text.find('\n', i)
            i = len(text) if j < 0 else j
        else:
            c = text[i]
            out.append(c)
            if c == '"' and (i == 0 or text[i - 1] != '\\'):
                quoted = not quoted
            i += 1
    if depth:
        raise ValueError('Unterminated Lean block comment')
    return ''.join(out)


def imports(text):
    return [
        module
        for line in without_comments(text).splitlines()
        if re.match(r'^\s*(?:public\s+|private\s+)?import\s', line)
        for module in re.sub(
            r'^\s*(?:public\s+|private\s+)?import\s+(?:all\s+)?', '', line
        ).split()
    ]


def verify(root):
    record = json.loads((root / 'provenance/extraction.json').read_text())
    errors = []
    expected = record['source_files']
    for name, item in expected.items():
        path = root / name
        if not path.is_file() or path.is_symlink():
            errors.append(f'Missing or symlinked source: {name}')
        else:
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != item['sha256']:
                errors.append(f'Source differs from the recorded snapshot: {name}')
            git_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if len(data) != item['bytes'] or git_blob != item['git_blob']:
                errors.append(f'Source differs from the upstream Git blob: {name}')

    expected_lean = set(record['imports']) | {'DifferentialGeometry.lean', 'MeeksYau.lean'}
    actual_lean = {str(p.relative_to(root)) for p in (root / 'DifferentialGeometry').rglob('*.lean')}
    actual_lean |= {str(p.relative_to(root)) for p in root.glob('*.lean')}
    if expected_lean != actual_lean:
        errors.append(f'Lean file inventory mismatch: {sorted(expected_lean ^ actual_lean)}')

    graph, external = {}, set()
    for name in sorted(expected_lean & actual_lean):
        text = (root / name).read_text()
        dependencies = imports(text)
        if name in record['imports'] and dependencies != record['imports'][name]:
            errors.append(f'Import header differs from the recorded snapshot: {name}')
        graph[name] = []
        for module in dependencies:
            path = module.replace('.', '/') + '.lean'
            if path in expected_lean:
                graph[name].append(path)
            elif module.startswith('DifferentialGeometry') or module == 'MeeksYau':
                errors.append(f'Unresolved project import in {name}: {module}')
            else:
                external.add(module)
        code = without_comments(text)
        if re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b', code):
            errors.append(f'Proof admission or unsafe/native marker requires review: {name}')

    if external != set(record['external_direct_imports']):
        errors.append('External import inventory differs')
    if imports((root / 'DifferentialGeometry.lean').read_text()) != record['target_modules']:
        errors.append('The root aggregate does not import exactly the selected target modules')
    if (root / 'MeeksYau.lean').read_text() != 'import DifferentialGeometry\n':
        errors.append('Unexpected MeeksYau entry point')

    finished, visiting = set(), set()
    def visit(node):
        if node in visiting:
            errors.append(f'Import cycle at {node}')
            return
        if node in finished:
            return
        visiting.add(node)
        for child in graph.get(node, []):
            visit(child)
        visiting.remove(node)
        finished.add(node)
    visit('MeeksYau.lean')
    if finished != expected_lean:
        errors.append(f'Unreachable source modules: {sorted(expected_lean - finished)}')

    upstream_config = (root / 'provenance/upstream-lakefile.toml').read_text()
    expected_config = upstream_config.replace('name = "DifferentialGeometry"', 'name = "MeeksYau"', 1)
    expected_config = expected_config.replace('version = "0.1.5"', 'version = "0.1.0"', 1)
    expected_config = expected_config.replace('defaultTargets = ["DifferentialGeometry"]',
                                              'defaultTargets = ["MeeksYau"]', 1)
    expected_config += '\n[[lean_lib]]\nname = "MeeksYau"\n'
    if (root / 'lakefile.toml').read_text() != expected_config:
        errors.append('Lake configuration differs from the documented standalone adaptation')
    lock = json.loads((root / 'lake-manifest.json').read_text())
    original_lock = json.loads((root / 'provenance/upstream-lake-manifest.json').read_text())
    if lock['name'] != 'MeeksYau':
        errors.append('Lake package names disagree')
    if lock['packages'] != original_lock['packages']:
        errors.append('An external package pin differs from upstream')
    if (root / 'lean-toolchain').read_text().strip() != record['lean_toolchain']:
        errors.append('Lean toolchain differs from upstream')

    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(record['target_modules'])} target modules; {len(record['imports'])} upstream Lean modules.")
    print(f'PASS: {len(expected)} upstream files match their recorded SHA-256 hashes.')
    print(f'PASS: complete, acyclic, reachable project import closure; {len(external)} external direct imports.')
    print('PASS: toolchain and all external package pins match upstream; no proof-admission markers found.')
    print('These are source-packaging checks, not Lean compilation or an axiom audit.')
    return 0


if __name__ == '__main__':
    sys.exit(verify(Path(__file__).resolve().parents[1]))
