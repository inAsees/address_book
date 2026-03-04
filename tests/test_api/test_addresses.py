import pytest
from fastapi import status


def test_create_address(client):
    address_data = {
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    response = client.post("/api/v1/addresses/", json=address_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["latitude"] == 40.7128
    assert data["longitude"] == -74.0060
    assert "id" in data
    assert "created_at" in data


def test_create_address_invalid_latitude(client):
    address_data = {
        "latitude": 100.0,
        "longitude": -74.0060
    }
    response = client.post("/api/v1/addresses/", json=address_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_address(client):
    # Create address first
    create_resp = client.post("/api/v1/addresses/", json={
        "latitude": 40.7128,
        "longitude": -74.0060
    })
    address_id = create_resp.json()["id"]

    response = client.get(f"/api/v1/addresses/{address_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == address_id


def test_get_address_not_found(client):
    response = client.get("/api/v1/addresses/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_address(client):
    # Create
    create_resp = client.post("/api/v1/addresses/", json={
        "latitude": 40.7128,
        "longitude": -74.0060
    })
    address_id = create_resp.json()["id"]

    # Update coordinates
    update_data = {"latitude": 40.6782, "longitude": -73.9442}
    response = client.put(f"/api/v1/addresses/{address_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["latitude"] == 40.6782
    assert data["longitude"] == -73.9442


def test_delete_address(client):
    # Create
    create_resp = client.post("/api/v1/addresses/", json={
        "latitude": 40.7128,
        "longitude": -74.0060
    })
    address_id = create_resp.json()["id"]

    # Delete
    response = client.delete(f"/api/v1/addresses/{address_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deleted
    get_resp = client.get(f"/api/v1/addresses/{address_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


def test_nearby_addresses(client):
    # Create two addresses with known coordinates
    addr1 = client.post("/api/v1/addresses/", json={
        "latitude": 40.7128,
        "longitude": -74.0060  # NYC
    }).json()

    addr2 = client.post("/api/v1/addresses/", json={
        "latitude": 40.7580,
        "longitude": -73.9855  # Times Square (approx 5km)
    }).json()

    # Query nearby from addr1
    response = client.get(
        f"/api/v1/addresses/nearby/?latitude={addr1['latitude']}&longitude={addr1['longitude']}&distance_km=10"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    assert "distance_km" in data[0]