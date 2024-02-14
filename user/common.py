
#emall/user/common.py
import logging

logger = logging.getLogger(__name__)

def err_msg(error_data):
    try:
        formatted_errors = str(error_data)
        return formatted_errors
    except Exception as e:
        logger.error(e)
        return "Unknown Error"