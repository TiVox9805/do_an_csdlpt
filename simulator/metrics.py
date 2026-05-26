class Metrics:
  
    def __init__(self):

        self.total_transactions = 0

        self.successful_transactions = 0
        self.failed_transactions = 0

        self.total_latency = 0.0

        self.latencies = []

    # =====================================================
    # SUCCESS
    # =====================================================

    def record_success(
        self,
        latency
    ):

        self.total_transactions += 1

        self.successful_transactions += 1

        self.total_latency += latency

        self.latencies.append(
            latency
        )

    # =====================================================
    # FAILURE
    # =====================================================

    def record_failure(
        self,
        latency
    ):

        self.total_transactions += 1

        self.failed_transactions += 1

        self.total_latency += latency

        self.latencies.append(
            latency
        )

    # =====================================================
    # REPORT
    # =====================================================

    def report(self):

        avg_latency = (
            self.total_latency /
            self.total_transactions
            if self.total_transactions > 0
            else 0
        )

        success_rate = (
            self.successful_transactions /
            self.total_transactions * 100
            if self.total_transactions > 0
            else 0
        )

        throughput = (
            self.total_transactions /
            self.total_latency
            if self.total_latency > 0
            else 0
        )

        min_latency = (
            min(self.latencies)
            if self.latencies
            else 0
        )

        max_latency = (
            max(self.latencies)
            if self.latencies
            else 0
        )

        # P95 LATENCY

        sorted_latencies = sorted(
            self.latencies
        )

        p95_index = int(
            len(sorted_latencies) * 0.95
        ) - 1

        p95_latency = (
            sorted_latencies[p95_index]
            if sorted_latencies
            else 0
        )

        return {

            "transactions":
                self.total_transactions,

            "avg_latency_ms":
                round(avg_latency * 1000, 2),

            "min_latency_ms":
                round(min_latency * 1000, 2),

            "max_latency_ms":
                round(max_latency * 1000, 2),

            "p95_latency_ms":
                round(p95_latency * 1000, 2),

            "success_rate":
                round(success_rate, 2),

            "throughput":
                round(throughput, 2)
        }