import pandas as pd
import matplotlib.pyplot as plt


# =====================================================
# LOAD CSV
# =====================================================

df = pd.read_csv(
    "benchmark_results.csv"
)

print(df)


# =====================================================
# LATENCY CHART
# =====================================================

plt.figure(
    figsize=(8, 5)
)

bars = plt.bar(
    df["scenario"],
    df["avg_latency_ms"]
)

for bar in bars:

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.2f}",
        ha="center",
        va="bottom"
    )

plt.title(
    "Latency Comparison"
)

plt.ylabel(
    "Latency (ms)"
)

plt.tight_layout()

plt.savefig(
    "latency_comparison.png"
)

plt.close()


# =====================================================
# THROUGHPUT CHART
# =====================================================

plt.figure(
    figsize=(8, 5)
)

bars = plt.bar(
    df["scenario"],
    df["throughput"]
)

for bar in bars:

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.2f}",
        ha="center",
        va="bottom"
    )

plt.title(
    "Throughput Comparison"
)

plt.ylabel(
    "Transactions per Second"
)

plt.tight_layout()

plt.savefig(
    "throughput_comparison.png"
)

plt.close()


# =====================================================
# SUCCESS RATE CHART
# =====================================================

plt.figure(
    figsize=(8, 5)
)

bars = plt.bar(
    df["scenario"],
    df["success_rate"]
)

for bar in bars:

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.2f}%",
        ha="center",
        va="bottom"
    )

plt.title(
    "Success Rate Comparison"
)

plt.ylabel(
    "Success Rate (%)"
)

plt.ylim(
    0,
    110
)

plt.tight_layout()

plt.savefig(
    "success_rate_comparison.png"
)

plt.close()


print("\nCharts generated successfully.")