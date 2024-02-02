from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

import json
import pytest
import api_helpers


import json
import pytest

# Define test data
@pytest.fixture
def new_order_data():
    return {
        "pet_id": 0
        
    }

# Test the POST request to place a new order
def test_place_new_order(new_order_data):
    response = api_helpers.post_api_data("/store/order", data=json.dumps(new_order_data))
    
    assert response.status_code == 201  # Check if the order is created successfully
    response_data = response.json()
    assert 'id' in response_data
    assert 'pet_id' in response_data
    assert response_data['pet_id'] == new_order_data['pet_id']


# Test the PATCH request to update the order status
def test_update_order_status(new_order_data):
    # First, create a new order
    new_order_data['pet_id'] = 2
    response = api_helpers.post_api_data("/store/order", data=json.dumps(new_order_data))
    assert response.status_code == 201
    order_id = response.json()["id"]

    # Update the order status
    update_data = {"status": "sold"}  # Example update data
    response = api_helpers.patch_api_data(f"/store/order/{order_id}", data=update_data)
    # Validate the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Order and pet status updated successfully"

