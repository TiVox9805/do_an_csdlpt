import uuid
from concurrent.futures import (
    ThreadPoolExecutor,
    wait,
    FIRST_COMPLETED
)


class QuorumCoordinator:

    def __init__(self, nodes):

        self.nodes = nodes

        # Majority quorum
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

            # ============================================
            # GỬI LOCK SONG SONG
            # ============================================

            future_map = {}

            for node in self.nodes:

                future = executor.submit(
                    node.acquire_lock,
                    user_id,
                    tx_id
                )

                future_map[future] = node

            completed = set()

            # ============================================
            # CHỜ TỪNG NODE
            # ============================================

            while len(acquired_nodes) < self.quorum_size:

                done, not_done = wait(
                    future_map.keys() - completed,
                    return_when=FIRST_COMPLETED
                )

                completed.update(done)

                for future in done:

                    node = future_map[future]

                    try:

                        result = future.result()

                        if result:

                            acquired_nodes.append(node)

                    except:
                        pass

                # Không đủ node
                if len(completed) == len(future_map):

                    break

            # ============================================
            # KHÔNG ĐẠT QUORUM
            # ============================================

            if len(acquired_nodes) < self.quorum_size:

                for node in acquired_nodes:

                    try:

                        node.release_lock(
                            user_id,
                            tx_id
                        )

                    except:
                        pass

                return False

            # ============================================
            # COMMIT NGAY TRÊN 2 NODE NHANH
            # ============================================

            for node in acquired_nodes:

                node.update_department(
                    user_id,
                    new_department
                )

            return True

        finally:

            # release locks
            for node in acquired_nodes:

                try:

                    node.release_lock(
                        user_id,
                        tx_id
                    )

                except:
                    pass

            # QUAN TRỌNG:
            # không chờ Site3 slow
            executor.shutdown(
                wait=False
            )