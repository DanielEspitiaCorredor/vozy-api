from vozy_api.database import db
import mongoengine
from datetime import datetime

class User(db.Document):
    name         = db.StringField(max_length=50)
    username     = db.StringField(max_length=50, required=True)
    email        = db.EmailField(required=True)
    password     = db.StringField(required=True)
    created_at   = db.DateTimeField()
    last_modified   = db.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.last_modified = datetime.now()
        
        return super(User, self).save(*args, **kwargs)
    
    def __repr__(self):
        return f'<User {self.username!r}>'