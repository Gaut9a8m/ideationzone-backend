from fastapi import APIRouter, HTTPException
from models import User_Pydantic, UserIn_Pydantic, User, UserLogin_Pydantic
import re

router = APIRouter(prefix="/users", tags=["Users"])


#User creation
@router.post("/add/")
async def create_user(user: UserIn_Pydantic):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' #need to update regex for tradeindia email only
    try:
        useremail = user.dict()['email']
        if re.fullmatch(regex, useremail):
            obj = await User.filter(email=useremail).first()
            if obj:
                raise Exception("User already exists")
            else:
                    user = await User.create(**user.dict(exclude_unset=True))
                    return {
                        'data':await User_Pydantic.from_tortoise_orm(user),
                        'msg':'success'
                    }
        else:
            raise Exception('Invalid email')
    except Exception as e:
        raise HTTPException(status_code=400, msg=f'{e}')

#Get user by id
@router.get("/{user_id}/")
async def get_user(user_id: int):
    try:
        obj = User.get(id=user_id)
        data = await User_Pydantic.from_queryset_single(obj)
        res = {
            "data":data,
            "msg":'success'
        }
        return res
    except Exception as e:
        print('ERRPOR::: ', e)
        raise HTTPException(status_code=404 ,msg=f"User not found. {e}")


@router.post("/login/")
async def login(user: UserLogin_Pydantic):
    print('here')
    try:
        obj = await User.filter(email=user.dict()['email']).first()
        print('here111')
        if obj:
            if obj.password == user.dict()['password']:
                return {
                    'data':{
                        "email":obj.email,
                        "name":obj.name
                    },
                    'msg':'success'
                }
            else:
                raise Exception('Invalid password')
        else:
            raise Exception('Invalid email')
    except Exception as e:
        raise HTTPException(status_code=400, msg=f'{e}')