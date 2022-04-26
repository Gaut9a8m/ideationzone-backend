from fastapi import APIRouter, HTTPException
from models import ConferenceRoom_Pydantic, ConferenceRoomIn_Pydantic, ConferenceRoom 

router = APIRouter(prefix="/conference_rooms", tags=["Conferencerooms"])

#conferenceroom creation
@router.post("/add/")
async def create_conference_room(conference_room: ConferenceRoomIn_Pydantic):
    try:
        obj = await ConferenceRoom.filter(name=conference_room.dict()['name']).first()
        if obj:
            raise Exception("Conference room already exists")
        else:
            conference_room = await ConferenceRoom.create(**conference_room.dict(exclude_unset=True))
            return await ConferenceRoom_Pydantic.from_tortoise_orm(conference_room)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')

#conferenceroom listing all
@router.get("/")
async def get_conference_room():
    try:
        return await ConferenceRoom_Pydantic.from_queryset(ConferenceRoom.all())
    except Exception as e:
        raise HTTPException(status_code=404 ,detail=f"Conference room not found. {e}")

#conferenceroom listing by id
@router.get("/{conference_room_id}", response_model = ConferenceRoom_Pydantic)
async def get_conference_room_by_id(conference_room_id: int):
    try:
        return await ConferenceRoom_Pydantic.from_queryset_single(ConferenceRoom.get(id=conference_room_id))
    except Exception as e:
        raise HTTPException(status_code=404 ,detail=f"Conference room not found. {e}")

#conferenceroom update
@router.put("/{conference_room_id}")
async def update_conference_room(conference_room_id: int, conference_room: ConferenceRoomIn_Pydantic):
    try:
        obj = await ConferenceRoom.filter(id=conference_room_id).first()
        if obj:
            await ConferenceRoom.filter(id=conference_room_id).update(**conference_room.dict(exclude_unset=True))
            return await ConferenceRoom_Pydantic.from_queryset_single(ConferenceRoom.get(id=conference_room_id))
        else:
            raise Exception("Conference room not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')

#conferenceroom delete
@router.delete("/{conference_room_id}")
async def delete_conference_room(conference_room_id: int):
    try:
        obj = await ConferenceRoom.filter(id=conference_room_id).first()
        if obj:
            await ConferenceRoom.filter(id=conference_room_id).update(is_active=False)
            return {"message": "Conference room deleted successfully"}
        else:
            raise Exception("Conference room not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')