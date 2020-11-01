from flask_login import UserMixin
from mongoengine import Document, StringField, DateTimeField, IntField, FloatField
import datetime

class User(UserMixin, Document):
    username = StringField()
    email = StringField()
    password = StringField()
    date = DateTimeField(default = datetime.datetime.now())
    def to_json(self):
        return {"username": self.username,
                "email": self.email}
				
				
class Demographic(Document):
	subject = StringField()
	ptid = StringField()
	examdate = DateTimeField()
	viscode = StringField()
	dx_bl = StringField()
	age = FloatField()
	ptgender = StringField()
	pteducat = IntField()
	ptethcat = StringField()
	ptraccat = StringField()
	ptmarry = StringField()
	cdrsb = FloatField()
	mmse = FloatField()


class Matrix(Document):
	subject = StringField()
	content = StringField()
	