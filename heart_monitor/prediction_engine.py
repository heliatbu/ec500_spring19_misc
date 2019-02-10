import time
import random
import threading
from common_types import Message, MessageUrgency

'''
This class is responsible for updating its internal model and 
alerting the user if a worrisome prediction occurs
'''


class PredictionEngine(threading.Thread):
    def __init__(self, update_interval, notification_man, database):
        super().__init__()
        self._database = database
        self._notification_man = notification_man
        self._update_interval = update_interval
        self._predicted_pulse = 0
        self._predicted_oxy = 0
        self._predicted_diastolic = 0
        self._predicted_systolic = 0

    def run(self):
        '''
        Entry point for the thread library.
        In here we should update the model and send notifications (if any)
        :return: None
        '''
        while True:
            pulse_row = self._database.get_latest_pulse_data()
            heart_rate_row = self._database.get_latest_heart_rate_data()
            oxygen_row = self._database.get_latest_oxygen_data()
            self.update_model(
                pulse_row[0],
                oxygen_row[0],
                heart_rate_row[0],
                heart_rate_row[1]
            )
            if not self.patient_will_live():
                self._notification_man.send_message(
                    Message(
                        '<<WARNING>> AI Prediction indicates patient will be critical in the future!',
                        MessageUrgency.HIGH_URGENCY
                    )
                )
            time.sleep(self._update_interval)

    def update_model(self, pulse, oxy, diastolic, systolic):
        self._predicted_diastolic = pulse + random.randint(0, 20)
        self._predicted_systolic = systolic + random.randint(0, 15)
        self._predicted_diastolic = diastolic + random.randint(0, 15)
        self._predicted_oxy = oxy + random.randint(0, 10)

    def patient_will_live(self):
        return 60 <= self._predicted_pulse <= 100 and \
               90 <= self._predicted_systolic <= 120 \
               and 60 <= self._predicted_diastolic <= 80
