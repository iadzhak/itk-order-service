from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000

    postgres_database_name: str = 'postgres'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_username: str = 'postgres'
    postgres_password: str = 'postgres'

    @property
    def db_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_database_name}'
        )


conf = Settings()
