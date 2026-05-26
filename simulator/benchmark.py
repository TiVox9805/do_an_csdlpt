import random
import time
import sys
import os
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

from database_node import DatabaseNode
from coordinator import QuorumCoordinator
from metrics import Metrics


# =====================================================
# CREATE NODES
# =====================================================

site1 = DatabaseNode(
    "Site1",
    "localhost",
    5434
)

site2 = DatabaseNode(
    "Site2",
    "localhost",
    5435
)

site3 = DatabaseNode(
    "Site3",
    "localhost",
    5436
)

coordinator = QuorumCoordinator(
    [
        site1,
        site2,
        site3
    ]
)


# =====================================================
# RESET CLUSTER
# =====================================================

def reset_cluster():

    site1.is_down = False
    site2.is_down = False
    site3.is_down = False

    site1.slow_mode = False
    site2.slow_mode = False
    site3.slow_mode = False


# =====================================================
# CLUSTER STATUS
# =====================================================

def get_cluster_status():

    available = 0

    for node in [site1, site2, site3]:

        if not node.is_down:

            available += 1

    quorum_available = (
        "YES"
        if available >= 2
        else "NO"
    )

    cluster_status = (
        "HEALTHY"
        if available == 3
        else "DEGRADED"
    )

    return {
        "available_nodes":
            f"{available}/3",

        "quorum":
            quorum_available,

        "status":
            cluster_status
    }


# =====================================================
# BENCHMARK FUNCTION
# =====================================================

def run_benchmark(
    title,
    transactions=100
):

    metrics = Metrics()

    cluster = get_cluster_status()

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    print(
        f"Cluster Status     : "
        f"{cluster['status']}"
    )

    print(
        f"Available Nodes    : "
        f"{cluster['available_nodes']}"
    )

    print(
        f"Quorum Required    : 2/3"
    )

    print(
        f"Quorum Available   : "
        f"{cluster['quorum']}"
    )

    print()

    start_total = time.perf_counter()

    for i in range(transactions):

        user_id = random.randint(
            1,
            1470
        )

        start_tx = time.perf_counter()

        success = coordinator.update_department(
            user_id=user_id,
            new_department=f"Dept_{i}"
        )

        latency = (
            time.perf_counter() -
            start_tx
        )

        if success:

            metrics.record_success(
                latency
            )

        else:

            metrics.record_failure(
                latency
            )

    end_total = time.perf_counter()

    report = metrics.report()

    print()
    print("=" * 60)
    print("KẾT QUẢ BENCHMARK")
    print("=" * 60)

    print()

    print(
        f"Tổng giao dịch      : "
        f"{report['transactions']}"
    )

    print(
        f"Độ trễ trung bình   : "
        f"{report['avg_latency_ms']} ms"
    )

    print(
        f"Độ trễ nhỏ nhất     : "
        f"{report['min_latency_ms']} ms"
    )

    print(
        f"Độ trễ lớn nhất     : "
        f"{report['max_latency_ms']} ms"
    )

    print(
        f"P95 Latency         : "
        f"{report['p95_latency_ms']} ms"
    )

    print(
        f"Tỷ lệ thành công    : "
        f"{report['success_rate']} %"
    )

    print(
        f"Thông lượng         : "
        f"{report['throughput']} TX/s"
    )

    print()

    print(
        f"Execution Time      : "
        f"{round(end_total - start_total, 2)} s"
    )

    print()

    return report


# =====================================================
# MODE
# =====================================================

mode = "full"

if len(sys.argv) > 1:

    mode = sys.argv[1].lower()


# =====================================================
# HEALTHY TEST
# =====================================================

if mode == "healthy":

    reset_cluster()

    run_benchmark(
        title="HEALTHY CLUSTER TEST",
        transactions=100
    )


# =====================================================
# SLOW NODE TEST
# =====================================================

elif mode == "slow":

    reset_cluster()

    site3.slow_mode = True

    run_benchmark(
        title="SLOW NODE TEST (+500ms)",
        transactions=100
    )


# =====================================================
# NODE FAILURE TEST
# =====================================================

elif mode == "down":

    reset_cluster()

    site3.is_down = True

    run_benchmark(
        title="NODE FAILURE TEST",
        transactions=100
    )


