
from pydantic_settings import BaseSettings, SettingsConfigDict

#BaseSettings allows you validate your env 
# Not case-sensetive but Settings class has to match your .env variable

class Settings(BaseSettings):
    database_type:str
    database_driver:str
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minute:int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
settings= Settings()    