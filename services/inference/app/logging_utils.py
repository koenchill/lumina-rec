import json
import logging

logger = logging.getLogger("lumina-rec-inference")


def log_event(event_name: str, **fields) -> None:
    log_record = {"event": event_name, **fields}
    logger.info(json.dumps(log_record))
