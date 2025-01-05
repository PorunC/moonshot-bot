import re
import asyncio
from logger_config import setup_logger
from config import SOLANA_TOKEN_PATTERN
from jupiter_py.jupiter_py import buy, sell
from config import JUPITER_SOL_AMOUNT_IN, JUPITER_SLIPPAGE, JUPITER_SOL_AMOUNT_PER

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

            buy(token_addresses[0], JUPITER_SOL_AMOUNT_IN, JUPITER_SLIPPAGE)
            
            # # 创建延迟卖出任务
            # asyncio.create_task(delayed_sell(token_addresses[0]))
        
    except Exception as e:
        logger.exception(f"Error processing message: {e}")

# async def delayed_sell(token_address):
#     try:
#         await asyncio.sleep(120)
        
#         logger.info(f"开始卖出 token: {token_address}")
#         sell(token_address, JUPITER_SOL_AMOUNT_PER, JUPITER_SLIPPAGE)
        
#     except Exception as e:
#         logger.exception(f"Error in delayed sell: {e}")