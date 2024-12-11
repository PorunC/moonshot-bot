# message_handler.py
import re
from logger_config import setup_logger
from config import SOLANA_TOKEN_PATTERN

logger = setup_logger()

async def handle_new_message(event):
    try:
        message_text = event.message.message
        logger.info(f"原始消息: {message_text}")
        
        token_addresses = re.findall(SOLANA_TOKEN_PATTERN, message_text)
        
        if token_addresses:
            logger.info("发现 Solana token 地址:")
            for addr in token_addresses:
                logger.info(f"- {addr}")
        
    except Exception as e:
        logger.exception(f"Error processing message: {e}")