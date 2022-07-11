from os import getenv

PARAMS = {
    "FILE_SIZE_BATCH_TRIGGER": float(getenv("FILE_SIZE_BATCH_TRIGGER", 0)),
    "FREQUENCY_BATCH_TRIGGER": float(getenv("FREQUENCY_BATCH_TRIGGER", 0)),
    "FREQUENCY_TIME_UNIT": getenv("FREQUENCY_TIME_UNIT", "s")
}
