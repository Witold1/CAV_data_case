# from collections import defaultdict
import numpy as np
import pandas as pd

def _prepare_testing_timelines(df_aux : pd.DataFrame, precision='s') -> np.array:
    '''

    We check every second of a day timelive to identify when every test was acive.
        When there is a test, we incriment a respective range in the timeline array.
        Casually, we calculate a maximum union for time lines all tests, reducing them to 24 hours cycle range

    For now we have one array for all tests, but with dummy scaling it is possible to have a dimension for every test

    Also, we might speed up second-wise slise using LineCollections, as here
    https://stackoverflow.com/questions/58648287/is-it-possible-to-speed-up-barh-plots-when-plotting-thousands-of-bars
    '''
    if precision == 's':
        interval_range = 24 * 60 * 60
    elif precision == 'm':
        interval_range = 24 * 60
    elif precision == 'h':
        interval_range = 24
    array_aux = np.zeros(shape=interval_range, dtype=np.uint16)

    for indx, (start_ts, test_length) in df_aux.iterrows():

        if precision == 's':
            start_ts_seconds = (start_ts.hour * 60 + start_ts.minute) * 60 + start_ts.second
            test_length_seconds = int(test_length / np.timedelta64(1, 's'))
        elif precision == 'm':
            start_ts_seconds = (start_ts.hour * 60 + start_ts.minute)
            test_length_seconds = int(test_length / np.timedelta64(1, 'm'))
        elif precision == 'h':
            start_ts_seconds = (start_ts.hour)
            test_length_seconds = int(test_length / np.timedelta64(1, 'h'))

        if start_ts_seconds + test_length_seconds > interval_range:
            days_diff = (start_ts_seconds + test_length_seconds) // interval_range
            next_day = (start_ts_seconds + test_length_seconds) % interval_range
            if days_diff >= 1:
                array_aux += days_diff - 1 # one day means not full cycle happend
                array_aux[start_ts_seconds : ] += 1
                array_aux[0 : next_day] += 1
        else:
            array_aux[start_ts_seconds : start_ts_seconds + test_length_seconds] += 1

    return array_aux, interval_range
