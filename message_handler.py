from logger import logger
from redis_config import get_redis_pool
import json
import time


async def handle_new_message(event):
    try:
        # 获取消息详情
        message_text = event.message.message
        user_id = event.message.from_id.user_id if event.message.from_id else None
        chat_id = event.chat_id
        message_id = event.message.id
        timestamp = int(time.time())
        
        # 构建消息数据结构
        message_data = {
            'message_text': message_text,
            'user_id': user_id,
            'chat_id': chat_id,
            'message_id': message_id,
            'timestamp': timestamp
        }
        
        # 连接Redis
        redis = await get_redis_pool()
        
        # 使用List存储消息
        # 键格式: messages:{chat_id}
        key = f"messages:{chat_id}"
        
        # 将消息数据转换为JSON字符串并存储
        await redis.lpush(key, json.dumps(message_data))
        
        # 设置消息过期时间（例如7天）
        await redis.expire(key, 60)
        
        logger.info(f"Stored message from chat {chat_id}: {message_text[:50]}...")
        
        await redis.close()
        
    except Exception as e:
        logger.exception(f"Error processing message: {e}")