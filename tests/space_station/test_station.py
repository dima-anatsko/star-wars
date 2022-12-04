import pytest
from django.core.exceptions import ObjectDoesNotExist

from space_station.models import Instruction, Station

STATIONS_URL = '/api/v1/stations/'
TEMPLATE_STATION_URL = '/api/v1/stations/{pk}/'
TEMPLATE_POSITION_URL = '/api/v1/stations/{pk}/state/'


@pytest.mark.django_db
def test_permissions(client, auth_client):
    assert client.get(STATIONS_URL).status_code == 403
    assert auth_client.get(STATIONS_URL).status_code == 200


@pytest.mark.django_db
def test_create_station(auth_client):
    payload = {'name': 'Death Star'}
    response = auth_client.post(STATIONS_URL, payload)
    data = response.data

    station_from_db = Station.objects.first()

    assert data['id'] == station_from_db.id
    assert data['name'] == station_from_db.name
    assert data['status'] == station_from_db.get_status_display()


@pytest.mark.django_db
def test_get_list_of_stations(auth_client):
    Station.objects.bulk_create(
        [
            Station(name='Death Star'),
            Station(name='Death Star 2'),
        ]
    )

    response = auth_client.get(STATIONS_URL)

    stations_from_db = Station.objects.all()

    assert response.status_code == 200
    assert len(response.data) == stations_from_db.count()


@pytest.mark.django_db
def test_get_station_detail_404(auth_client):
    response = auth_client.get(TEMPLATE_STATION_URL.format(pk=0))
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_station(auth_client):
    station = Station.objects.create(name='Death Star')

    url = TEMPLATE_STATION_URL.format(pk=station.pk)
    payload = {'name': 'Union'}
    response = auth_client.put(url, payload)

    station.refresh_from_db()

    assert response.status_code == 200
    assert response.data['name'] == station.name


@pytest.mark.django_db
def test_patch_station(auth_client):
    station = Station.objects.create(name='Death Star')

    url = TEMPLATE_STATION_URL.format(pk=station.pk)
    payload = {'name': 'Union'}
    response = auth_client.patch(url, payload)

    station.refresh_from_db()

    assert response.status_code == 200
    assert response.data['name'] == station.name


@pytest.mark.django_db
def test_delete_station(auth_client):
    station = Station.objects.create(name='Death Star')

    url = TEMPLATE_STATION_URL.format(pk=station.pk)

    response = auth_client.delete(url)

    assert response.status_code == 204

    with pytest.raises(ObjectDoesNotExist):
        station.refresh_from_db()


@pytest.mark.django_db
def test_create_position_after_created_station(auth_client):
    payload = {'name': 'Death Star'}
    response = auth_client.post(STATIONS_URL, payload)

    station_data = response.data

    url = TEMPLATE_POSITION_URL.format(pk=station_data['id'])
    response = auth_client.get(url)
    position_data = response.data

    default_position = 100

    assert response.status_code == 200
    assert position_data['x'] == default_position
    assert position_data['y'] == default_position
    assert position_data['z'] == default_position


@pytest.mark.django_db
def test_create_instruction(auth_client, user):
    station = Station.objects.create(name='Death Star')

    url = TEMPLATE_POSITION_URL.format(pk=station.id)
    payload = {
        'station': station.id,
        'axis': 'x',
        'distance': -20,
    }
    response = auth_client.post(url, payload)

    assert response.status_code == 201

    position_data = response.data

    assert position_data['x'] == 80

    instruction = Instruction.objects.first()

    assert instruction.user_id == user.id
    assert instruction.station_id == station.id
    assert instruction.axis == 'x'
    assert instruction.distance == -20


@pytest.mark.django_db
def test_broke_station(auth_client, user):
    station = Station.objects.create(name='Death Star')

    # first instruction
    Instruction.objects.create(
        user_id=user.id,
        station_id=station.id,
        axis='y',
        distance=-101,
    )

    station.refresh_from_db()

    assert station.status == Station.Status.BROKEN
    assert station.position.y == -1

    # second instruction
    Instruction.objects.create(
        user_id=user.id,
        station_id=station.id,
        axis='y',
        distance=10,
    )

    station.refresh_from_db()

    assert station.status == Station.Status.BROKEN
    assert station.position.y == 9
