class BodyNotJsonError(Exception):
    def __init__(self, code: int = 5051, message: str = "请求体非Json", status_code: int = 505):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)
