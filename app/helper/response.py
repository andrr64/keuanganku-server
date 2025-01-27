from typing import Any

class HelperResponse:
    def __init__(self, success: bool, message: str, data: Any = None):
        self.success = success
        self.message = message
        self.data = data

    def to_dict(self):
        """
        Mengubah objek HelperResponse menjadi dictionary untuk pengembalian API.
        """
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
        }
    
    @staticmethod
    def error(err_message: str):
        return HelperResponse(success=False, message=err_message)
    
    @staticmethod
    def success(data: Any, message: str="OK"):
        return HelperResponse(message=message, data=data, success=True)