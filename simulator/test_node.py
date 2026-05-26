from database_node import DatabaseNode

site1 = DatabaseNode(
    "Site1",
    "localhost",
    5434
)

print(
    site1.acquire_lock(
        1,
        "TX-001"
    )
)

print(
    site1.acquire_lock(
        1,
        "TX-002"
    )
)

print(
    "Conflicts:",
    site1.conflict_count
)

site1.release_lock(
    1,
    "TX-001"
)