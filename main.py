from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from routers import user, conferenceroom, slotbooking
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Slotbooking",
        "description": "Manage slot booking for conference rooms.",
    },
    {
        "name": "Conferencerooms",
        "description": "Manage conference rooms.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(user.router)
app.include_router(conferenceroom.router)
app.include_router(slotbooking.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_tortoise(
        app,
        db_url="postgres://postgres:root@localhost:5432/bookingapp",
        modules={
            "models": ["models"],
        },
        generate_schemas=True,
        add_exception_handlers=True
    )