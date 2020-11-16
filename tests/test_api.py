from io import BytesIO


def test_get_all(test_client):
    response = test_client.get('/airports')
    assert 200 == response.status_code
    assert 0 == len(response.json)


def test_post(test_client):
    response = test_client.post('/airports', json=airport)
    assert 201 == response.status_code
    assert 1 == response.json.get('id')


def test_get_all_with_data(test_client):
    response = test_client.get('/airports')
    assert 200 == response.status_code
    assert 1 == len(response.json)


def test_get_by_id(test_client):
    response = test_client.get('/airports/1')
    assert 200 == response.status_code
    assert "Airport 1" == response.json.get('name')


def test_delete(test_client):
    response = test_client.delete('/airports/1')
    assert 204 == response.status_code
    response = test_client.get('/airports/1')
    assert 404 == response.status_code


def test_update(test_client):
    response = test_client.post('/airports', json=airport)
    assert 201 == response.status_code
    response = test_client.put('/airports/1', json=airport_update)
    assert 201 == response.status_code
    assert "Airport updated" == response.json.get('name')
    assert "new city" == response.json.get('city')


def test_upload(test_client):
    data = dict(
        file=(BytesIO(b'my file contents'), "airports.csv"),
    )

    response = test_client.post('/airports/upload',
                                content_type='multipart/form-data',
                                data=data)
    assert 201 == response.status_code


def test_webhook(test_client):
    response = test_client.post('/airports/webhook', json=airport)
    assert 200 == response.status_code


airport = {
        "id": 1,
        "name": "Airport 1",
        "city": "A city",
        "country": "A country",
        "iata": "IATA",
        "icao": "ICAO",
        "latitude": 1.1,
        "longitude": 2.2,
        "altitude": 100,
        "timezone": 1,
        "DST": "DST",
        "tz": "tz/tz",
        "type": "airport",
        "source": "data"
    }

airport_update = {"name": "Airport updated", "city": "new city"}
