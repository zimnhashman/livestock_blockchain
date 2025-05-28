def has_access(role, department, location):
    allowed_roles = ["Admin", "Researcher"]
    allowed_departments = ["Livestock", "FieldOps"]
    allowed_locations = ["Farm001", "Farm002"]

    return (
        role in allowed_roles and
        department in allowed_departments and
        location in allowed_locations
    )
