import pytest
from httpx import AsyncClient, Response


async def test_add_and_get_note(
    room_id,
    date_from,
    date_to,
    status_code,
    booked_rooms,
    authenticated_ac: AsyncClient,
):
    response: Response = await authenticated_ac.post(
        url="/notes",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    response: Response = await authenticated_ac.get(url="/bookings")

    assert booked_rooms == len(response.json())