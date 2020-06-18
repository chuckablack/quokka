import threading

from quokka.controller.DeviceMonitorTask import DeviceMonitorTask
from quokka.controller.ComplianceMonitorTask import ComplianceMonitorTask
from quokka.controller.HostMonitorTask import HostMonitorTask
from quokka.controller.ServiceMonitorTask import ServiceMonitorTask
from quokka.controller.DiscoverTask import DiscoverTask


class ThreadManager:

    device_monitor_task = None
    device_monitor_thread = None
    compliance_monitor_task = None
    compliance_monitor_thread = None
    host_monitor_task = None
    host_monitor_thread = None
    service_monitor_task = None
    service_monitor_thread = None
    discovery_task = None
    discovery_thread = None

    @staticmethod
    def stop_device_threads():

        print("--- ---> Shutting down device monitoring threads (device and compliance)")

        if ThreadManager.device_monitor_task and ThreadManager.device_monitor_thread:
            ThreadManager.device_monitor_task.set_terminate()
            ThreadManager.device_monitor_thread.join()
        if ThreadManager.compliance_monitor_task and ThreadManager.compliance_monitor_thread:
            ThreadManager.compliance_monitor_task.set_terminate()
            ThreadManager.compliance_monitor_thread.join()

        ThreadManager.device_monitor_task = None
        ThreadManager.device_monitor_thread = None
        ThreadManager.compliance_monitor_task = None
        ThreadManager.compliance_monitor_thread = None

    @staticmethod
    def start_device_threads():

        ThreadManager.device_monitor_task = DeviceMonitorTask()
        ThreadManager.device_monitor_thread = threading.Thread(target=ThreadManager.device_monitor_task.monitor,
                                                               args=(60,))
        ThreadManager.device_monitor_thread.start()

        ThreadManager.compliance_monitor_task = ComplianceMonitorTask()
        ThreadManager.compliance_monitor_thread = threading.Thread(target=ThreadManager.compliance_monitor_task.monitor,
                                                                   args=(60,))
        ThreadManager.compliance_monitor_thread.start()

    @staticmethod
    def stop_host_thread():

        print("--- ---> Shutting down host monitoring thread")

        if ThreadManager.host_monitor_task and ThreadManager.host_monitor_thread:
            ThreadManager.host_monitor_task.set_terminate()
            ThreadManager.host_monitor_thread.join()

        ThreadManager.host_monitor_task = None
        ThreadManager.host_monitor_thread = None

    @staticmethod
    def start_host_thread():

        ThreadManager.host_monitor_task = HostMonitorTask()
        ThreadManager.host_monitor_thread = threading.Thread(target=ThreadManager.host_monitor_task.monitor,
                                                             args=(60,))
        ThreadManager.host_monitor_thread.start()

    @staticmethod
    def stop_service_thread():

        print("--- ---> Shutting down service monitoring thread")

        if ThreadManager.service_monitor_task and ThreadManager.service_monitor_thread:
            ThreadManager.service_monitor_task.set_terminate()
            ThreadManager.service_monitor_thread.join()

        ThreadManager.service_monitor_task = None
        ThreadManager.service_monitor_thread = None

    @staticmethod
    def start_service_thread():

        ThreadManager.service_monitor_task = ServiceMonitorTask()
        ThreadManager.service_monitor_thread = threading.Thread(target=ThreadManager.service_monitor_task.monitor,
                                                                args=(60,))
        ThreadManager.service_monitor_thread.start()

    @staticmethod
    def stop_discovery_thread():

        print("--- ---> Shutting down discovery monitoring thread")

        if ThreadManager.discovery_task and ThreadManager.discovery_thread:
            ThreadManager.discovery_task.set_terminate()
            ThreadManager.discovery_thread.join()

        ThreadManager.discovery_task = None
        ThreadManager.discovery_thread = None

    @staticmethod
    def start_discovery_thread():

        ThreadManager.discovery_task = DiscoverTask()
        ThreadManager.discovery_thread = threading.Thread(target=ThreadManager.discovery_task.discover,
                                                          args=(60,))
        ThreadManager.discovery_thread.start()
