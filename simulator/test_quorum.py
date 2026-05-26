from database_node import DatabaseNode
from coordinator import QuorumCoordinator

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
site3.slow_mode = True
coordinator = QuorumCoordinator(
    [
        site1,
        site2,
        site3
    ]
)

result = coordinator.update_department(
    user_id=1,
    new_department="Research"
    
)


print(result)