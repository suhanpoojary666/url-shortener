import os
import redis
from dotenv import load_dotenv

load_dotenv()

#write all the redis code here

redis_client=redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)