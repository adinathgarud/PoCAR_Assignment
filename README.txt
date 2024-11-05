Soil Water Balance Model

This script simulates the daily water balance for crops based on rainfall data,
soil moisture, crop water uptake, runoff, and groundwater percolation. 
It computes and saves the results into a CSV file for further analysis.

Requirements

- Python 3.x
- pandas (for reading CSV files and managing data)
- numpy (for numerical calculations)

You can install the required packages using:

pip install pandas numpy

Description

This program calculates the water balance for two types of soil: "deep" and "shallow". 
It uses daily rainfall data to determine:
- Runoff based on the rainfall amount.
- Soil moisture (including excess that exceeds soil capacity).
- Crop water uptake (a fixed daily demand).
- Groundwater percolation (a fraction of the remaining soil moisture).

The results are saved to a CSV file which contains the calculated values for each day.

How to Run

1. Ensure you have a CSV file named `daily_rainfall_jalgaon_chalisgaon_talegaon_2022.csv` in the same 
directory as the script. 
This file should have a column labeled 'Rainfall' containing daily rainfall values (in mm).
2. Run the script using the command:

python soil_water_balance.py

3. The script will prompt you to input the soil type ('deep' or 'shallow').
4. The script will compute the water balance and save the results into a file named 
`soil_water_balance_<soil_type>.csv` (where <soil_type> is either "deep" or "shallow").

Variables

Constants

- CROP_UPTAKE:
  The fixed daily crop water uptake in mm. This value represents the amount of water the crop consumes each 
  day,regardless of rainfall. In this model, the crop uptake is set to 4 mm.

- SOIL_PARAMETERS:
  A dictionary containing the soil parameters for two soil types (`deep` and `shallow`):
  SOIL_PARAMS = {
      "deep": {'C': 100, 'gw_fraction': 0.2},
      "shallow": {'C': 42, 'gw_fraction': 0.4}
  }
  - capacity: Maximum soil moisture capacity (in mm) for each soil type.
  - gw_fraction: The fraction of soil moisture that is available for groundwater recharge.

- RUNOFF_COEFFICIENTS:
  A dictionary mapping rainfall ranges (in mm) to corresponding runoff coefficients. 
  These coefficients represent the percentage of rainfall that becomes runoff:
  RUNOFF_COEFFICIENTS = {
      (0, 25): 0.2,
      (25, 50): 0.3,
      (50, 75): 0.4,
      (75, 100): 0.5,
      (100, float('inf')): 0.7
  }

Functions

1. runoff_coefficient(rain)

This function calculates the runoff coefficient based on the rainfall amount for the day. 
The runoff coefficient determines the portion of rainfall that becomes surface runoff, 
and the rest is considered infiltration into the soil.

Parameters:
- rain (float): The amount of rainfall (in mm) for a given day.

Returns:
- (float): The runoff coefficient (between 0 and 1).

Example:
runoff_coefficient(30)  # Returns 0.3 for rainfall between 25 and 50 mm.

2. water_balance(soil_type, rainfall_data)

This function calculates the soil water balance for a given soil type and daily rainfall data. 
It calculates daily soil moisture, runoff, excess water, crop water uptake, and groundwater recharge.

Parameters:
- soil_type (str): The type of soil ('deep' or 'shallow').
- rainfall_data (array-like): A sequence (list, array) of daily rainfall amounts (in mm).

Returns:
- A DataFrame containing the following columns:
  - Day: Day number (starting from 1).
  - Rainfall (mm): Daily rainfall (in mm).
  - Runoff + Excess (mm): Runoff and excess water from the soil.
  - Crop Water Uptake (mm): The amount of water taken up by the crop.
  - Soil Moisture (mm): The remaining soil moisture after crop uptake.
  - Percolation to Groundwater (mm): The groundwater recharge (percolation) for that day.

Example:
result_df = water_balance('deep', [10, 20, 30])  # Compute for deep soil with rainfall data [10mm, 20mm, 30mm]

3. main()

The main() function orchestrates the entire process:
- Prompts the user for the soil type (either 'deep' or 'shallow').
- Loads the daily rainfall data from a CSV file.
- Calls the water_balance() function to compute the results.
- Saves the results into a CSV file with a filename based on the soil type.

User Input:
- The user is prompted to input the soil type.

Example:
Please enter the soil type ('deep' or 'shallow'): deep

Outputs:
- The function generates and saves a CSV file named `soil_water_balance_<soil_type>.csv`
 (where <soil_type> is the type entered by the user).

File Output

After running the script, the results will be saved into a CSV file with the name:
soil_water_balance_<soil_type>.csv
Where <soil_type> is either "deep" or "shallow".

The CSV file will contain the following columns:
1. Day: The day number.
2. Rainfall (mm): The rainfall for that day (in mm).
3. Runoff + Excess (mm): The total runoff and excess water for that day.
4. Crop Water Uptake (mm): The water taken up by the crop for that day.
5. Soil Moisture (mm): The remaining soil moisture after crop uptake.
6. Percolation to Groundwater (mm): The groundwater recharge (percolation) for that day.

Example Output (CSV Format)

For the soil type "deep", the output CSV might look like this:

Day,Rainfall (mm),Runoff + Excess (mm),Crop Water Uptake (mm),Soil Moisture (mm),Percolation to Groundwater (mm)
1,10,2,4,6,1.2
2,15,3,4,8,1.6
3,30,6,4,9,2.4
...

Error Handling

- Invalid Soil Type: If the user inputs a soil type that is not "deep" or "shallow", an error message is shown.
- File Not Found: If the rainfall data CSV file is not found, an error message is shown.

Conclusion

This script is a simple yet effective way to model the water balance of crops based on daily rainfall and soil
 parameters. The user can input different soil types and calculate the daily water balance for various 
 agricultural scenarios. The results are saved into a CSV file for further analysis.

