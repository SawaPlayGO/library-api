from jose import jwt
from config import settings


class JWT:
    """Класс для работы с JWT токенами"""
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_token(self, payload: dict) -> str:
        """
        Генерация JWT токена

        :param payload: словарь с данными для токена. Данные не должны быть пустыми.

        :return: JWT токен
        """
        assert payload, 'Payload для токена не может быть пустым'
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> dict:
        """
        Проверка JWT токена

        :param token: JWT токен

        :return: словарь с данными из токена
        """
        return jwt.decode(token, self.secret_key, algorithms=self.algorithm)
    
jwt_handler = JWT(secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)