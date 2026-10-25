from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000

    postgres_database_name: str = 'postgres'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_username: str = 'postgres'
    postgres_password: str = 'postgres'

    catalog_url: str = ''
    catalog_key: str = ''

    payment_url: str = ''
    payment_key: str = ''
    payment_callback_url: str = ''

    max_retries: int = 3

    kafka_bootstrap_servers: str = ''
    topic_out: str = 'student_system-order.events'

    @property
    def db_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_database_name}'
        )

    model_config = SettingsConfigDict(env_file='.env')


conf = Settings()
