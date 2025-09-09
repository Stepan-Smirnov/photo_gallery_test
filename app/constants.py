MAX_IMAGE_SIZE = 10 * 1024 * 1024
IMAGE_EXTENSIONS = [
    "image/jpeg",
    "image/png",
]
ONE_CHUNK = MAX_IMAGE_SIZE // 10
REDIS_CHANNEL = "image_channel"
REDIS_KEY_PREFIX = "image:"
REDIS_KEY_EXPIRE = 60
