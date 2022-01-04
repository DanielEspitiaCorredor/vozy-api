class RegisterError(Exception):
    """
    Raised when a user exist in the database
    """
    def __init__(self, *args, **kwargs):
        self.message  = args[0]

    def __str__(self): 
        return self.message