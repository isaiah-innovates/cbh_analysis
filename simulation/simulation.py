from models.lyft_system import LyftSystem
from models.rider import Rider
from models.driver import Driver
import matplotlib.pyplot as plt
import pandas as pd


class Simulation:
    def __init__(self, months=12, initial_riders=1000, initial_drivers=100, lyft_take_options=[3, 4, 5, 6]):
        self.months = months
        self.initial_riders = initial_riders
        self.initial_drivers = initial_drivers
        self.lyft_take_options = lyft_take_options
        self.results = {}
        self.detailed_metrics = {} # to store metrics for data viz

    def setup_environment(self):
        self.lyft_system = LyftSystem()
        for _ in range(self.initial_drivers):
            new_driver = Driver(id=_)
            self.lyft_system.add_driver(new_driver)
        for _ in range(self.initial_riders):
            new_rider = Rider(id=_)
            self.lyft_system.add_rider(new_rider)

    def run_simulation(self):
        for lyft_take in self.lyft_take_options:
            
            print(f"\nRunning simulation with Lyft's take: ${lyft_take}")
            
            # Reset environment for each simulation run
            self.setup_environment()
            self.lyft_system.adjust_lyft_take(lyft_take)
            monthly_metrics = []
            for month in range(self.months):
                self.lyft_system.run_month()
            
                 # Print metrics after each month
                metrics = self.lyft_system.report_metrics()
                monthly_metrics.append(metrics)
                print(f"Month {month+1} Metrics:")
                print(f"Total Rides Requested: {metrics['Total Rides Requested']}")
                print(f"Successful Matches: {metrics['Successful Matches']}")
                print(f"Failed Matches: {metrics['Failed Matches']}")
                print(f"Current Match Rate: {metrics['Current Match Rate']:.2%}")
                print(f"Current Driver Count: {metrics['Current Driver Count']}")
                print(f"Current Rider Count: {metrics['Current Rider Count']}")

            self.detailed_metrics[lyft_take] = monthly_metrics          
            # Store the final month's metrics for analysis
            self.results[lyft_take] = self.lyft_system.report_metrics()

    def analyze_results(self):
        
        # Analyze the results to find the optimal Lyft's take
        max_net_revenue = 0
        optimal_take = 0
        for take, metrics in self.results.items():
            if metrics: #Check if metrics is not None
                net_revenue = (25 - take) * metrics['Successful Matches'] # Ensure this key matches the returned dictionary
                if net_revenue > max_net_revenue:
                    max_net_revenue = net_revenue
                    optimal_take = take
        print(f'Optimal Lyft Take: ${optimal_take}, Max Net Revenue: ${max_net_revenue}')

    def run(self):
        self.run_simulation()
        self.analyze_results()

    def compile_metrics_to_dataframe(self):
        # Create a list to hold all rows before converting to DataFrame
        all_metrics = []
        
        for take, monthly_metrics in self.detailed_metrics.items():
            for month, metrics in enumerate(monthly_metrics, start=1):
                metrics_row = {
                    'Lyft Take': take,
                    'Month': month,
                    **metrics  # This unpacks all key-value pairs from the metrics dict directly into the row
                }
                all_metrics.append(metrics_row)
        
        # Convert the list of dictionaries to a DataFrame
        metrics_df = pd.DataFrame(all_metrics)
        return metrics_df


    def plot_metrics(self):
        fig, axs = plt.subplots(2, 1, figsize=(10, 10))

        for take, metrics in self.detailed_metrics.items():
            months = range(1, len(metrics) +1)
            match_rates = [m['Current Match Rate'] for m in metrics]
            successful_matches = [m['Successful Matches'] for m in metrics]
            net_revenues = [(25 - take) * m for m in successful_matches]

            axs[0].plot(months, match_rates, label = f'Lyft Take ${take}')
            axs[1].plot(months, net_revenues, label = f'Lyft Take ${take}')

        axs[0].set_title('Match Rate Over Time')
        axs[0].set_xlabel('Month')
        axs[0].set_ylabel('Match Rate')
        axs[0].legend()

        axs[1].set_title('Net Revenue Over Time')
        axs[1].set_xlabel('Month')
        axs[1].set_ylabel('Net Revenue ($)')
        axs[1].legend()

        plt.tight_layout()
        plt.show()
