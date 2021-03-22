from typing import Optional, Tuple

from operations.utils import load_config, update_config


def base_commission(commission: float) -> Tuple[Optional[str], Optional[str]]:
    """
    Replace the default commmission with the new specified commission.

    :param commission: New commission
    :return: Success or error messages
    """
    config = load_config()
    config['base_commission'] = commission

    try:
        update_config(config=config)
    except Exception as e:
        error_msg = f'The following error has been occurred: {e}'

        return None, error_msg

    success_msg = 'Configuration has been updated'

    return success_msg, None
