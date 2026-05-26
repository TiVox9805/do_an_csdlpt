import pandas as pd
import psycopg2

CSV_FILE = "../data/data.csv"

PORTS = [
    5434,
    5435,
    5436
]

df = pd.read_csv(CSV_FILE)

for port in PORTS:

    print(f"Importing Site {port}")

    conn = psycopg2.connect(
        host="localhost",
        port=port,
        database="profile_service",
        user="quorum",
        password="quorum123"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM user_profiles"
    )

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT INTO user_profiles(
                user_id,
                age,
                gender,
                department,
                job_role,
                marital_status,
                monthly_income
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                int(row["EmployeeNumber"]),
                int(row["Age"]),
                row["Gender"],
                row["Department"],
                row["JobRole"],
                row["MaritalStatus"],
                int(row["MonthlyIncome"])
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    print(
        f"Site {port} imported {len(df)} records"
    )

print("Replication completed")