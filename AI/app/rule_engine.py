from app.models import FieldSpec

def generate_scenarios(field_spec):
    scenarios = []

    if field_spec.required:
        if field_spec.data_type == 'integer':
            scenarios.append({
                "description": f"Field '{field_spec.name}' is present with valid data.",
                "data": {field_spec.name: field_spec.get_valid_data()}
            })
            scenarios.append({
                "description": f"Field '{field_spec.name}' is missing.",
                "data": {}
            })

    return scenarios