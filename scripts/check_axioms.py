#!/usr/bin/env python3
"""Print selected theorem types and reject nonstandard transitive axioms after a build."""

from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
THEOREMS = [
    'DifferentialGeometry.Geometry.exists_morrey_disk',
    'DifferentialGeometry.Geometry.exists_morrey_disk_of_compact',
    'DifferentialGeometry.Geometry.exists_confined_morrey_disk_R7E',
    'DifferentialGeometry.Geometry.closed_disk_immersion_of_completed_profile',
    'DifferentialGeometry.Geometry.IsMorreyDisk.isEmbedding_of_no_transverse',
    'DifferentialGeometry.Geometry.prepared_least_area_embedded_R12',
    'DifferentialGeometry.Geometry.MinimalSurface.isExteriorSpanningDisk_of_morrey_AT',
    'DifferentialGeometry.Geometry.MinimalSurface.isExteriorSpanningDisk.attains_positive_leastExteriorDiskArea_of_morrey_open',
]


def main():
    code = 'import MeeksYau\n\n'
    code += '\n'.join(f'#check @{name}\n#print axioms {name}' for name in THEOREMS)
    with tempfile.TemporaryDirectory(prefix='meeks-yau-axioms-') as directory:
        driver = Path(directory) / 'Check.lean'
        driver.write_text(code + '\n')
        result = subprocess.run(['lake', 'env', 'lean', str(driver)], cwd=ROOT,
                                text=True, capture_output=True)
    print(result.stdout, end='')
    print(result.stderr, end='')
    if result.returncode:
        return result.returncode
    closures = re.findall(r'depends on axioms:\s*\[([^\]]*)\]', result.stdout)
    if len(closures) != len(THEOREMS):
        print('FAIL: did not receive an axiom closure for every selected theorem.')
        return 1
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for name, closure in zip(THEOREMS, closures):
        unexpected = {x.strip() for x in closure.split(',') if x.strip()} - allowed
        if unexpected:
            print(f'FAIL: {name} depends on unexpected axioms: {sorted(unexpected)}')
            return 1
    if re.search(r'\b(?:warning|error):', result.stdout + result.stderr):
        print('FAIL: Lean emitted a diagnostic.')
        return 1
    print('PASS: the eight selected declarations use only the allowed foundational axioms.')
    print('Their explicit hypotheses remain part of the theorem statements printed above.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
