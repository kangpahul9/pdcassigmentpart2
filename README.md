# COMP 3030 Assignment Part 2 — OpenMP N-body

**Student:** Pahul Preet Singh — <student id>
**Repository:** https://github.com/kangpahul9/pdcassigmentpart2

## Files
| File | Purpose |
|---|---|
| `src/nbody_shared_forces.c` | Supplied sequential starter, used as the validation reference |
| `part2a_critical.c` | Part 2A.1: shared force updates protected by a named `omp critical` |
| `part2a_locks.c` | Part 2A.2: one `omp_lock_t` per particle + private sum for `forces[part]` |
| `src/omp_nbody_basic.c` | Part 2B Basic (supplied) |
| `src/omp_nbody_red_default.c` | Part 2B Reduced, default schedule on all loops |
| `src/omp_nbody_red.c` | Part 2B Reduced, Forces Cyclic (supplied) |
| `src/omp_nbody_red_all_cyclic.c` | Part 2B Reduced, `schedule(static,1)` on all loops |
| `scripts/bench.sh` | Part 2B timing experiment |
| `scripts/plot.py` | Runtime table, speedup and efficiency graphs |
| `evidence/` | Part 2A validation and race outputs |
| `results/` | Part 2B timings and graphs |

## Compile
    gcc -O2 -Wall -fopenmp -o part2a_critical part2a_critical.c -lm
    gcc -O2 -Wall -fopenmp -o part2a_locks    part2a_locks.c    -lm
Add `-DNO_OUTPUT` to print only the elapsed time.

## Run
    ./part2a_critical <threads> <particles> <timesteps> <dt> <output freq> g
    ./part2a_locks 8 100 100 0.01 10 g

## Validation
Each program's output was compared with the sequential reference at
1, 2, 4, 8 and 16 OpenMP threads (ignoring the elapsed-time line).
See `evidence/`.

## Part 2B experiment
    ./scripts/bench.sh            # n=4000, 100 steps, 5 runs, threads 1 4 8 16 32
    python3 scripts/plot.py       # needs matplotlib