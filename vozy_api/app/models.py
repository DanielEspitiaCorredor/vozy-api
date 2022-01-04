from vozy_api.db_config import db
from datetime import datetime

class Post(db.Document):
    created_at   = db.DateTimeField()
    owner_id     = db.StringField(required=True) # User that make the post
    text         = db.StringField(required=True)
    source       = db.StringField(required=True)
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        
        return super(Post, self).save(*args, **kwargs)
        
    def process_post_item(self):
        item_dict = self.to_mongo().to_dict()
        item_dict.pop("_id")
        item_dict['id'] = str(self.id)
        item_dict['created_at'] = self.created_at.isoformat()
        return item_dict
    
    def __repr__(self):
        return f'<Post {str(self.id)}>'