from vozy_api.db_config import db
from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
    name         = StringField(max_length=50)
    username     = StringField(max_length=50, required=True)
    email        = EmailField(required=True)
    password     = StringField(required=True)
    created_at   = DateTimeField()
    last_modified   = DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.last_modified = datetime.now()
        
        return super(User, self).save(*args, **kwargs)
    
    def __repr__(self):
        return f'<User {self.username!r}>'