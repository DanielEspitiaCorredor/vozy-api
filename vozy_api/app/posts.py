from app import app
from flask import request
from vozy_api import errors
from flask_jwt_extended import jwt_required, get_jwt_identity
from vozy_api.app.exceptions import PostNotFound
from vozy_api.app.models import Post
from vozy_api.decorators import validate_request
from vozy_api.transactions import DatabaseTransaction

from flask_mongoengine.pagination import Pagination
from vozy_api.db_config import ITEMS_PER_PAGE

MANAGE_POST_KEYS = {
    "POST": ["text", "source"],
    "PATCH": ["post_id", "data"],
    "DELETE": ["ids"]
}

# query managers
post_manager = DatabaseTransaction(model=Post)

@app.route("/posts", methods=["GET", "POST", "PATCH", "DELETE"])
@jwt_required()
@validate_request(body_keys=MANAGE_POST_KEYS)
def manage_post():
    """
    Endpoint used to manage posts in VozyApp
    

    Methods
    -------
    GET: List user post
    POST: Create new post
    PATCH: Update existing post
    DELETE: Remove a list of post
    
    Returns
    -------
    list|dict
        Json with query results
    """
    try:
        
        if request.method == 'GET':
            posts = post_manager.read(
                owner_id = get_jwt_identity()
            )
            
            args = request.args
            page = int(args.get("page", 1))
            
            paginator = Pagination(posts, page, per_page=ITEMS_PER_PAGE)
            print()
            return (
                {
                    "pages": paginator.pages,
                    "results": paginator.total,
                    "has_next": paginator.has_next,
                    "next": paginator.next_num if paginator.has_next else None,
                    "prev": paginator.prev_num if paginator.has_prev else None,
                    "data": [item.process_post_item() for item in paginator.items]
                }, 200
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            body['owner_id'] = get_jwt_identity()
            post = post_manager.create(
                **body
            )
            
            return (
                {
                    "post_id": str(post.id),
                    "message": "Post created"
                }, 200
            )
        elif request.method == "PATCH":
            body = request.get_json()
            post =post_manager.read(
                id=body['post_id']
            )
            
            if not post:
                raise PostNotFound(f"Post {body['post_id']} not found")
            
            post_manager.update(
                queryset=post,
                data=body['data']
            )
            print(post)
            return (
                {
                    "post_id": body['post_id'],
                    "message": "Post updated"
                }, 200
            )
        elif request.method == 'DELETE':
            body = request.get_json()
            posts =post_manager.read(
                id__in=body['ids']
            )
            
            post_manager.delete(
                queryset=posts
            )
            
            return (
                {
                    "message": "Done"
                }, 200
            )
    except PostNotFound as e:
        return errors.ERR_POST_NOT_FOUND
    except Exception as e:
        print(e)
        return errors.ERR_UNCONTROLLED_EXCEPTION
    