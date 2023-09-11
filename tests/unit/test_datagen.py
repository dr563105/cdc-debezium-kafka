from user_product_data import generate_user_data, generate_product_data
from typing import Dict, Any

def test_generate_user_data() -> None:
    """
    Test the generate_user_data function.

    Returns:
        None
    """
    user_data = generate_user_data(1)
    assert isinstance(user_data, dict)

    # Test that the generated username and email_address are not empty
    assert user_data["username"] != ""
    assert user_data["email_address"] != ""


def test_generate_product_data() -> None:
    """
    Test the generate_product_data function.

    Returns:
        None
    """
    product_data = generate_product_data(1)
    assert isinstance(product_data, dict)

    # Test that the generated name, description, and price are not empty or zero
    assert product_data["name"] != ""
    assert product_data["description"] != ""
    assert product_data["price"] > 0.0
