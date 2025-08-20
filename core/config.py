from pydantic_settings import BaseSettings, SettingsConfigDict
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

class Settings(BaseSettings):
    redis_connection_string: str = ""
    embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
    log_level: str = "INFO"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_redis_connection_string()

    def load_redis_connection_string(self):
        try:
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url="https://kv-querymind-qa.vault.azure.net/", credential=credential)
            secret = secret_client.get_secret("RedisConnectionStrings--DefaultConnection")
            self.redis_connection_string = secret.value
        except Exception as e:
            print(f"Erro ao buscar o segredo do Key Vault: {e}")
            self.redis_connection_string = os.getenv("REDIS_CONNECTION_STRING", "")
            if not self.redis_connection_string:
                raise ValueError("A string de conexão do Redis não foi encontrada no Key Vault ou nas variáveis de ambiente.")

settings = Settings()