from slowapi import Limiter
from slowapi.util import get_remote_address

# Создание экземпляра лимитера с использованием IP как ключа
limiter = Limiter(key_func=get_remote_address)
