"""
Retrieves the data from the configuration file (properties.ini) located in the resources directory.
Some data is just read from the file and returned, and some has default values. If no value is specified in the
properties file, the default will be used.
"""

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


def get_desired_country():
    country = get_config().get("ShipToSection", "banggood.shipto")
    if country is not None:
        return str(country)
    else:
        return "US"


def get_desired_currency():
    currency = get_config().get("ShipToSection", "banggood.currency")
    if currency is not None:
        return str(currency)
    else:
        return "USD"


def get_sleep_time():
    sleep_time = get_config().get("SleepSection", "browser.sleep.time")
    if sleep_time is not None and sleep_time.isnumeric:
        return int(sleep_time)
    else:
        return 2
