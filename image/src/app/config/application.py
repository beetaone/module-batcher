"""
All constants specific to the application
"""
from app.utils.env import env
from app.utils.floatenv import floatenv


APPLICATION = {
    "FILE_SIZE_BATCH_TRIGGER": floatenv("FILE_SIZE_BATCH_TRIGGER"),
    "FREQUENCY_BATCH_TRIGGER": floatenv("FREQUENCY_BATCH_TRIGGER"),
    "FREQUENCY_TIME_UNIT": env("FREQUENCY_TIME_UNIT", "s")
}
