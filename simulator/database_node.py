import psycopg2
import time


class DatabaseNode:

    LOCK_TIMEOUT_SECONDS = 5

    def __init__(
        self,
        name,
        host,
        port,
        database="profile_service",
        user="quorum",
        password="quorum123"
    ):

        self.name = name

        self.host = host
        self.port = port

        self.database = database
        self.user = user
        self.password = password

        self.is_down = False
        self.slow_mode = False

        self.conflict_count = 0

    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):

        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            connect_timeout=2
        )

    # =====================================================
    # SLOW NODE SIMULATION
    # =====================================================

    def apply_delay(self):

        if self.slow_mode:

            time.sleep(0.5)

    # =====================================================
    # CLEANUP EXPIRED LOCKS
    # =====================================================

    def cleanup_expired_locks(self):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(
            f"""
            DELETE
            FROM distributed_locks
            WHERE locked_at <
                  NOW() - INTERVAL
                  '{self.LOCK_TIMEOUT_SECONDS} seconds'
            """
        )

        conn.commit()

        cur.close()
        conn.close()

    # =====================================================
    # ACQUIRE LOCK
    # =====================================================

    def acquire_lock(
        self,
        user_id,
        tx_id
    ):

        if self.is_down:

            raise Exception(
                f"{self.name} is DOWN"
            )

        self.apply_delay()

        self.cleanup_expired_locks()

        conn = self.connect()

        cur = conn.cursor()

        try:

            cur.execute(
                """
                INSERT INTO distributed_locks(
                    user_id,
                    tx_id,
                    locked_at
                )
                VALUES(
                    %s,
                    %s,
                    NOW()
                )
                """,
                (
                    user_id,
                    tx_id
                )
            )

            conn.commit()

            return True

        except psycopg2.Error:

            conn.rollback()

            self.conflict_count += 1

            return False

        finally:

            cur.close()
            conn.close()

    # =====================================================
    # RELEASE LOCK
    # =====================================================

    def release_lock(
        self,
        user_id,
        tx_id
    ):

        if self.is_down:

            return

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(
            """
            DELETE
            FROM distributed_locks
            WHERE user_id=%s
            AND tx_id=%s
            """,
            (
                user_id,
                tx_id
            )
        )

        conn.commit()

        cur.close()
        conn.close()

    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    def update_department(
        self,
        user_id,
        new_department
    ):

        if self.is_down:

            raise Exception(
                f"{self.name} is DOWN"
            )

        self.apply_delay()

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(
            """
            UPDATE user_profiles
            SET department=%s
            WHERE user_id=%s
            """,
            (
                new_department,
                user_id
            )
        )

        conn.commit()

        cur.close()
        conn.close()

    # =====================================================
    # READ PROFILE
    # =====================================================

    def read_profile(
        self,
        user_id
    ):

        if self.is_down:

            raise Exception(
                f"{self.name} is DOWN"
            )

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                user_id,
                department,
                job_role
            FROM user_profiles
            WHERE user_id=%s
            """,
            (user_id,)
        )

        row = cur.fetchone()

        cur.close()
        conn.close()

        return row