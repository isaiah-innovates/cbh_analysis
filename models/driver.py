class Driver:
    def __init__(self, id, monthly_rides=100, churn_rate=0.05):
        self.id = id
        self.monthly_rides = monthly_rides
        self.churn_rate = churn_rate
        self.earnings = 0

    def complete_ride(self, payment):
        # This method updates the driver's earnings for a completed ride
        self.earnings += payment
