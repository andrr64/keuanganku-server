from fastapi import status, Response
from os import getenv
from typing import Callable
from fastapi import HTTPException
debug= getenv('debug') == 'yes'

class ControllerResponse:
    def __init__(self, success: bool, message: str, data: any= None, http_code: int= 200):
        self.detail = message
        self.data = data
        self.success = success
        self.http_code = http_code
    
    def to_dict_error(self) -> dict:
        return {
            "status": self.success,
            "detail": self.detail
        }
    def to_dict(self) -> dict:
        return {
            "status": self.success,
            "detail": self.detail,
            "data": self.data
        }
    
    @staticmethod
    def success(message: str= "OK", data: any= None):
        return ControllerResponse(success=True, data=data, message=message)
    
    @staticmethod
    def error(err_message: str, http_code: int = 500, data: any=None):
        return ControllerResponse(success=False, data=data, message=err_message, http_code=http_code)
    
    @staticmethod
    def bad_request(err_message: str = "Bad Request", data: any = None):
        return ControllerResponse(success=False, data=data, message=err_message, http_code=400)

    @staticmethod
    def unauthorized(err_message: str = "Unauthorized", data: any = None):
        return ControllerResponse(success=False, data=data, message=err_message, http_code=401)

    @staticmethod
    def forbidden(err_message: str = "Forbidden", data: any = None):
        return ControllerResponse(success=False, data=data, message=err_message, http_code=403)

    @staticmethod
    def not_found(err_message: str = "Not Found", data: any = None):
        return ControllerResponse(success=False, data=data, message=err_message, http_code=404)
    
    @staticmethod
    def conflict(err_message: str = "Conflict", data: any= None):
        return ControllerResponse(success=False, data=data, message=err_message, http_code=status.HTTP_409_CONFLICT)
    
def handle_controller_response(ctrl_res: ControllerResponse, fn_suc: Callable[[ControllerResponse], any] = None):
    if not ctrl_res.success:
        raise HTTPException(
            status_code=ctrl_res.http_code,
            detail=ctrl_res.message
        )
    if fn_suc:
        return fn_suc(ctrl_res)
    return ctrl_res.to_dict()