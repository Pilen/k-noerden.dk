
import os
import secrets

def init(config):
    import sys
    # config = sys.modules[__name__]
    from knoerden import default_config, local_config
    # from knoerden import local_config
    # default_config = object()
    # local_config = object()
    # default_config.DEBUG = True
    result = dict()
    for item in dir(default_config):
        if item.isupper():
            value = getattr(default_config, item)
            setattr(config, item, value)
            result[item] = value
    for item in dir(local_config):
        if item.isupper():
            if not hasattr(config, item):
                raise Exception(f"Could not overwrite {item}, not found in default config")
            value = getattr(local_config, item)
            setattr(config, item, value)
            result[item] = value
    config.SECRET_KEY = load_create_secret_key(config.SECRET_KEY_FILE, config.SECRET_KEY_LENGTH)
    result["SECRET_KEY"] = config.SECRET_KEY
    return result

def create_secret_key(filename, length):
    key = secrets.token_bytes(length)
    with open(filename, "wb") as file:
        file.write(key)
    return key

def load_create_secret_key(filename, length):
    if os.path.isfile(filename):
        with open(filename, "rb") as file:
            return file.read()
    else:
        return create_secret_key(filename, length)
