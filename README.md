# Meeks–Yau formalization components in Lean

This repository isolates the minimal-surface development used for the Meeks–Yau work in
[DifferentialGeometry](https://github.com/qinz1yang/differential-geometry), together with every
project source module it imports. The source snapshot is commit
[`fd2f07fba4c6c102ba626c59153ad98da8f0d442`](https://github.com/qinz1yang/differential-geometry/tree/fd2f07fba4c6c102ba626c59153ad98da8f0d442),
dated October 10, 2026. The extraction was prepared on November 11, 2026.

**This is an extraction of the existing formalized components. It is not a new certification
of the full classical Meeks–Yau theorem.** In this snapshot, the embedding theorem takes an
explicit no-transverse-collision hypothesis, and the tower theorem takes explicit supplier
hypotheses. Those statements and proofs are preserved unchanged. The
[proof-status notes](provenance/PROOF_STATUS.md) identify the distinction.

## Contents

- 397 target modules covering Plateau existence, regularity, embeddedness, confinement,
  fixed-boundary least-area disks, and their variation and stability results.
- 3,609 upstream Lean modules in the complete transitive import closure, about 55 MiB of source.
  The original module paths and namespaces are preserved.
- The upstream licenses, attribution, and relevant third-party provenance records.
- Lean `v4.35.0-rc3` and an unchanged external dependency lock, including Mathlib commit
  `c55e6e786f49471c72fbddbec5415808896aec1e`.

The selection comprises all registered modules under
`DifferentialGeometry/Geometry/MinimalSurface/` except its `Width/` directory, followed by
their dependencies. The Geometrization and Poincaré endpoint modules and the cusp-specific
applications are excluded. Some shared differential-geometric helpers happen to live under
`Geometry/Flow/RicciFlow/`; they remain because the retained source imports them.

This is a module-level extraction: complete source files are kept, including other declarations
in a required dependency file. It does not rename or prune individual declarations. There is no
dependency on the parent DifferentialGeometry repository at build time. Mathlib and its own
dependencies are ordinary pinned Lake dependencies, fetched when setting up the project.

## Build and import

Install Lean through [elan](https://github.com/leanprover/elan), then run from this directory:

```sh
lake exe cache get
lake build
```

The toolchain file selects the exact Lean release, and `lake-manifest.json` pins all external
packages. The first command retrieves Mathlib's build cache; the second builds the extracted
library. This repository distributes source, not machine-specific compiled artifacts.

Use the complete extracted development with:

```lean
import MeeksYau
```

Individual upstream imports also work, for example:

```lean
import DifferentialGeometry.Geometry.MinimalSurface.Plateau.Existence
import DifferentialGeometry.Geometry.MinimalSurface.Plateau.Embeddedness.RegularDisk
```

On Della, compilation must run in a Slurm CPU allocation, with one CPU and
`LEAN_NUM_THREADS=1`, following the owner's cluster policy. The commands above are the portable
build interface; the build configuration uses no hard-coded Della paths or cache symlinks.

## Verification

```sh
python3 scripts/verify_extraction.py
```

This requires Python 3.9 or newer. It checks the upstream file hashes, exact source inventory,
complete and acyclic project imports, reachability from the entry point, dependency pins, and
source admission markers. It does not compile Lean or prove semantic correctness.

After a successful Lean build, run:

```sh
python3 scripts/check_axioms.py
```

This prints the exact types and transitive axioms of eight representative declarations. It
rejects axioms other than `propext`, `Classical.choice`, and `Quot.sound`. The temporary Lean
driver is created outside the repository and removed afterward. An acceptable axiom list does
not discharge a theorem's explicit hypotheses.

At extraction time, the source-packaging checks passed. **A fresh full Lean build and the
compiler-based axiom check have not been performed for this standalone repository.** Existing
upstream claims or artifacts are not presented as fresh standalone build evidence.

## Provenance and license

[provenance/extraction.json](provenance/extraction.json) records every copied file's hash,
its upstream Git blob, the target list, the full import graph, and the external imports.
[provenance/target-modules.txt](provenance/target-modules.txt) is the selected target list.
The original package configuration and dependency lock are retained in `provenance/`.

All 3,609 copied Lean modules are byte-for-byte identical to the pinned upstream source.
Only the standalone package configuration, the two aggregate entry points, documentation,
and verification scripts were created or adapted for this extraction.

The upstream [Apache-2.0 license](LICENSE), [NOTICE](NOTICE), and
[citation metadata](provenance/upstream-CITATION.cff) are retained. Third-party licenses,
attributions, and modification records remain under their original `DifferentialGeometry/External/`
directories. Authorship and provenance of the formal mathematics remain with those sources.
