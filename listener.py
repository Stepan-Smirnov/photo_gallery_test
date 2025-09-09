import asyncio
import json
import logging

from redis.asyncio import Redis

logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:S",
    format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-8s - %(message)s",
    handlers=[logging.StreamHandler()],
    force=True,
)

logger = logging.getLogger(__name__)


async def main() -> None:
    redis = Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )
    pubsub = redis.pubsub()
    await pubsub.subscribe("image_channel")
    logger.info("Subscribed to 'image_channel'")
    try:
        async for message in pubsub.listen():
            if message.get("type") != "message":
                continue
            data = message.get("data")
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                logger.error("Parse error")
                continue

            logger.info(payload)
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe("image_channel")
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
