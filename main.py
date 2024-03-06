

from simulation.simulation import Simulation


def main():
    # Initialize and run the simulation
    print("Starting Lyft Ride-Sharing Simulation...")

    # Configuration for the simulation
    months = 12  # Duration of the simulation in months
    initial_riders = 1000  # Number of initial riders in the system
    initial_drivers = 100  # Number of initial drivers in the system
    lyft_take_options = [3, 4, 5, 6]  # Different values of Lyft's take to test

    # Create and run the simulation
    simulation = Simulation(months=months, initial_riders=initial_riders, initial_drivers=initial_drivers,
                            lyft_take_options=lyft_take_options)
    simulation.run()
    simulation.plot_metrics()

    # Compile metrics to df
    metrics_df = simulation.compile_metrics_to_dataframe()

    # Save df to csv
    metrics_df.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()
