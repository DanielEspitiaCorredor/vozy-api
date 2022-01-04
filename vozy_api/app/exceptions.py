class PostNotFound(Exception):
    """
    Raised when a user post is not found in the database
    """
    def __init__(self, *args, **kwargs):
        self.message  = args[0]

    def __str__(self): 
        return self.message