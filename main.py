# main.py
from telethon import TelegramClient, events
import asyncio
from config import TELEGRAM_CONFIG, TARGET_GROUPS
from logger_config import setup_logger
from message_handler import handle_new_message
from connection_manager import maintain_connection, initialize_client

logger = setup_logger()

# 创建客户端
tgClient = TelegramClient(
    TELEGRAM_CONFIG['session_name'],
    TELEGRAM_CONFIG['api_id'],
    TELEGRAM_CONFIG['api_hash'],
    proxy=TELEGRAM_CONFIG['proxy'],
    receive_updates=True,
    auto_reconnect=True
)

# 注册消息处理器
tgClient.on(events.NewMessage(chats=TARGET_GROUPS))(handle_new_message)

async def run():
    if await initialize_client(tgClient):
        logger.info("开始监听消息...")
        connection_task = asyncio.create_task(maintain_connection(tgClient))
        try:
            await tgClient.run_until_disconnected()
        finally:
            connection_task.cancel()

if __name__ == "__main__":
    try:
        tgClient.loop.run_until_complete(run())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.exception(f"发生未知错误: {e}")
    finally:
        if tgClient.is_connected():
            tgClient.disconnect()
        logger.info("程序已退出")