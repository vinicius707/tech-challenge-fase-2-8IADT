#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_PATH = "experiments/batch_runs/aggregate_results.csv"
OUT_PATH = "docs/images/compare_results.png"

def main():
    if not os.path.exists(CSV_PATH):
        print("Aggregate CSV not found:", CSV_PATH)
        return
    df = pd.read_csv(CSV_PATH)
    plt.figure(figsize=(8,4))
    plt.bar(df['name'], df['best_fitness'], color='tab:blue')
    plt.ylabel('best_fitness (lower is better)')
    plt.title('Comparison of Best Fitness across experiments')
    plt.grid(axis='y', alpha=0.3)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=150)
    print("Saved plot to", OUT_PATH)

if __name__ == "__main__":
    main()

