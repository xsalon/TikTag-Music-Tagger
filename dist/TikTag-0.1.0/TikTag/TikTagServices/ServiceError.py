# File: ServiceError.py
# Project: TikTag
# Author: Marek Salon (xsalon00)
# Contact: xsalon00@stud.fit.vutbr.cz
# Date: 10.5.2019
# Description: Services exceptions

class ServiceError(Exception):
    """Base exception class for services"""
    def __init__(self, code, msg): 
        self.code = code
        self.msg = msg

class ServiceRequirement(ServiceError):
    """Exception class for services requirements"""
    def __init__(self, code, msg, url): 
        self.url = url
        super().__init__(code, msg)
