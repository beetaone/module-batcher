"""
All logic related to the module's main application
Mostly only this file requires changes
"""

from flask import Flask
from app.config import APPLICATION
from app.weeve.egress import send_data
import threading
import sys

__INTERVAL_PERIOD__ = APPLICATION['FREQUENCY_BATCH_TRIGGER']
__INTERVAL_UNIT__ = APPLICATION['FREQUENCY_TIME_UNIT']
__FILE_SIZE__ = APPLICATION['FILE_SIZE_BATCH_TRIGGER'] * 1000      # (* 1000) because of converting kilobyte (kb) unit to bytes (b)

# data collector
data = []

app = None

def set_module_app(appi: Flask):
    global app
    app = appi

def frequency_processing():
    '''
    For the case with frequency processing
    Sets an interval for receiving data and processes them.
    Sends data to the next module.
    '''
    # convert interval unit to seconds (must do for threading Timer)
    convert_interval_unit = {
        'ms': __INTERVAL_PERIOD__/1000,
        's': __INTERVAL_PERIOD__,
        'm': __INTERVAL_PERIOD__ * 60,
        'h': __INTERVAL_PERIOD__ * 3600,
        'd': __INTERVAL_PERIOD__ * 3600 * 24,
    }
    interval = convert_interval_unit[__INTERVAL_UNIT__]

    # start thread with given interval
    threading.Timer(interval, frequency_processing).start()

    # save number of data to process, because new data might arrive when processing
    count = len(data)

    if count != 0:
        # send data
        sent = send_data(data[:count])
        if not sent:
            app.logger.error("Error while transfering")

        # remove old data
        del data[:count]


def module_main(parsed_data):
    """implement module logic here

    Args:
        parsed_data ([JSON Object]): [The output of data_validation function]

    Returns:
        [string, string]: [data, error]
    """

    global data

    try:
        if type(parsed_data) == dict:
            data.append(parsed_data)
        else:
            data = data + parsed_data
        
        # case for file size processing
        if __FILE_SIZE__ != 0.0 and sys.getsizeof(data) > __FILE_SIZE__:
            return_data = data[:-1]
            # delete old data
            del data[:-1]

            return return_data, None

        return None, None
    except Exception:
        return None, "Unable to perform the module logic"
