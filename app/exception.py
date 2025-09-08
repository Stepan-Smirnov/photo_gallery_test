from fastapi import HTTPException, status


class CustomExceptions(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjNotFound(CustomExceptions):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "object not found"


class ValueIsSpace(CustomExceptions):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "value is space"
