from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Gate Controller Type: http, serial, gpio, mock
    GATE_CONTROLLER_TYPE: str = "mock"

    # HTTP Relay Settings
    GATE_CONTROLLER_HOST: str = "192.168.1.50"
    GATE_CONTROLLER_PORT: int = 80

    # Serial Relay Settings
    GATE_CONTROLLER_SERIAL_PORT: str = "COM3"
    GATE_CONTROLLER_BAUD_RATE: int = 9600

    # Gate Settings
    GATE_OPEN_DURATION: int = 5  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
