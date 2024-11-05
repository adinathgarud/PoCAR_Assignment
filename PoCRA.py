import pandas as pd
import numpy as np


CROP_UPTAKE = 4  
SOIL_PARAMETERS = {
    "deep": {'C': 100, 'gw_fraction': 0.2},
    "shallow": {'C': 42, 'gw_fraction': 0.4}
} 


RUNOFF_COEFFICIENTS = {
    (0, 25): 0.2,
    (25, 50): 0.3,
    (50, 75): 0.4,
    (75, 100): 0.5,
    (100, float('inf')): 0.7
}

def runoff_coefficient(rain):
    
    for (low, high), coeff in RUNOFF_COEFFICIENTS.items():
        if low <= rain < high:
            return coeff
    return 0.7  


def water_balance(soil_type, rainfall_data):
    if soil_type not in SOIL_PARAMETERS:
        raise ValueError("Soil type must be 'deep' or 'shallow'.")
    soil = SOIL_PARAMETERS[soil_type]
    C, gw_fraction = soil['C'], soil['gw_fraction']

    
    sm_previous = 0  
    results = {
        "Day": [],
        "Rainfall (mm)": [],
        "Runoff + Excess (mm)": [],
        "Crop Water Uptake (mm)": [],
        "Soil Moisture (mm)": [],
        "Percolation to Groundwater (mm)": []
    }

    
    for day, rain in enumerate(rainfall_data, start=1):
        
        runoff = runoff_coefficient(rain) * rain
        infiltration = rain - runoff
        
        
        sm_today = sm_previous + infiltration
        excess = max(0, sm_today - C)
        sm_today = min(sm_today, C)  
        
        
        uptake = min(CROP_UPTAKE, sm_today)
        sm_today -= uptake
        
        
        gw = gw_fraction * sm_today

       
        results["Day"].append(day)
        results["Rainfall (mm)"].append(rain)
        results["Runoff + Excess (mm)"].append(runoff + excess)
        results["Crop Water Uptake (mm)"].append(uptake)
        results["Soil Moisture (mm)"].append(sm_today)
        results["Percolation to Groundwater (mm)"].append(gw)

        
        sm_previous = sm_today

    
    result_df = pd.DataFrame(results)

    
    rain_sum = np.sum(rainfall_data)
    sm_final = sm_previous
    runoff_sum = np.sum(results["Runoff + Excess (mm)"])
    uptake_sum = np.sum(results["Crop Water Uptake (mm)"])
    gw_sum = np.sum(results["Percolation to Groundwater (mm)"])

    return result_df


def main():
    soil_type = input("Please enter the soil type ('deep' or 'shallow'): ").strip().lower()

    if soil_type not in ["deep", "shallow"]:
        print("Invalid soil type. Please enter either 'deep' or 'shallow'.")
        return

    
    
    try:
        rainfall_data = pd.read_csv('daily_rainfall_jalgaon_chalisgaon_talegaon_2022.csv')['Rainfall'].values
    except FileNotFoundError:
        print("Error: The file was not found.")
        return

    
    result_df = water_balance(soil_type, rainfall_data)
    
    
    output_filename = f"soil_water_balance_{soil_type}.csv"
    result_df.to_csv(output_filename, index=False)

    print(f"Water balance calculation complete. Results saved to {output_filename}.")

if __name__ == "__main__":
    main()
