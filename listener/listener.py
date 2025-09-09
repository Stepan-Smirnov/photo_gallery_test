import asyncio
import json

from redis.asyncio import Redis
from listener.config import settings

logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-8s - %(message)s",
        handlers=[logging.StreamHandler()],
        force=True,
    )

logger = logging.getLogger("listener")


async def main() -> None:
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe(settings.REDIS_CHANNEL)
    logger.info(f"Subscribed to '{settings.REDIS_CHANNEL}")
    try:
        async for message in pubsub.listen():
            if message.get("type") != "message":
                continue
            data = message.get("data")
            try:
                payload = json.loads(data)
            except Exception:
                logger.error(f"Event: raw={data}")
                continue

            logger.info(payload)
    except asyncio.CancelledError:
        pass
    finally:
        try:
            await pubsub.unsubscribe(REDIS_CHANNEL)
        finally:
            await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
