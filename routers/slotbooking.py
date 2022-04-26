from fastapi import APIRouter, HTTPException
from models import BookingSlots_Pydantic, BookingSlotsIn_Pydantic, BookingSlots, ConferenceRoomB_Pydantic, UserB_Pydantic, ConferenceRoom_Pydantic, User_Pydantic
from models import User, ConferenceRoom

router = APIRouter(prefix="/slot", tags=["Slotbooking"])

#get all slots
@router.get("/")
async def get_all_slots():
    try:
        obj = BookingSlots.all()
        return {
            'msg':'success',
            'data':await BookingSlots_Pydantic.from_queryset(obj)
        }
    except Exception as e:
        raise HTTPException(status_code=404 ,detail=f"Slot data not found. {e}")

#get slot by id
@router.get("/{slot_id}")
async def get_slot_by_id(slot_id: int):
    try:
        slot_obj = await BookingSlots.get(id=slot_id)
        user_obj = await User_Pydantic.from_queryset_single(slot_obj.user)
        conf_obj = await ConferenceRoom_Pydantic.from_queryset_single(slot_obj.conference_room)
        print('user=',user_obj)
        print('user=',conf_obj)
        slots_response = []
        try:
            slots_response = await BookingSlots_Pydantic.from_queryset_single(slot_obj)
        except Exception as e:
            print('ERROR:', e)
        return {
            "slots": slots_response,
            "user": {
                "name":user_obj.name,
                "email":user_obj.email
            },
            "room": {
                "name": conf_obj.name,
                "vacant": conf_obj.vacant,
                "is_active": conf_obj.is_active
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404 ,detail=f"Slot not found. {e}")

#create slot
@router.post("/add/")
async def create_slot(slot: BookingSlotsIn_Pydantic, user_id:UserB_Pydantic, conference_room_id:ConferenceRoomB_Pydantic):
    try:
        try:
            user_obj = await User.get(id=user_id.dict()['id'])
            conf_obj = await ConferenceRoom.get(id=conference_room_id.dict()['id'])
        except Exception as e:
            raise Exception('User or Conference room not found')

        from_date = slot.dict()['start_time']
        to = slot.dict()['end_time']
    
        if from_date > to:
            raise Exception('Start time should be less than end time')
    
        slots = await BookingSlots.filter(start_time__range=(from_date,to), is_active=True, conference_room__vacant=True)
        if slots :
            raise Exception("Slot already exists")
        else:
            body = slot.dict(exclude_unset=True)
            slot = await BookingSlots.create(**body, user=user_obj, conference_room = conf_obj)
            res = await BookingSlots_Pydantic.from_tortoise_orm(slot)
            return {
                    "msg": "Slot created successfully",
                    "slot":res,
                    "user": {
                        "name":slot.user.name,
                        "email":slot.user.email
                    },
                    "room": {
                        "name": slot.conference_room.name,
                        "vacant": slot.conference_room.vacant,
                        "is_active": slot.conference_room.is_active
                    }
                }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')