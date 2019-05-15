# File: TaggerError.py
# Project: TikTag
# Author: Marek Salon (xsalon00)
# Contact: xsalon00@stud.fit.vutbr.cz
# Date: 10.5.2019
# Description: Tagger exceptions

class TaggerError(Exception):
   """Base tagger error"""
   def __init__(self, msg, src): 
        self.msg = msg
        self.src = src

class ModuleTaggerError(TaggerError):
   """Error from format classes"""
   def __init__(self, msg, src): 
        super().__init__(msg, src)