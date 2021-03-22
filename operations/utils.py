import json
from typing import Any, Dict

import pymongo
from google_currency import convert


def load_config(config_path: str = 'config.json') -> Dict[str, Any]:
    """
    Load the configuration file.

    :param config_path: Path to the configuration file
    :return: Configuration object
    """
    try:
        with open(config_path) as cf:
            config = json.load(cf)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    return config


def update_config(config: Dict[str, Any], config_path: str = 'config.json'):
    """
    Update the configuration file.

    :param config_path: Path to the configuration file
    """
    with open(config_path, 'w') as cf:
        json.dump(config, cf)


def init_mongo_client() -> pymongo.MongoClient:
    """
    Initialize a mongo client.

    :return: Mongo client
    """
    config = load_config()
    db_config = config['db']
    address = db_config['address']
    username = db_config['username']
    password = db_config['password']
    client = pymongo.MongoClient(address, username=username, password=password)

    return client


def convert_money(origin_currency: str, target_currency: str,
                  amount: float) -> float:
    """
    Convert a certain amount of money from one currency to another.

    :param origin_currency: Origin currency
    :param target_currency: Target currency
    :param amount: Amount of money to convert
    :return: Converted amount
    """
    result = convert(origin_currency.upper(), target_currency.upper(), amount)
    result = json.loads(result)
    succeed = result.get('converted', False)

    # Check if the conversion completed successfully and return the converted
    # amount, otherwise return zero.
    if not succeed:
        return 0

    converted_amount = float(result.get('amount', 0))

    return converted_amount


def init_db():
    """
    Initialize a database.
    """
    config = load_config()
    db_config = config['db']
    do_init = db_config['init_db']

    if do_init:
        client = init_mongo_client()
        db = client['xchange']
        db.create_collection('loans')
        config['db']['init_db'] = False
        update_config(config=config)
        client.close()
