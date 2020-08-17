"""
Retrieves the data from the OS environment variables.
Environments variables are defined in the Dockerfile, and some of them have the default value.
If value is not found in environment variable, the configuration file (properties.ini) is used.
It is located in the resources directory.
If no value is specified in the properties file, the default will be used if the property supports it.
"""

import configparser
import os


def get_config():
    filename = "resources/properties.ini"
    config = configparser.RawConfigParser()
    config.read(filename)
    return config


def get_username():
    if "BANGGOOD_USERNAME" in os.environ:
        return os.environ.get("BANGGOOD_USERNAME")
    else:
        return get_config().get("CredentialsSection", "banggood.username")


def get_password():
    if "BANGGOOD_PASSWORD" in os.environ:
        return os.environ.get("BANGGOOD_PASSWORD")
    else:
        return get_config().get("CredentialsSection", "banggood.password")


def get_desired_country():
    if "BANGGOOD_SHIPTO" in os.environ:
        return os.environ.get("BANGGOOD_SHIPTO")
    else:
        country = get_config().get("ShipToSection", "banggood.shipto")
        if country is not None:
            return str(country)
        else:
            return "US"


def get_desired_currency():
    if "BANGGOOD_CURRENCY" in os.environ:
        return os.environ.get("BANGGOOD_CURRENCY")
    else:
        currency = get_config().get("ShipToSection", "banggood.currency")
        if currency is not None:
            return str(currency)
        else:
            return "USD"


def get_sleep_time():
    if "BROWSER_SLEEP" in os.environ:
        return os.environ.get("BROWSER_SLEEP")
    else:
        sleep_time = get_config().get("SleepSection", "browser.sleep.time")
        if sleep_time is not None and sleep_time.isnumeric:
            return int(sleep_time)
        else:
            return 2
