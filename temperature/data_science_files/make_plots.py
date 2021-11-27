"""
create plots using Temperature class
"""
is_jupyter = True
if __name__ == '__main__' or is_jupyter:
        from temperature import Temperature
else:
        from temperature.data_science_files.temperature import Temperature
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (18, 8)
plt.rcParams['legend.fontsize'] = 30
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['axes.titlesize'] = 30
class Plots(Temperature):
    def plot_temperatures(self, show_plot):
            """
            Plot temperatures for the given locations
            param show_plot: logical. Should the plot be shown?
            """
            self.get_temperature_data().plot(linewidth=4)
            plt.ylabel("Temperature (degC)",
                    fontweight="bold")
            plt.xlabel("",
                    fontweight="bold")
            plt.title(f"Temperature forecasts on {self.date_of_request} ",
                    fontweight="bold",
                    fontsize=30)
            if show_plot:
                plt.show()
    def append_warnings_onto_plot(self, show_plot):
        """
        Put warnings on plot
        show_plot: Logical. Should the plots be shown?
        """
        self.plot_temperatures(show_plot=False)
        invalid_locations = self.identify_valid_and_invalid_locations()["invalid_locations"]
        i = 0.45
        j = 0.35
        if invalid_locations != []:
            plt.figtext(i, j, "Warning: The following locations are unknown:", fontsize=14)
            for index, location in enumerate(invalid_locations):
                plt.figtext(i+0.03, j-0.03, f'{index + 1}. {location.title()}', fontsize=14)
                j -= 0.03
        if show_plot:
            plt.show()
if __name__ == "__main__":
        LOCATION_FILE = "temperature/data_science_files/data/worldcities.csv"
        REQUESTED_LOCATION = ["Leipzig", "Berlin", "Stuttgart", "Tokyo", "Beijing"]
        DATE_OF_REQUEST = "2021-10-25"
        OBJ = Plots(LOCATION_FILE, REQUESTED_LOCATION, DATE_OF_REQUEST)
        print(OBJ.append_warnings_onto_plot(True))