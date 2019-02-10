import datetime
import threading
from collections import defaultdict


class Database(object):

    def insert_pulse_data(self, pulse, timestamp):
        raise NotImplementedError

    def insert_oxygen_data(self, blood_oxy, timestamp):
        raise NotImplementedError

    def insert_heart_rate_data(self, diastolic, systolic, timestamp):
        raise NotImplementedError

    def get_latest_pulse_data(self):
        raise NotImplementedError

    def get_latest_heart_rate_data(self):
        raise NotImplementedError

    def get_latest_oxygen_data(self):
        raise NotImplementedError


class InMemorySimpleDatabase(Database):

    def __init__(self):
        self._pulse_pk = 0
        self._oxy_pk = 0
        self._heart_rate_pk = 0
        self._db_lock = threading.Lock()
        self._pulse_table = defaultdict(lambda: (0, datetime.datetime.now()))
        self._heart_rate_table = defaultdict(lambda: (0, 0, datetime.datetime.now()))
        self._oxygen_table = defaultdict(lambda: (0, datetime.datetime.now()))
        self._pulse_lock = threading.Lock()
        self._oxy_lock = threading.Lock()
        self._heart_rate_lock = threading.Lock()

    def insert_pulse_data(self, pulse, timestamp):
        self._pulse_lock.acquire(blocking=True)
        self._pulse_table[self._pulse_pk] = (pulse, timestamp)
        self._pulse_pk += 1
        self._pulse_lock.release()

    def insert_heart_rate_data(self, diastolic, systolic, timestamp):
        self._heart_rate_lock.acquire(blocking=True)
        self._heart_rate_table[self._heart_rate_pk] = (diastolic, systolic, timestamp)
        self._heart_rate_pk += 1
        self._heart_rate_lock.release()

    def insert_oxygen_data(self, blood_oxy, timestamp):
        self._oxy_lock.acquire(blocking=True)
        self._oxygen_table[self._oxy_pk] = (blood_oxy, timestamp)
        self._oxy_pk += 1
        self._oxy_lock.release()

    def get_latest_pulse_data(self):
        self._pulse_lock.acquire(blocking=True)
        data = self._pulse_table[self._pulse_pk - 1]
        self._pulse_lock.release()
        return data

    def get_latest_heart_rate_data(self):
        self._heart_rate_lock.acquire(blocking=True)
        data = self._heart_rate_table[self._heart_rate_pk - 1]
        self._heart_rate_lock.release()
        return data

    def get_latest_oxygen_data(self):
        self._oxy_lock.acquire(blocking=True)
        data = self._oxygen_table[self._oxy_pk - 1]
        self._oxy_lock.release()
        return data
