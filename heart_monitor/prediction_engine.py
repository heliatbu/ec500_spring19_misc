import threading
import time
import random
from common_types import Message, MessageUrgency
'''
He Li's version
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
        self.update_setting()
        while True:
            pulse_row = self._database.get_latest_pulse_data()
            heart_rate_row = self._database.get_latest_heart_rate_data()
            oxygen_row = self._database.get_latest_oxygen_data()
            self.predict(pulse_row[0], oxygen_row[0], heart_rate_row[0], heart_rate_row[1])
            if not self.patient_condition():
                '''
                Only when two numbers are abnormal, AI will send alert
                '''
                if self.urgency >= 2:
                    self._notification_man.send_message(
                        Message(
                            'Prediction indicates patient will be in bad condition',
                            MessageUrgency.HIGH_URGENCY
                        )
                    )
            time.sleep(self._update_interval)

    '''
    Allow doctor to set personalized healthy range
    '''
    def update_setting(self, pulse_low=60, pulse_high=100, oxy_low=50, diastolic_low=60, diastolic_high=80, systolic_low=90, systolic_high=120):
        self.PULSE_LOW = pulse_low
        self.PULSE_HIGH = pulse_high
        self.OXYGEN_LOW = oxy_low
        self.DIASTOLIC_LOW = diastolic_low
        self.DIASTOLIC_HIGH = diastolic_high
        self.SYSTOLIC_LOW = systolic_low
        self.SYSTOLIC_HIGH = systolic_high


    def predict(self, pulse, oxy, diastolic, systolic):
        self._predicted_diastolic = pulse + random.randint(-10, 10)
        self._predicted_systolic = systolic + random.randint(-10, 10)
        self._predicted_diastolic = diastolic + random.randint(-10, 10)
        '''
        Highest oxygen is 100%
        '''
        self._predicted_oxy = min(oxy + random.randint(0, 5), 100)

    def patient_condition(self):
        self.count = 0
        self.urgency = 0
        if not self.PULSE_LOW <= self._predicted_pulse <= self.PULSE_HIGH:
            self.count = self.count + 1
        if not self.DIASTOLIC_LOW <= self._predicted_diastolic <= self.DIASTOLIC_HIGH:
            self.count = self.count + 1
        if not self.SYSTOLIC_LOW <= self._predicted_systolic <= self.SYSTOLIC_HIGH:
            self.count = self.count + 1

        if self.count == 0:
            return True
        elif self.count == 1:
            self.urgency = 1
            return False
        else:
            self.urgency = 2
            return False