import logging
import redis
from fastapi import HTTPException, status
from core.config import settings

connection = settings.redis_connection_string

class RedisService:
    @staticmethod
    def get_client():
        try:
            password = connection.split('password=')[1].split(',')[0]
            host = connection.split(':')[0]
            port = int(connection.split(':')[1].split(',')[0])
            ssl = "ssl=True" in connection
            return redis.Redis(host=host, port=port, password=password, ssl=ssl, decode_responses=False)
        except Exception as e:
            logging.error(f"Erro ao conectar ao Redis: {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexão com Redis indisponível.")

    @staticmethod
    def set(key: str, value: bytes):
        client = RedisService.get_client()
        try:
            client.set(key, value)
            return True
        except Exception as e:
            logging.error(f"Erro ao definir valor no Redis: {e}")
            return False

    @staticmethod
    def get(key: str) -> bytes:
        client = RedisService.get_client()
        try:
            return client.get(key)
        except Exception as e:
            logging.error(f"Erro ao obter valor do Redis: {e}")
            return None

    @staticmethod
    def mget(keys: list[str]) -> list[bytes]:
        client = RedisService.get_client()
        try:
            return client.mget(keys)
        except Exception as e:
            logging.error(f"Erro ao obter valores do Redis com MGET: {e}")
            return []

    @staticmethod
    def get_all_keys(pattern: str) -> list[str]:
        client = RedisService.get_client()
        try:
            keys = [key.decode('utf-8') for key in client.scan_iter(pattern)]
            return keys
        except Exception as e:
            logging.error(f"Erro ao obter chaves do Redis: {e}")
            return []
        
    @staticmethod
    def incr(key: str) -> int:
        client = RedisService.get_client()
        try:
            return client.incr(key)
        except Exception as e:
            logging.error(f"Erro ao incrementar contador no Redis: {e}")
            return -1
