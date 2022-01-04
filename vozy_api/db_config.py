from app import app
from flask_mongoengine import MongoEngine

db = MongoEngine()
db.init_app(app)

# Pagination
ITEMS_PER_PAGE = 20