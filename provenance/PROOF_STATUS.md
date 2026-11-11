# Scope and proof status

This document describes the exact upstream snapshot copied into this repository. It does not
make a claim about subsequent or unpublished branches of DifferentialGeometry.

## Entry points

Names in the first six rows below are in `DifferentialGeometry.Geometry`; names in the last two
are in `DifferentialGeometry.Geometry.MinimalSurface`.

| Declaration | Source module beneath `Geometry/MinimalSurface/` | Scope |
|---|---|---|
| `exists_morrey_disk` | `Plateau/Existence.lean` | Existence from a complete, homogeneously regular target metric, a smooth embedded boundary loop, and a nonempty competitor class. |
| `exists_morrey_disk_of_compact` | `Plateau/Existence/Compact.lean` | Compact-target version, with its stated weakly monotone competitor assumption. |
| `exists_confined_morrey_disk_R7E` | `Plateau/ConfinedMorreyR7E.lean` | A confined Morrey disk under the explicit compactness, collar-convexity, boundary, and spanning hypotheses. |
| `closed_disk_immersion_of_completed_profile` | `Plateau/Regularity/ProfileClosedRank.lean` | Closed-disk rank for the completed-profile setting, under the geometric hypotheses in its full statement. |
| `IsMorreyDisk.isEmbedding_of_no_transverse` | `Plateau/Embeddedness/RegularDisk.lean` | Embedding of the given Morrey disk, assuming full closed-disk rank, separation from the prescribed boundary, and exclusion of transverse collisions. |
| `prepared_least_area_embedded_R12` | `Plateau/TowerEngineR12.lean` | Conditional tower induction; the regular-neighborhood, cap, fold-shortening, covering-step, and descent suppliers remain explicit inputs. |
| `isExteriorSpanningDisk_of_morrey_AT` | `ExteriorDiskAttainAT.lean` | Exact-trace, area-preserving reparametrization of a Morrey disk whose embedding and closed-disk immersion are supplied. |
| `isExteriorSpanningDisk.attains_positive_leastExteriorDiskArea_of_morrey_open` | `ExteriorDiskAttainment.lean` | Positive least exterior area from a confined Morrey disk and an appropriate exact-trace replacement. |

The source statements, including their section variables and typeclass assumptions, are authoritative.
The table is a navigation aid, not a substitute for those statements.

## Why the conditional status matters

The source of `IsMorreyDisk.isEmbedding_of_no_transverse` explicitly takes
`hNoTransverse` as an argument. Its proof combines rank, boundary separation, and local
collision information to establish an embedding. It does not construct that collision
exclusion from the classical Meeks–Yau hypotheses.

The source of `prepared_least_area_embedded_R12` performs the tower induction using supplied
regular-neighborhood, cap, fold-shortening, double-cover, and descent statements. A Lean proof
of that conditional theorem establishes the implication; it does not establish the supplier
statements merely by receiving them as arguments.

The upstream application
[`HMYOfHNT_MYN.lean`](https://github.com/qinz1yang/differential-geometry/blob/fd2f07fba4c6c102ba626c59153ad98da8f0d442/DifferentialGeometry/Geometry/Flow/RicciFlow/LongTime/CuspP1/HMYOfHNT_MYN.lean)
also retains the no-transverse premise in `hMY_concl_of_hNT_MYN`. Its cusp/Ricci-flow-specific
context is not part of this standalone extraction.

Accordingly, this repository should be shared as **Meeks–Yau formalization components with
their dependencies**. A claim of the full classical theorem would additionally require an
exact natural headline, all its suppliers, and a fresh compiler and axiom audit on that chain.
No additional theorem, axiom, admission, or replacement hypothesis was inserted during extraction.

## Evidence from this extraction

- All copied source files were checked against the pinned upstream Git objects.
- The retained project import graph has no missing modules or cycles; every source module is
  reachable from `MeeksYau.lean`.
- The external package versions are the upstream versions. External direct imports resolve
  in the existing matching package sources and the pinned Lean toolchain.
- A source scan, with comments removed, found no `sorry`, `admit`, explicit `axiom`, `unsafe`,
  or `native_decide` markers in the retained Lean code. This is not a transitive axiom audit.
- Fresh standalone Lean compilation and the compiler-based axiom audit are **not performed**.
  The checks and commands needed to obtain that evidence are included in the repository.
- `git diff --cached --check` on the initial extraction reported seven inherited whitespace
  findings: five lines in the vendored DeGiorgi README and a final blank line in each of
  `RegularCollisionContact.lean` and `RegularCollisionContactR3B.lean`. They were retained to
  preserve exact upstream bytes. The new package configuration, entry points, scripts, and
  documentation pass the whitespace check.

This was a source extraction and packaging task. Existing mathematical proofs were not changed,
and no complete independent mathematical review of the 3,609-module dependency closure is claimed.
