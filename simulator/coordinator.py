import uuid
from concurrent.futures import (
    ThreadPoolExecutor,
    wait,
    FIRST_COMPLETED
)


class QuorumCoordinator:

    def __init__(self, nodes):

        self.nodes = nodes
        self.quorum_size = 2

    def update_department(
        self,
        user_id,
        new_department
    ):

        tx_id = str(uuid.uuid4())

        acquired_nodes = []

        executor = ThreadPoolExecutor(
            max_workers=len(self.nodes)
        )

        try:

            futures = []

            for node in self.nodes:

                future = executor.submit(
                    node.acquire_lock,
                    user_id,
                    tx_id
                )

                futures.append(
                    (future, node)
                )

            # ==========================================
            # CHỈ LẤY 2 NODE NHANH NHẤT
            # ==========================================

            while len(acquired_nodes) < self.quorum_size:

                done, _ = wait(
                    [f for f, _ in futures],
                    return_when=FIRST_COMPLETED
                )

                for future in done:

                    for f, node in futures:

                        if f == future:

                            try:

                                result = future.result(
                                    timeout=0
                                )

                                if result:

                                    acquired_nodes.append(
                                        node
                                    )

                            except:
                                pass

                            futures.remove(
                                (f, node)
                            )

                            break

                # Không đủ quorum
                if len(done) == 0:
                    break

            # ==========================================
            # KHÔNG ĐỦ QUORUM
            # ==========================================

            if len(acquired_nodes) < self.quorum_size:

                for node in acquired_nodes:

                    node.release_lock(
                        user_id,
                        tx_id
                    )

                return False

            # ==========================================
            # UPDATE CHỈ 2 NODE NHANH
            # ==========================================

            for node in acquired_nodes:

                node.update_department(
                    user_id,
                    new_department
                )

            return True

        finally:

            for node in acquired_nodes:

                try:

                    node.release_lock(
                        user_id,
                        tx_id
                    )

                except:
                    pass

            executor.shutdown(
                wait=False
            )