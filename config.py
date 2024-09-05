from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user_login: str
    user_password: str
    admin_login: str
    admin_password: str
    api_login: str
    api_password: str

    monday: int = 9
    tuesday: int = 10
    wednesday: int = 14
    thursday: int = 12
    friday: int = 19
    saturday: int = 20
    sunday: int = 16

    def get_percent(self, weekday: int) -> float:
        week_dict = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }
        return week_dict[weekday] / 100

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
