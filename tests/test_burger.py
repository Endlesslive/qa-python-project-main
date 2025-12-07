import os
import sys
import pytest 
from unittest.mock import Mock
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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


def test_set_buns_sets_bun(burger, bun_mock):
    burger.set_buns(bun_mock)
    assert burger.bun is bun_mock


def test_add_ingredient_appends_to_list(burger, ingredient_mock):
    burger.add_ingredient(ingredient_mock)
    assert burger.ingredients == [ingredient_mock]


@pytest.mark.parametrize(
    "start_count, index_to_remove",
    [
        (3, 0),
        (3, 1),
        (3, 2),
    ],
)
def test_remove_ingredient_by_index(burger, ingredient_mock, start_count, index_to_remove):
    # arrange
    for _ in range(start_count):
        burger.add_ingredient(ingredient_mock)

    # act
    burger.remove_ingredient(index_to_remove)

    # assert
    assert len(burger.ingredients) == start_count - 1
    assert ingredient_mock in burger.ingredients


@pytest.mark.parametrize(
    "ingredients_order,new_index,expected_order",
    [
        # index всегда 0, поэтому:
        # если new_index == 0 — порядок не меняется
        ([0, 1, 2], 0, [0, 1, 2]),
        # если new_index == 1 — первый элемент уезжает на позицию 1
        ([0, 1, 2], 1, [1, 0, 2]),
        # если new_index == 2 — первый элемент уезжает в конец
        ([0, 1, 2], 2, [1, 2, 0]),
    ],
)
def test_move_ingredient_changes_position(burger, ingredients_order, new_index, expected_order):
    ingredients = [Mock(name=f"ing{i}") for i in ingredients_order]
    burger.ingredients = ingredients.copy()

    burger.move_ingredient(index=0, new_index=new_index)

    assert [ing._extract_mock_name() for ing in burger.ingredients] == [
        f"ing{i}" for i in expected_order
    ]

def test_get_price_uses_bun_and_ingredients_prices(burger, bun_mock, ingredient_mock):
    burger.set_buns(bun_mock)
    burger.add_ingredient(ingredient_mock)
    burger.add_ingredient(ingredient_mock)

    price = burger.get_price()

    # 2 булки * 100 + 2 ингредиента * 50 = 300
    assert price == 300.0
    bun_mock.get_price.assert_called()
    assert ingredient_mock.get_price.call_count == 2


def test_get_receipt_format(burger, bun_mock, ingredient_mock):
    burger.set_buns(bun_mock)
    burger.add_ingredient(ingredient_mock)

    receipt = burger.get_receipt()

    # базовые проверки структуры, детали строки зависят от твоей реализации
    assert bun_mock.get_name.return_value in receipt
    assert ingredient_mock.get_name.return_value in receipt
    assert str(burger.get_price()) in receipt
