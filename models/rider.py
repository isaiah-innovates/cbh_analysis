class Rider:
    def __init__(self, id):
        self.id = id
        self.failed_to_find_driver = False

    def request_ride(self):
        # This method will be called when a rider requests a ride
        # The actual logic of finding a driver will be handled by the LyftSystem class
        pass

    def update_failed_to_find_driver(self, failed):
        self.failed_to_find_driver = failed
