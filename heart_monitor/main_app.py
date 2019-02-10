import sensor_readers
import display
import prediction_engine
import notification_manager
import notifications_sender
import realtime_data_processor
from multiprocessing import Queue
from common_types import Contact


def main(cmd_args):
    '''
    Entry point of application; in here we spawn the sensor threads, AI thread and
    realtime data processing thread and then wait till we need to quit
    :param cmd_args: dictionary of expected command line arguments
    :return: 0 on success and non-zero on error
    '''
    data_proc_queue = Queue()
    tty = display.TextTerminalDisplay()
    notification_man = notification_manager.FlexibleNotificationManager(
        Contact('Nurse Suzy', None, None, None),
        notifications_sender.MockSMSSender(),
        notifications_sender.MockTelegramSender(),
        notifications_sender.MockEmailSender()
    )
    pulse_reader = sensor_readers.BloodPulseSensorReader(1, data_proc_queue, tty)
    oxy_reader = sensor_readers.BloodOxygenSensorReader(4, data_proc_queue, tty)
    pressure_reader = sensor_readers.BloodPressureSensorReader(2, data_proc_queue, tty)
    real_time_proc = realtime_data_processor.RealTimeDataProcessor(data_proc_queue, notification_man)
    pulse_reader.start()
    oxy_reader.start()
    pressure_reader.start()
    real_time_proc.start()
    oxy_reader.join()
    pressure_reader.join()
    pulse_reader.join()
    real_time_proc.join()
    return 0


if __name__ == '__main__':
    main(None)