from tortoise import models, fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime

Tortoise.init_models(["__main__"], "models")

class ConferenceRoom(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    vacant = fields.BooleanField(default=True)
    description = fields.TextField(null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name

ConferenceRoom_Pydantic = pydantic_model_creator(ConferenceRoom,name="ConferenceRoom")
ConferenceRoomIn_Pydantic = pydantic_model_creator(ConferenceRoom,name="ConferenceRoomIn", exclude_readonly=True)
ConferenceRoomB_Pydantic = pydantic_model_creator(ConferenceRoom,name="ConferenceRoomB", include=['id'])


class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name

User_Pydantic = pydantic_model_creator(User,name="User")
UserIn_Pydantic = pydantic_model_creator(User,name="UserIn", exclude_readonly=True)
UserB_Pydantic = pydantic_model_creator(User,name="UserB", include=['id'])
UserLogin_Pydantic = pydantic_model_creator(User,name="UserLogin", include=['email','password'])


class BookingSlots(models.Model):
    id = fields.IntField(pk=True)
    is_active = fields.BooleanField(default=True)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    user  = fields.ForeignKeyField('models.User', related_name='booking_slots_user')
    conference_room  = fields.ForeignKeyField('models.ConferenceRoom', related_name='booking_slots_room')


    def __str__(self):
        return f'{self.conference_room.name} - {self.start_time} - {self.end_time} - {self.user.name}'

BookingSlots_Pydantic = pydantic_model_creator(BookingSlots,name="BookingSlots", include=['id', 'conference_room', 'user', 'start_time', 'end_time','created_at','updated_at'])
BookingSlotsIn_Pydantic = pydantic_model_creator(BookingSlots,name="BookingSlotsIn", exclude_readonly=True)