class TaggerError(Exception):
   def __init__(self, msg, src): 
        self.msg = msg
        self.src = src

class ModuleTaggerError(TaggerError):
   def __init__(self, msg, src): 
        super().__init__(msg, src)