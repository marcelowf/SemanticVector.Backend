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
