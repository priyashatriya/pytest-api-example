from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

import jsonschema

# Define the schema for a pet object
pet_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "type": {"type": "string"},
        "status": {"type": "string"},
        # Add more properties as needed
    },
    "required": ["id", "name", "type", "status"]  # Ensure required properties are present
}

def validate_pet_schema(pet):
    # Validate the pet object against the schema
    try:
        jsonschema.validate(instance=pet, schema=schemas.pet)
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Validation error for pet: {e}")


@pytest.mark.parametrize("status", [("available", "pending")])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    
    # Validate the response code is 200 OK
    assert response.status_code == 200, f"Response code is not 200 OK: {response.status_code}"
    # Parse the response JSON
    response_json = response.json()

    # Validate the 'status' property in each object in the response
    for pet in response_json:
        assert pet["status"] in status, f"Unexpected 'status' property in the response: {pet['status']}"

    # Validate the schema for each object in the response
    for pet in response_json:
        validate_pet_schema(pet)


def test_get_by_id_404():
    test_endpoint = "/pets/{pet_id}"  # Replace with the actual endpoint
    non_existing_pet_id = 999999  # Use a non-existing pet ID

    # Send a request to the API endpoint with a non-existing pet ID
    response = api_helpers.get_api_data(test_endpoint.format(pet_id=non_existing_pet_id))

    # Validate the response code is 404 Not Found
    assert response.status_code == 404, f"Response code is not 404: {response.status_code}"
