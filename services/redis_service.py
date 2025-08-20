import logging
import redis

redis_connection_string = "xyz"

class RedisService:
    @staticmethod
    def get_client():
        return redis.Redis.from_url(
            f"rediss://:{redis_connection_string.split('password=')[1].split(',')[0]}@{redis_connection_string.split(':')[0]}:6380",
            decode_responses=False
        )

    @staticmethod
    def set(key: str, value: bytes):
        client = RedisService.get_client()
        try:
            client.set(key, value)
            return True
        except Exception as e:
            return False

    @staticmethod
    def get(key: str) -> bytes:
        client = RedisService.get_client()
        try:
            return client.get(key)
        except Exception as e:
            return None

    @staticmethod
    def get_all_keys(pattern: str) -> list[str]:
        client = RedisService.get_client()
        try:
            keys = [key.decode('utf-8') for key in client.keys(pattern)]
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