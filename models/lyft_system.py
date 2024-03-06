import random


class LyftSystem:
    def __init__(self, initial_driver_pay=19, lyft_take=6, match_rate_target=0.93):
        self.initial_driver_pay = initial_driver_pay
        self.lyft_take = lyft_take
        self.drivers = []
        self.riders = []
        self.match_rate_target = match_rate_target
        self.failed_matches = 0
        self.successful_matches = 0
        self.total_rides_requested = 0

    def add_driver(self, driver):
        self.drivers.append(driver)

    def add_rider(self, rider):
        self.riders.append(rider)

    def request_ride(self, rider):
        self.total_rides_requested += 1
        if random.random() < self.calculate_current_match_rate():
            self.successful_matches += 1
            rider.update_failed_to_find_driver(False)
            self.process_ride_payment()
        else:
            self.failed_matches += 1
            rider.update_failed_to_find_driver(True)
            self.update_rider_churn(rider)

    def process_ride_payment(self):
        # In a real system, we'd select a specific driver, but here we simplify.
        payment_to_driver = self.initial_driver_pay - self.lyft_take
        random.choice(self.drivers).complete_ride(payment_to_driver)

    def calculate_current_match_rate(self):
        # This method calculates the current match rate based on Lyft's take adjustments
        # For simplification, we're assuming a direct correlation between Lyft's take and match rate
        match_rate_increase = (6 - self.lyft_take) / 3 * 0.33  # Simplified model of impact
        return min(1, 0.6 + match_rate_increase)  # Ensure match rate doesn't exceed 100%

    def update_rider_churn(self, rider):
        # Increase churn rate for riders who fail to find a driver
        if rider.failed_to_find_driver:
            rider.churn_rate = 0.33
        else:
            rider.churn_rate = 0.1

    def adjust_lyft_take(self, new_take):
        self.lyft_take = new_take

    def run_month(self):
        # Simulate a month of operations
        for rider in self.riders:
            rider.request_ride()
            self.request_ride(rider)
        self.remove_churned_agents()

    def remove_churned_agents(self):
        # Remove churned riders and drivers
        self.riders = [rider for rider in self.riders if not rider.failed_to_find_driver or random.random() > 0.33]
        self.drivers = [driver for driver in self.drivers if random.random() > driver.churn_rate]

    def report_metrics(self):
        # Calculate metrics
        total_rides_requested = self.total_rides_requested
        successful_matches = self.successful_matches
        failed_matches = self.failed_matches
        current_match_rate = self.successful_matches / self.total_rides_requested if self.total_rides_requested > 0 else 0

        # Return metrics as a dictionary
        return {
            'Total Rides Requested': total_rides_requested,
            'Successful Matches': successful_matches,
            'Failed Matches': failed_matches,
            'Current Match Rate': current_match_rate,
            'Current Driver Count': len(self.drivers),
            'Current Rider Count': len(self.riders),
        }