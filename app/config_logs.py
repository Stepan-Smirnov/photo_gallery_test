import logging


def config_logs(level: str = logging.INFO):
    """Config logs"""

    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-8s - %(message)s",
        handlers=[logging.StreamHandler()],
        force=True
    )