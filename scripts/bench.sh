#!/usr/bin/env bash
# Part 2B timing experiment: 4 implementations x thread counts x RUNS.
# Builds with -DNO_OUTPUT so only the elapsed time is printed.
# Output: results/raw_times.csv (impl,threads,run,seconds)
#         results/environment.txt
# Usage:  ./scripts/bench.sh
#         N=4000 STEPS=100 RUNS=5 THREADS="1 4 8 16 32" ./scripts/bench.sh
set -eu
cd "$(dirname "$0")/.."

N=${N:-4000}
STEPS=${STEPS:-100}
DT=0.01
RUNS=${RUNS:-5}
THREADS=${THREADS:-"1 4 8 16 32"}

mkdir -p bin results
for p in omp_nbody_basic omp_nbody_red_default omp_nbody_red omp_nbody_red_all_cyclic; do
  gcc -O2 -Wall -fopenmp -DNO_OUTPUT -o bin/$p src/$p.c -lm 2>/dev/null
done

{
  echo "date:     $(date)"
  echo "host:     $(hostname)"
  echo "cores:    $(nproc)"
  lscpu | grep -E "Model name|^CPU\(s\)|Thread\(s\) per core|Core\(s\) per socket|Socket\(s\)" || true
  echo "compiler: $(gcc --version | head -1)"
  echo "flags:    -O2 -fopenmp -DNO_OUTPUT"
  echo "params:   n=$N steps=$STEPS dt=$DT, output disabled"
  echo "runs:     $RUNS per config (+1 warm-up discarded)"
} > results/environment.txt
cat results/environment.txt

echo "impl,threads,run,seconds" > results/raw_times.csv
for pair in basic:omp_nbody_basic red_default:omp_nbody_red_default \
            red_forces_cyclic:omp_nbody_red red_all_cyclic:omp_nbody_red_all_cyclic; do
  impl=${pair%%:*}; exe=bin/${pair##*:}
  for t in $THREADS; do
    $exe $t $N $STEPS $DT 1 g > /dev/null          # warm-up
    for r in $(seq 1 $RUNS); do
      s=$($exe $t $N $STEPS $DT 1 g | awk '/Elapsed/ {print $4}')
      echo "$impl,$t,$r,$s" >> results/raw_times.csv
      echo "$impl t=$t run=$r $s s"
    done
  done
done
echo "Done -> results/raw_times.csv"