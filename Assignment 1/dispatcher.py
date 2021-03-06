from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        self.waiting_list = []
        self.driver_registry = []

        pass

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        return "Driver Registry:{}\nWaiting List:{}\n".format(
                self.driver_registry, self.waiting_list)
        pass

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """
        if len(self.driver_registry) == 0:
            self.waiting_list.append(rider)
            return None
        else:
            fastest_driver = None
            fastest_time = 0

            for driver in self.driver_registry:
                if driver.is_idle:
                    if fastest_driver is None:
                        fastest_driver = driver
                        fastest_time = driver.get_travel_time(rider.origin)
                    else:
                        travel_time = driver.get_travel_time(rider.origin)
                        if travel_time < fastest_time:
                            fastest_driver = driver
                            fastest_time = travel_time

            if fastest_driver is None:
                self.waiting_list.append(rider)
            return fastest_driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """
        if driver not in self.driver_registry:
            self.driver_registry.append(driver)

        if len(self.waiting_list) == 0:
            return None
        else:
            return self.waiting_list.pop(0)

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        if rider in self.waiting_list:
            self.waiting_list.remove(rider)
