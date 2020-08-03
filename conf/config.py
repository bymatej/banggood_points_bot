import configparser


class Config:

    @classmethod
    def get_config(cls):
        filename = "resources/properties.ini"
        config = configparser.RawConfigParser()
        config.read(filename)
        return config

    @classmethod
    def get_username(cls):
        return cls.get_config().get("CredentialsSection", "banggood.username")

    @classmethod
    def get_password(cls):
        return cls.get_config().get("CredentialsSection", "banggood.password")

    @classmethod
    def get_desired_country(cls):
        country = cls.get_config().get("ShipToSection", "banggood.shipto")
        if country is not None:
            return str(country)
        else:
            return "US"

    @classmethod
    def get_desired_currency(cls):
        currency = cls.get_config().get("ShipToSection", "banggood.currency")
        if currency is not None:
            return str(currency)
        else:
            return "USD"

    @classmethod
    def get_sleep_time(cls):
        sleep_time = cls.get_config().get("SleepSection", "browser.sleep.time")
        if sleep_time is not None and sleep_time.isnumeric:
            return int(sleep_time)
        else:
            return 2
