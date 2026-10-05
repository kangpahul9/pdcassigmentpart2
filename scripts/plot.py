#!/usr/bin/env python3
"""Part 2B: runtime table + speedup/efficiency graphs from results/raw_times.csv.
Speedup S(p) = T_impl(1) / T_impl(p)   (each implementation vs its own 1-thread run)
Efficiency  E(p) = S(p) / p
Outputs: results/summary.csv, results/runtime_table.md,
         results/speedup.png, results/efficiency.png
"""
import csv, statistics
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ORDER = ["basic", "red_default", "red_forces_cyclic", "red_all_cyclic"]
LABEL = {"basic": "Basic", "red_default": "Reduced Default",
         "red_forces_cyclic": "Reduced Forces Cyclic",
         "red_all_cyclic": "Reduced All Cyclic"}
MARK = {"basic": "o-", "red_default": "s--",
        "red_forces_cyclic": "^-.", "red_all_cyclic": "D:"}

times = defaultdict(list)
for row in csv.DictReader(open("results/raw_times.csv")):
    times[(row["impl"], int(row["threads"]))].append(float(row["seconds"]))

threads = sorted({p for _, p in times})
mean = {k: statistics.mean(v) for k, v in times.items()}
std = {k: statistics.stdev(v) if len(v) > 1 else 0.0 for k, v in times.items()}

with open("results/summary.csv", "w") as f:
    f.write("impl,threads,runs,mean_s,std_s,speedup,efficiency\n")
    for i in ORDER:
        for p in threads:
            s = mean[(i, 1)] / mean[(i, p)]
            f.write(f"{i},{p},{len(times[(i,p)])},{mean[(i,p)]:.4f},"
                    f"{std[(i,p)]:.4f},{s:.3f},{s/p:.3f}\n")

with open("results/runtime_table.md", "w") as f:
    f.write("| Number of Threads | " + " | ".join(LABEL[i] for i in ORDER) + " |\n")
    f.write("|---|" + "---|" * len(ORDER) + "\n")
    for p in threads:
        f.write(f"| {p} | " + " | ".join(f"{mean[(i,p)]:.3f}" for i in ORDER) + " |\n")

def graph(fn, ylabel, title, fname, ideal):
    fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=200)
    ax.plot(threads, [ideal(p) for p in threads], color="grey", lw=1, label="Ideal")
    for i in ORDER:
        ax.plot(threads, [fn(i, p) for p in threads], MARK[i], label=LABEL[i])
    ax.set_xscale("log", base=2)
    ax.set_xticks(threads); ax.set_xticklabels([str(p) for p in threads])
    ax.set_xlabel("Number of OpenMP threads"); ax.set_ylabel(ylabel)
    ax.set_title(title); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(f"results/{fname}"); plt.close(fig)

graph(lambda i, p: mean[(i,1)] / mean[(i,p)], "Speedup  T(1)/T(p)",
      "Speedup vs. Number of Threads", "speedup.png", lambda p: p)
graph(lambda i, p: mean[(i,1)] / mean[(i,p)] / p, "Efficiency  S(p)/p",
      "Efficiency vs. Number of Threads", "efficiency.png", lambda p: 1.0)

print(open("results/runtime_table.md").read())