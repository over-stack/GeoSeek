class InvalidTokenType(Exception):
    def __init__(self, token_type):
        self.token_type = token_type
        self.message = f"Invalid token type: {token_type}"
        super().__init__(self.message)


class TokenNotFoundError(Exception):
    def __init__(self, token):
        self.message = f"Token not found: {token}"
        super().__init__(self.message)
