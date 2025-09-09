import asyncio
import json
import logging

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
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )
    pubsub = redis.pubsub()
    await pubsub.subscribe(settings.REDIS_CHANNEL)
    logger.info(
        "Subscribed to '%s' at %s:%s",
        settings.REDIS_CHANNEL,
        settings.REDIS_HOST,
        settings.REDIS_PORT,
    )
    try:
        async for message in pubsub.listen():
            if message.get("type") != "message":
                continue
            data = message.get("data")
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                logger.error("Event parse error, raw=%s", data)
                continue

            logger.info(
                "[%s] id=%s title=%s",
                payload.get("event"),
                payload.get("id"),
                payload.get("title"),
            )
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe(settings.REDIS_CHANNEL)
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
