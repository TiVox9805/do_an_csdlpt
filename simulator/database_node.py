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

    # ============================================
    # CONNECT
    # ============================================

    def connect(self):

        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    # ============================================
    # DELAY
    # ============================================

    def apply_delay(self):

        if self.slow_mode:

            time.sleep(0.5)

    # ============================================
    # CLEANUP LOCKS
    # ============================================

    def cleanup_expired_locks(self):

        conn = self.connect()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE
            FROM distributed_locks
            WHERE locked_at <
                  NOW() - INTERVAL '5 seconds'
            """
        )

        conn.commit()

        cur.close()
        conn.close()

    # ============================================
    # ACQUIRE LOCK
    # ============================================

    def acquire_lock(
        self,
        user_id,
        tx_id
    ):

        if self.is_down:

            raise Exception(
                f"{self.name} is DOWN"
            )

        # Delay chỉ ở lock phase
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

            return False

        finally:

            cur.close()
            conn.close()

    # ============================================
    # RELEASE LOCK
    # ============================================

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

    # ============================================
    # UPDATE
    # ============================================

    def update_department(
        self,
        user_id,
        new_department
    ):

        if self.is_down:

            raise Exception(
                f"{self.name} is DOWN"
            )

        # KHÔNG DELAY Ở ĐÂY

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

    # ============================================
    # READ
    # ============================================

    def read_profile(self, user_id):

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