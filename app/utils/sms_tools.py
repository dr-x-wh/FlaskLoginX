from app.extensions import logger


def send_sms(phone: str, text: str) -> bool:
    logger.info(f"send sms: {phone} and {text}")
    return True
