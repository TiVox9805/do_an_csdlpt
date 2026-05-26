import tkinter as tk
from tkinter import ttk, messagebox

import subprocess
import os

from PIL import Image, ImageTk


class QuorumDashboard:

    def __init__(self, root):

        self.root = root

        root.title(
            "Hệ Thống Khóa Phân Tán Dựa Trên Quorum"
        )

        root.geometry(
            "1500x950"
        )

        root.configure(bg="white")

        # =====================================================
        # TITLE
        # =====================================================

        title = tk.Label(
            root,
            text="HỆ THỐNG KHÓA PHÂN TÁN DỰA TRÊN QUORUM",
            font=("Arial", 24, "bold"),
            bg="white"
        )

        title.pack(
            pady=10
        )

        subtitle = tk.Label(
            root,
            text="Global Profile Service - Majority Quorum (2/3)",
            font=("Arial", 12),
            bg="white"
        )

        subtitle.pack()

        # =====================================================
        # CLUSTER STATUS
        # =====================================================

        self.status_frame = tk.Frame(
            root,
            bg="#e9f5ff",
            bd=2,
            relief="ridge"
        )

        self.status_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.cluster_status = tk.Label(
            self.status_frame,
            text="Trạng Thái Cluster: HEALTHY",
            font=("Arial", 12, "bold"),
            bg="#e9f5ff"
        )

        self.cluster_status.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.quorum_status = tk.Label(
            self.status_frame,
            text="Quorum Required: 2/3",
            font=("Arial", 11),
            bg="#e9f5ff"
        )

        self.quorum_status.pack(
            anchor="w",
            padx=10
        )

        self.node_status = tk.Label(
            self.status_frame,
            text="Node Hoạt Động: 3/3",
            font=("Arial", 11),
            bg="#e9f5ff"
        )

        self.node_status.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.quorum_available = tk.Label(
            self.status_frame,
            text="Quorum Available: YES",
            font=("Arial", 11, "bold"),
            bg="#e9f5ff"
        )

        self.quorum_available.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        # =====================================================
        # KPI CARDS
        # =====================================================

        self.create_kpi_cards()

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = tk.Frame(
            root,
            bg="white"
        )

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="Healthy Test",
            command=self.run_healthy,
            bg="#28a745",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Slow Node Test",
            command=self.run_slow,
            bg="#ffc107",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Node Failure Test",
            command=self.run_down,
            bg="#dc3545",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Full Benchmark",
            command=self.run_full,
            bg="#007bff",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=10)

        # =====================================================
        # TABLE
        # =====================================================

        self.create_table()

        # =====================================================
        # CHARTS
        # =====================================================

        self.create_charts()

        # =====================================================
        # CONCLUSION
        # =====================================================

        self.conclusion = tk.Label(
            root,
            text="",
            justify="left",
            font=("Arial", 11),
            bg="white"
        )

        self.conclusion.pack(
            anchor="w",
            padx=20,
            pady=10
        )

    # =====================================================
    # KPI CARDS
    # =====================================================

    def create_kpi_cards(self):

        frame = tk.Frame(
            self.root,
            bg="white"
        )

        frame.pack(
            pady=10
        )

        self.healthy_label = self.create_card(
            frame,
            "Healthy",
            "-",
            "#d4edda"
        )

        self.slow_label = self.create_card(
            frame,
            "Site3 Slow",
            "-",
            "#fff3cd"
        )

        self.down_label = self.create_card(
            frame,
            "Site3 Down",
            "-",
            "#f8d7da"
        )

    def create_card(
        self,
        parent,
        title,
        value,
        color
    ):

        card = tk.Frame(
            parent,
            bg=color,
            relief="ridge",
            bd=2
        )

        card.pack(
            side="left",
            padx=15
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 14, "bold"),
            bg=color
        ).pack(
            padx=40,
            pady=5
        )

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 20),
            bg=color
        )

        label.pack(
            pady=10
        )

        return label

    # =====================================================
    # TABLE
    # =====================================================

    def create_table(self):

        frame = tk.Frame(
            self.root
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree = ttk.Treeview(
            frame
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # CHARTS
    # =====================================================

    def create_charts(self):

        self.chart_frame = tk.Frame(
            self.root,
            bg="white"
        )

        self.chart_frame.pack(
            pady=10
        )

        self.latency_panel = tk.Label(
            self.chart_frame,
            bg="white"
        )

        self.latency_panel.pack(
            side="left",
            padx=10
        )

        self.throughput_panel = tk.Label(
            self.chart_frame,
            bg="white"
        )

        self.throughput_panel.pack(
            side="left",
            padx=10
        )

        self.success_panel = tk.Label(
            self.chart_frame,
            bg="white"
        )

        self.success_panel.pack(
            side="left",
            padx=10
        )

    # =====================================================
    # RUN SCRIPT
    # =====================================================

    def run_script(
        self,
        scenario
    ):

        try:

            self.load_results(
                scenario
            )

        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    # =====================================================
    # SCENARIOS
    # =====================================================

    def run_healthy(self):

        self.cluster_status.config(
            text="Trạng Thái Cluster: HEALTHY"
        )

        self.node_status.config(
            text="Node Hoạt Động: 3/3"
        )

        self.quorum_available.config(
            text="Quorum Available: YES"
        )

        self.run_script(
            "healthy"
        )

    def run_slow(self):

        self.cluster_status.config(
            text="Trạng Thái Cluster: SLOW NODE"
        )

        self.node_status.config(
            text="Node Hoạt Động: 3/3"
        )

        self.quorum_available.config(
            text="Quorum Available: YES"
        )

        self.run_script(
            "slow"
        )

    def run_down(self):

        self.cluster_status.config(
            text="Trạng Thái Cluster: DEGRADED"
        )

        self.node_status.config(
            text="Node Hoạt Động: 2/3"
        )

        self.quorum_available.config(
            text="Quorum Available: YES (2/3)"
        )

        self.run_script(
            "down"
        )

    def run_full(self):

        self.cluster_status.config(
            text="Trạng Thái Cluster: FULL BENCHMARK"
        )

        self.node_status.config(
            text="Node Hoạt Động: 3/3"
        )

        self.quorum_available.config(
            text="Quorum Available: YES"
        )

        self.run_script(
            "full"
        )

    # =====================================================
    # LOAD RESULTS
    # =====================================================

    def load_results(
        self,
        scenario
    ):

        # RESET KPI

        self.healthy_label.config(text="-")
        self.slow_label.config(text="-")
        self.down_label.config(text="-")

        # CLEAR TABLE

        self.tree.delete(
            *self.tree.get_children()
        )

        columns = (
            "Scenario",
            "Avg Latency",
            "Min Latency",
            "Max Latency",
            "P95 Latency",
            "Success Rate",
            "Throughput"
        )

        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=160
            )

        # =================================================
        # RUN BENCHMARK
        # =================================================

        result = subprocess.check_output(
            [
                "python",
                "benchmark.py",
                scenario
            ],
            text=True,
            encoding="utf-8"
        )

        lines = result.splitlines()

        # =================================================
        # FULL BENCHMARK
        # =================================================

        if scenario == "full":

            benchmark_data = []

            current_scenario = None

            avg_latency = "-"
            min_latency = "-"
            max_latency = "-"
            p95_latency = "-"
            success_rate = "-"
            throughput = "-"

            for line in lines:

                if "HEALTHY CLUSTER" in line:

                    if current_scenario is not None:

                        benchmark_data.append(
                            (
                                current_scenario,
                                avg_latency,
                                min_latency,
                                max_latency,
                                p95_latency,
                                success_rate,
                                throughput
                            )
                        )

                    current_scenario = "Healthy"

                    avg_latency = "-"
                    min_latency = "-"
                    max_latency = "-"
                    p95_latency = "-"
                    success_rate = "-"
                    throughput = "-"

                elif "SITE3 SLOW" in line:

                    if current_scenario is not None:

                        benchmark_data.append(
                            (
                                current_scenario,
                                avg_latency,
                                min_latency,
                                max_latency,
                                p95_latency,
                                success_rate,
                                throughput
                            )
                        )

                    current_scenario = "Site3 Slow"

                    avg_latency = "-"
                    min_latency = "-"
                    max_latency = "-"
                    p95_latency = "-"
                    success_rate = "-"
                    throughput = "-"

                elif "SITE3 DOWN" in line:

                    if current_scenario is not None:

                        benchmark_data.append(
                            (
                                current_scenario,
                                avg_latency,
                                min_latency,
                                max_latency,
                                p95_latency,
                                success_rate,
                                throughput
                            )
                        )

                    current_scenario = "Site3 Down"

                    avg_latency = "-"
                    min_latency = "-"
                    max_latency = "-"
                    p95_latency = "-"
                    success_rate = "-"
                    throughput = "-"

                elif "Độ trễ trung bình" in line:

                    avg_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Độ trễ nhỏ nhất" in line:

                    min_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Độ trễ lớn nhất" in line:

                    max_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "P95 Latency" in line:

                    p95_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Tỷ lệ thành công" in line:

                    success_rate = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Thông lượng" in line:

                    throughput = (
                        line.split(":")[1]
                        .strip()
                    )

            if current_scenario is not None:

                benchmark_data.append(
                    (
                        current_scenario,
                        avg_latency,
                        min_latency,
                        max_latency,
                        p95_latency,
                        success_rate,
                        throughput
                    )
                )

            for row in benchmark_data:

                self.tree.insert(
                    "",
                    "end",
                    values=row
                )

                scenario_name = row[0]
                latency = row[1]

                if scenario_name == "Healthy":

                    self.healthy_label.config(
                        text=latency
                    )

                elif scenario_name == "Site3 Slow":

                    self.slow_label.config(
                        text=latency
                    )

                elif scenario_name == "Site3 Down":

                    self.down_label.config(
                        text=latency
                    )

            self.load_image(
                "latency_comparison.png",
                self.latency_panel
            )

            self.load_image(
                "throughput_comparison.png",
                self.throughput_panel
            )

            self.load_image(
                "success_rate_comparison.png",
                self.success_panel
            )

        # =================================================
        # SINGLE SCENARIO
        # =================================================

        else:

            avg_latency = "-"
            min_latency = "-"
            max_latency = "-"
            p95_latency = "-"
            success_rate = "-"
            throughput = "-"

            for line in lines:

                if "Độ trễ trung bình" in line:

                    avg_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Độ trễ nhỏ nhất" in line:

                    min_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Độ trễ lớn nhất" in line:

                    max_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "P95 Latency" in line:

                    p95_latency = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Tỷ lệ thành công" in line:

                    success_rate = (
                        line.split(":")[1]
                        .strip()
                    )

                elif "Thông lượng" in line:

                    throughput = (
                        line.split(":")[1]
                        .strip()
                    )

            if scenario == "healthy":

                scenario_name = "Healthy"

                self.healthy_label.config(
                    text=avg_latency
                )

            elif scenario == "slow":

                scenario_name = "Site3 Slow"

                self.slow_label.config(
                    text=avg_latency
                )

            else:

                scenario_name = "Site3 Down"

                self.down_label.config(
                    text=avg_latency
                )

            self.tree.insert(
                "",
                "end",
                values=(
                    scenario_name,
                    avg_latency,
                    min_latency,
                    max_latency,
                    p95_latency,
                    success_rate,
                    throughput
                )
            )

            self.latency_panel.config(
                image=""
            )

            self.throughput_panel.config(
                image=""
            )

            self.success_panel.config(
                image=""
            )

        # =================================================
        # CONCLUSION
        # =================================================

        self.conclusion.config(
            text=
            "KẾT LUẬN THỰC NGHIỆM\n\n"
            "• Majority Quorum (2/3) giúp hệ thống duy trì hoạt động.\n"
            "• Slow Node làm tăng latency nhưng không ảnh hưởng nhiều.\n"
            "• Khi 1 node bị lỗi, hệ thống vẫn đạt quorum.\n"
            "• Quorum đảm bảo consistency và availability."
        )

    # =====================================================
    # LOAD IMAGE
    # =====================================================

    def load_image(
        self,
        path,
        panel
    ):

        if os.path.exists(path):

            img = Image.open(path)

            img = img.resize(
                (420, 300)
            )

            photo = ImageTk.PhotoImage(img)

            panel.config(
                image=photo
            )

            panel.image = photo


# =====================================================
# MAIN
# =====================================================

root = tk.Tk()

app = QuorumDashboard(root)

root.mainloop()