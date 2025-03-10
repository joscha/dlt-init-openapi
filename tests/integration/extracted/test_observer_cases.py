#
# Test different iterations of observer spec: FastAPI generated
#
from tests.integration.utils import get_dict_by_case


def test_simple_observer_load() -> None:
    source = get_dict_by_case("extracted", "observer_with_pagination.yml")
    assert len(source["resources"]) == 2

    assert source["client"]["paginator"] == {
        "type": "offset",
        "limit": 100,
        "offset_param": "offset",
        "limit_param": "limit",
        "total_path": "total",
    }

    assert source["resources"][1] == {
        "name": "user_response",
        "table_name": "user_response",
        "primary_key": "id",
        "write_disposition": "merge",
        "endpoint": {
            "params": {},
            "data_selector": "items",
            "path": "/admin/users",
        },
    }
    assert source["resources"][0] == {
        "name": "office_response",
        "table_name": "office_response",
        "primary_key": "id",
        "write_disposition": "merge",
        "endpoint": {
            "params": {},
            "data_selector": "items",
            "path": "/offices",
        },
    }
