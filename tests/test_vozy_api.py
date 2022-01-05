from json import dumps
from unittest import TestCase

from mongoengine import connect, disconnect_all
from app import app
import json

from vozy_api.users.models import User
from vozy_api.app.models import Post
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_TEXT = 'text/plain'
class VozyAPITest(TestCase):
    
    default_user_password = "daniel.espitia99"
    default_access_token = None
    default_user = {
        "name": "Daniel Espitia",
        "username": "danielespitia",
        "email": "daniel@gmail.com",
        "password":  generate_password_hash(default_user_password, method="pbkdf2:sha256")
    }
    
    default_post_id = None
    default_posts = [
        {
            "source": "mobile",
            "text": "Diciembre es el mes para estar en familia"
        },
        {
            "source": "mobile",
            "text": "Hola soy Lili, encantada de conocerte."
        },
    ]
    
    def setUp(self) -> None:
        disconnect_all()
        connect(
            'vozytest',
            host='mongomock://localhost'
        )
        user = User(**self.default_user).save()
        with app.app_context():
            self.default_access_token = create_access_token(identity=str(user.id))
        
        self.headers = {'Authorization': f"Bearer {self.default_access_token}"}
        for post in self.default_posts:
            post['owner_id'] = str(user.id)
            post_obj = Post(**post).save()
            
            if not self.default_post_id:
                self.default_post_id = str(post_obj.id)

    def tearDown(self) -> None:
        disconnect_all()

    # User tests
    def test_register_succeeded(self):
        
        with app.test_client() as client:
            query = {
                "name": "Daniel Espitia",
                "username": "danielespitia1",
                "email": "daniel11@gmail.com",
                "password": self.default_user_password
            }
            
            response = client.post('/auth/register',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON)
            
            user = User.objects(username="danielespitia1").first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user.username, query['username'])
            self.assertEqual(user.email, query['email'])
    
    def test_user_already_exist(self):
        with app.test_client() as client:
            response = client.post('/auth/register',
                                   data=dumps(self.default_user),
                                   content_type=CONTENT_TYPE_JSON)
            
            self.assertEqual(response.status_code, 400)
    
    def test_register_fail(self):
        with app.test_client() as client:
            response = client.post('/auth/register',
                                   data=dumps(self.default_user),
                                   content_type=CONTENT_TYPE_TEXT)
            
            self.assertEqual(response.status_code, 400)
            
            bad_register_dict = self.default_user.copy()
            bad_register_dict.pop("username")
            
            response = client.post('/auth/register',
                                   data=dumps(bad_register_dict),
                                   content_type=CONTENT_TYPE_JSON)
            
            self.assertEqual(response.status_code, 400)
    
    def test_login_succeeded(self):
        query = {
            "username": self.default_user['username'],
            "password": self.default_user_password
        }
        
        response_expected_keys = ["access_token", "id"]
        with app.test_client() as client:
            response = client.post('/auth/login',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON)
            
            resp_dict = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertListEqual(list(resp_dict.keys()), response_expected_keys)
    
    def test_login_fail(self):
        query = {
            "username": self.default_user['username'],
            "password": self.default_user_password + "123"
        }
        
        with app.test_client() as client:
            response = client.post('/auth/login',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON)
            
            self.assertEqual(response.status_code, 400)
            # Invalid content type
            response = client.post('/auth/login',
                                   data=dumps(query),
                                   content_type='text/plain')
            
            self.assertEqual(response.status_code, 400)
            # Invalid content type
            query['user'] = query.pop("username")
            response = client.post('/auth/login',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON)
            
            self.assertEqual(response.status_code, 400)

    # Posts tests
    def test_create_posts(self):
        expected_posts = [
            {
                "source": "mobile",
                "text": "Hola de nuevo, este es un post de prueba para vozyapi"
            },
            {
                "source": "computer",
                "text": "Hola de nuevo, soy Lili de vozy app"
            },
            {
                "source": "mobile",
                "text": "Feliz año nuevo 2022 te desea Vozy"
            },
            {
                "source": "mobile",
                "text": "Todos los días de enero estan muy soleados"
            },
            
        ]
        
        response_expected_keys = ["message", "post_id"]
        
        
        with app.test_client() as client:
            
            for post in expected_posts:
                response = client.post('/posts',
                                    data=dumps(post),
                                    content_type=CONTENT_TYPE_JSON,
                                    headers=self.headers)
                
                self.assertEqual(response.status_code, 200)
                self.assertListEqual(list(response.get_json().keys()), response_expected_keys)
                
    def test_create_post_fail(self):
        query = {
            "source": "mobile",
            "text": "Hola de nuevo, este es un post de prueba para vozyapi"
        }
        
        with app.test_client() as client:
            # Invalid content type
            response = client.post('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_TEXT,
                                   headers=self.headers)
            
            self.assertEqual(response.status_code, 400)
            
            # Not authenticated
            response = client.post('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON)
            
            self.assertEqual(response.status_code, 401)
            
            # Invalid params
            query.pop("source")
            response = client.post('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON,
                                   headers=self.headers)
            
            self.assertEqual(response.status_code, 400)
    
    
    def test_update_post(self):
        query = {
            "post_id": self.default_post_id,
            "data": {
                "text": "Esta es una publicación actualizada en vozyapi",
                "source": "mobile"
            }
        }
        
        with app.test_client() as client:
            response = client.patch('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON,
                                   headers=self.headers)
            
            post = Post.objects(id=self.default_post_id).first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(post.text, query['data']['text'])
            
    
    def test_update_post_fail(self):
        query = {
            "post_id": self.default_post_id,
            "data": {
                "text": "Esta es una publicación actualizada en vozyapi",
                "source": "mobile"
            }
        }
        
        with app.test_client() as client:
            # Invalid content type
            response = client.patch('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_TEXT,
                                   headers=self.headers)
            
            self.assertEqual(response.status_code, 400)
            
            # Not authenticated
            response = client.patch('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON)
            
            self.assertEqual(response.status_code, 401)
            
            # Invalid params
            query.pop("post_id")
            response = client.patch('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON,
                                   headers=self.headers)
            
            self.assertEqual(response.status_code, 400)
            
    
    
    def test_list_posts(self):
        query = {
            "page": 1
        }
        with app.test_client() as client:
            response = client.get('/posts',
                                   query_string=query,
                                   headers=self.headers)
            resp_dict = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(resp_dict['data']), 0)
    
    
    def test_delete_post(self):
        query = {
            "ids": [
                self.default_post_id
            ]
        }
        
        with app.test_client() as client:
            response = client.delete('/posts',
                                   data=dumps(query),
                                   content_type=CONTENT_TYPE_JSON,
                                   headers=self.headers)
            
            post = Post.objects(id=self.default_post_id).first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(type(post), type(None))