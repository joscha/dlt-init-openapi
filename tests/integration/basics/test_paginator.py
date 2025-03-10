from typing import Any, Dict

import pytest

from dlt_init_openapi.config import Config
from dlt_init_openapi.detector.default.warnings import PossiblePaginatorWarning
from tests.integration.utils import get_dict_by_case, get_indexed_resources, get_project_by_case


@pytest.fixture(scope="module")
def paginators() -> Dict[str, Any]:
    resources = get_indexed_resources("artificial", "pagination.yml", config=Config(name_resources_by_operation=True))
    return {name: resource.get("endpoint").get("paginator") for name, resource in resources.items()}  # type: ignore


def test_offset_limit_pagination_1(paginators: Dict[str, Any]) -> None:
    assert paginators["offset_limit_pagination_1"] == {
        "limit": 20,
        "limit_param": "limit",
        "offset_param": "offset",
        "type": "offset",
        "total_path": "count",
    }


def test_offset_limit_pagination_no_count_1(paginators: Dict[str, Any]) -> None:
    assert paginators["offset_limit_pagination_no_count_1"] == {
        "limit": 20,
        "limit_param": "limit",
        "offset_param": "offset",
        "type": "offset",
        "maximum_offset": 20,
        "total_path": "",
    }


def test_json_links_pagination_1(paginators: Dict[str, Any]) -> None:
    assert paginators["json_links_pagination_1"] == {
        "next_url_path": "next",
        "type": "json_response",
    }


def test_json_cursor_1(paginators: Dict[str, Any]) -> None:
    assert paginators["cursor_pagination_1"] == {"cursor_param": "cursor", "cursor_path": "cursor", "type": "cursor"}


def test_page_number_paginator_no_count(paginators: Dict[str, Any]) -> None:
    assert paginators["page_number_paginator_no_count"] == {
        "type": "page_number",
        "page_param": "page",
        "maximum_page": 20,
        "total_path": "",
    }


def test_page_number_paginator_with_count(paginators: Dict[str, Any]) -> None:
    assert paginators["page_number_paginator_with_count"] == {
        "type": "page_number",
        "page_param": "page",
        "total_path": "count",
    }


def test_global_paginator() -> None:
    api_dict = get_dict_by_case("artificial", "global_pagination.yml", config=Config(name_resources_by_operation=True))
    # we have a global cursor paginator
    assert api_dict["client"]["paginator"] == {
        "type": "cursor",
        "cursor_path": "cursor",
        "cursor_param": "cursor",
    }

    # check endpoint pagination settings
    resources: Any = {entry["name"]: entry for entry in api_dict["resources"]}  # type: ignore
    assert not resources["item_endpoint"]["endpoint"].get("paginator")
    assert not resources["collection_1"]["endpoint"].get("paginator")
    assert not resources["collection_2"]["endpoint"].get("paginator")

    # there is a different paginator on the diverging endpoint
    assert resources["collection_other_paginator"]["endpoint"].get("paginator") == {
        "page_param": "page",
        "total_path": "count",
        "type": "page_number",
    }


def test_incomplete_paginator_warning() -> None:
    project = get_project_by_case("artificial", "pagination.yml", config=Config(name_resources_by_operation=True))

    # check if the warnings exist that we expect
    warnings = project.detector.get_warnings()

    # warning for possible paginator
    assert len(warnings.get("cursor_pagination_incomplete")) == 2
    assert type(warnings.get("cursor_pagination_incomplete")[0]) == PossiblePaginatorWarning
    assert warnings.get("cursor_pagination_incomplete")[0].params == ["cursor"]  # type: ignore
