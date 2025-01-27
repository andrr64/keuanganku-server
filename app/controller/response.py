class ControllerResponse:
    def __init__(self, success: bool, message: str, data: any= None, http_code: int= 200):
        self.message = message
        self.data = data
        self.success = success
        self.http_code = http_code
    
    def to_dict_error(self) -> dict:
        return {
            "status": self.success,
            "message": self.message
        }
    def to_dict(self) -> dict:
        return {
            "status": self.success,
            "message": self.message,
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