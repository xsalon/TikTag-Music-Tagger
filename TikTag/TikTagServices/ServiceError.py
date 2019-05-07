class ServiceError(Exception):
   def __init__(self, code, msg): 
        self.code = code
        self.msg = msg

class ServiceRequirement(ServiceError):
    def __init__(self, code, msg, url): 
        self.url = url
        super().__init__(code, msg)
