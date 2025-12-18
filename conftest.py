import sys
import os
import pytest
from unittest.mock import Mock

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)

from burger import Burger

@pytest.fixture
def burger():
    return Burger()

@pytest.fixture
def bun_mock():
    bun = Mock()
    bun.get_price.return_value = 100.0
    bun.get_name.return_value = "Булка"
    return bun

@pytest.fixture
def ingredient_mock():
    ing = Mock()
    ing.get_price.return_value = 50.0
    ing.get_name.return_value = "Сыр"
    ing.get_type.return_value = "FILLING"
    return ing