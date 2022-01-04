from vozy_api import errors
from flask import request


def validate_json_request(body_keys: list=[], allowed_params: list=[]):
    """
    Decorator used to validate json request. This function can also be used to validate GET parameters.
    """ 
    def inner(func):
        
        def wrapper(*args, **kwargs):
            try:
                if body_keys:
                    if not request.is_json:
                        return errors.ERR_NOT_JSON_PAYLOAD
                    validate_body(body=request.get_json(), body_keys=body_keys)
                
                if allowed_params:
                    validate_params(params=request.args, allowed_params=allowed_params)
                return func(*args, **kwargs)
            
            except ParameterError:
                return errors.ERR_INVALID_PARAMS
            
        wrapper.__name__ = func.__name__    
        return wrapper
    
    def validate_params(
        *,
        params: list,
        allowed_params: list
        ):
        
        for param in params:
            if param not in allowed_params:
                raise ParameterError("Invalid Parameter. Check the request")
    
    def validate_keys(
        *,
        keys: list,
        dictionary: dict
        ):
        for param in keys:
            if param not in dictionary.keys():
                raise ParameterError("Invalid Parameters. Check the request")
                  
    def validate_body(
        *,
        body: object,
        body_keys: list
        ):
        
        if isinstance(body, list):
            for element in body:
                validate_keys(
                    keys=body_keys,
                    dictionary=element
                )
        elif isinstance(body, dict):
            validate_keys(
                keys=body_keys,
                dictionary=body
            )
    
    
    return inner


# Errors
class ParameterError(Exception):
    """
    Raised when a request doesn't have any mandatory parameter
    """
    def __init__(self, *args, **kwargs):
        self.message  = args[0]

    def __str__(self): 
        return self.message