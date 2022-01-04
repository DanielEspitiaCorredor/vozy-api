# 4xx Errors
ERR_NOT_JSON_PAYLOAD = ({"message": "This endpoint only allows json payload"}, 400)
ERR_INVALID_PARAMS   = ({"message": "Invalid params"}, 400)
ERR_INVALID_QUERY    = ({"message": "Invalid query"}, 400)
ERR_REGISTER_ERROR = ({"message": "The user could not be registered. Please try again"}, 400)
ERR_AUTH = ({"message": "Invalid user or password"}, 400)
ERR_POST_NOT_FOUND  = ({"message": "Post not found"}, 400)

# 5xx Errors
ERR_UNCONTROLLED_EXCEPTION = ({"message": "Uncontrolled exception"}, 500)