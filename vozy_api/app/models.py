from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Post(Document):
    created_at   = DateTimeField()
    owner_id     = StringField(required=True) # User that make the post
    text         = StringField(required=True)
    source       = StringField(required=True)
    
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