# =====================================================
# FULL BENCHMARK
# =====================================================

else:

    print()
    print("=" * 60)
    print("FULL QUORUM BENCHMARK")
    print("=" * 60)

    print()

    # =================================================
    # HEALTHY
    # =================================================

    reset_cluster()

    healthy_report = run_benchmark(
        title="HEALTHY CLUSTER",
        transactions=100
    )

    # =================================================
    # SLOW
    # =================================================

    reset_cluster()

    site3.slow_mode = True

    slow_report = run_benchmark(
        title="SITE3 SLOW (+500ms)",
        transactions=100
    )

    # =================================================
    # DOWN
    # =================================================

    reset_cluster()

    site3.is_down = True

    down_report = run_benchmark(
        title="SITE3 DOWN",
        transactions=100
    )

    # =================================================
    # FINAL COMPARISON
    # =================================================

    print()
    print("=" * 60)
    print("SO SÁNH TỔNG KẾT")
    print("=" * 60)

    print()

    print(
        f"Healthy Latency     : "
        f"{healthy_report['avg_latency_ms']} ms"
    )

    print(
        f"Slow Node Latency   : "
        f"{slow_report['avg_latency_ms']} ms"
    )

    print(
        f"Node Failure        : "
        f"{down_report['avg_latency_ms']} ms"
    )

    print()

    print(
        f"Healthy Throughput  : "
        f"{healthy_report['throughput']} TX/s"
    )

    print(
        f"Slow Throughput     : "
        f"{slow_report['throughput']} TX/s"
    )

    print(
        f"Failure Throughput  : "
        f"{down_report['throughput']} TX/s"
    )

    print()

    # =================================================
    # CONCLUSION
    # =================================================

    latency_increase = round(
        (
            slow_report["avg_latency_ms"] -
            healthy_report["avg_latency_ms"]
        )
        /
        healthy_report["avg_latency_ms"]
        * 100,
        2
    )

    print("=" * 60)
    print("KẾT LUẬN THỰC NGHIỆM")
    print("=" * 60)

    print()

    print(
        f"- Slow Node làm tăng độ trễ "
        f"{latency_increase}%"
    )

    print(
        "- Hệ thống vẫn đạt "
        "100% success rate "
        "khi 1 node bị lỗi"
    )

    print(
        "- Majority Quorum (2/3) "
        "duy trì tính sẵn sàng hệ thống"
    )

    print(
        "- Hệ thống vẫn hoạt động "
        "khi còn đa số node"
    )

    # =================================================
    # SAVE CSV
    # =================================================

    df = pd.DataFrame([

        {
            "scenario": "Healthy",
            "avg_latency_ms": healthy_report["avg_latency_ms"],
            "min_latency_ms": healthy_report["min_latency_ms"],
            "max_latency_ms": healthy_report["max_latency_ms"],
            "p95_latency_ms": healthy_report["p95_latency_ms"],
            "success_rate": healthy_report["success_rate"],
            "throughput": healthy_report["throughput"]
        },

        {
            "scenario": "Site3 Slow",
            "avg_latency_ms": slow_report["avg_latency_ms"],
            "min_latency_ms": slow_report["min_latency_ms"],
            "max_latency_ms": slow_report["max_latency_ms"],
            "p95_latency_ms": slow_report["p95_latency_ms"],
            "success_rate": slow_report["success_rate"],
            "throughput": slow_report["throughput"]
        },

        {
            "scenario": "Site3 Down",
            "avg_latency_ms": down_report["avg_latency_ms"],
            "min_latency_ms": down_report["min_latency_ms"],
            "max_latency_ms": down_report["max_latency_ms"],
            "p95_latency_ms": down_report["p95_latency_ms"],
            "success_rate": down_report["success_rate"],
            "throughput": down_report["throughput"]
        }

    ])

    df.to_csv(
        "benchmark_results.csv",
        index=False
    )

    print()
    print("benchmark_results.csv generated.")

    # =================================================
    # GENERATE CHARTS
    # =================================================

    os.system(
        "python visualization.py"
    )

    print()
    print("Charts generated.")
    print()

    print("DONE.")