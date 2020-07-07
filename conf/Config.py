import configparser


def get_config():
    filename = "resources/properties.ini"
    config = configparser.RawConfigParser()
    config.read(filename)
    return config


def get_username():
    return get_config().get("CredentialsSection", "banggood.username")


def get_password():
    return get_config().get("CredentialsSection", "banggood.password")


def get_sleep_time():
    return int(get_config().get("SleepSection", "browser.sleep.time"))
