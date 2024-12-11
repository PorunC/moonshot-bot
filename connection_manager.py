# connection_manager.py
import asyncio
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import AuthKeyUnregisteredError
from telethon.tl.functions.updates import GetStateRequest
from logger_config import setup_logger

logger = setup_logger()

async def maintain_connection(client):
    """保持连接并定期检查更新状态"""
    while True:
        try:
            if client.is_connected():
                await client(GetStateRequest())
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"Connection check error: {e}")
            await asyncio.sleep(5)

async def initialize_client(client):
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            logger.info(f"尝试连接... (尝试 {attempt + 1}/{max_attempts})")
            
            if not client.is_connected():
                await client.connect()
            
            if not await client.is_user_authorized():
                logger.info("需要登录...")
                phone = input("请输入你的手机号 (格式: +86xxxxxxxxxx): ")
                await client.send_code_request(phone)
                code = input("请输入收到的验证码: ")
                try:
                    await client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    password = input("请输入你的两步验证密码: ")
                    await client.sign_in(password=password)
            
            logger.info("连接成功!")
            return True
            
        except AuthKeyUnregisteredError:
            logger.error("认证密钥无效，请删除session文件重试")
            return False
            
        except Exception as e:
            attempt += 1
            logger.error(f"连接失败: {str(e)}")
            if attempt < max_attempts:
                wait_time = attempt * 5
                logger.info(f"等待 {wait_time} 秒后重试...")
                await asyncio.sleep(wait_time)
            else:
                logger.error("达到最大重试次数，退出程序")
                return False