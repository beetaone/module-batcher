"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from .params import PARAMS
from api.send_data import send_data

import threading
import sys

log = getLogger("module")

__INTERVAL_PERIOD__ = PARAMS['FREQUENCY_BATCH_TRIGGER']
__INTERVAL_UNIT__ = PARAMS['FREQUENCY_TIME_UNIT']
__FILE_SIZE__ = PARAMS['FILE_SIZE_BATCH_TRIGGER'] * 1000      # (* 1000) because of converting kilobyte (kb) unit to bytes (b)

# data collector
data = []

def frequency_processing():
    '''
    For the case with frequency processing.
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
        send_error = send_data(data[:count])
        if send_error:
            log.error("Error while transferring data.")

        # remove old data
        del data[:count]


def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    global data

    try:
        # YOUR CODE HERE

        if type(received_data) == dict:
            data.append(received_data)
        else:
            data = data + received_data

        # case for file size processing
        if __FILE_SIZE__ != 0.0 and sys.getsizeof(data) > __FILE_SIZE__:
            return_data = data[:-1]
            # delete old data
            del data[:-1]

            return return_data, None

        return None, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"
