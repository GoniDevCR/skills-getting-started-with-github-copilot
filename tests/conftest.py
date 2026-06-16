import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src import app as app_module

_initial_activities = deepcopy(app_module.activities)

@pytest.fixture
def client():
    return TestClient(app_module.app)

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = deepcopy(_initial_activities)
