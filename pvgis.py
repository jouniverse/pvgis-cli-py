from grid_connected import *
from tracking_pv import *
from off_grid import *
from monthly_radiation import *
from daily_radiation import *
from hourly_radiation import *
from tmy import *
from horizon_profile import *
from api_call import create_output_directory


# Main menu
def main_menu():

    while True:
        # print the menu
        print("=============")
        print("PVGIS API APP")
        print("=============")
        print("1.  Grid-connected PV")
        print("2.  Tracking PV")
        print("3.  Off-grid PV")
        print("4.  Monthly radiation")
        print("5.  Daily radiation")
        print("6.  Hourly radiation")
        print("7.  TMY")
        print("8.  Horizon profile")
        # exit
        print("Q.  Quit")
        print("=============")
        print("Please enter the number of the item you want to select: ")

        choice = input().strip()
        if choice == "1":
            output_dir = create_output_directory()
            grid_connected(output_dir)
        elif choice == "2":
            output_dir = create_output_directory()
            tracking_pv(output_dir)
        elif choice == "3":
            output_dir = create_output_directory()
            off_grid(output_dir)
        elif choice == "4":
            output_dir = create_output_directory()
            monthly_radiation(output_dir)
        elif choice == "5":
            output_dir = create_output_directory()
            daily_radiation(output_dir)
        elif choice == "6":
            output_dir = create_output_directory()
            hourly_radiation(output_dir)
        elif choice == "7":
            output_dir = create_output_directory()
            tmy(output_dir)
        elif choice == "8":
            output_dir = create_output_directory()
            horizon_profile(output_dir)
        # ignore the case of Q
        elif choice.lower() == "q":
            break
        else:
            print("Invalid choice. Please try again.")


# Start the application
if __name__ == "__main__":
    main_menu()
