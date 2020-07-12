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
    sleep_time = get_config().get("SleepSection", "browser.sleep.time")
    if sleep_time is not None and sleep_time.isnumeric:
        return int(sleep_time)
    else:
        return 2
