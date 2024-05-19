import streamlit as st
import itertools

# Provided list of resistors
resistors = [
    0, 1, 2, 2.2, 4.7, 5.1, 10, 20, 22, 33, 47, 49.9, 51, 75, 100, 120, 150, 200, 220, 270, 300,
    330, 390, 470, 510, 560, 680, 820, 1000, 1200, 1500, 1800, 2000, 2200, 2400, 2700, 3000, 3300,
    3600, 3900, 4700, 4990, 5100, 5600, 6200, 6800, 7500, 8200, 9100, 10000, 12000, 13000, 15000,
    18000, 20000, 22000, 24000, 27000, 30000, 33000, 39000, 47000, 49900, 51000, 56000, 68000, 75000,
    82000, 100000, 120000, 150000, 200000, 220000, 300000, 330000, 470000, 510000, 1000000, 2000000, 10000000
]

# Streamlit interface
st.title("Voltage Divider Resistor Calculator with Power Check")

# User inputs
Vin = st.number_input("Input Voltage (Vin)", min_value=0.0, value=48.0)
Vout = st.number_input("Desired Output Voltage (Vout)", min_value=0.001, value=0.986, step=0.001,format="%.3f")
range_min, range_max = st.slider("Select Resistor Range (Ω)", min_value=1, max_value=10000000, value=(1000, 1000000))

# Filter resistors within selected range
filtered_resistors = [r for r in resistors if range_min <= r <= range_max]

# Initialize minimum error and best resistor values
min_error = float('inf')
best_pair = (None, None)

# Calculate voltage divider
for R1, R2 in itertools.permutations(filtered_resistors, 2):
    # Calculate output voltage
    Vout_calculated = Vin * R2 / (R1 + R2)
    
    # Calculate error
    error = abs(Vout - Vout_calculated)
    
    # Update best resistor pair
    if error < min_error:
        min_error = error
        best_pair = (R1, R2)

if best_pair[0] is not None and best_pair[1] is not None:
    R1, R2 = best_pair
    Vout_actual = Vin * R2 / (R1 + R2)
    
    # Calculate power dissipation for R1 and R2
    I = Vin / (R1 + R2)
    P_R1 = I**2 * R1
    P_R2 = I**2 * R2
    
    st.success(f"Best resistor pair: R1 = {R1}Ω, R2 = {R2}Ω")
    st.success(f"Calculated output voltage: {Vout_actual}V")
    st.success(f"Power dissipation in R1: {P_R1:.6f}W")
    st.success(f"Power dissipation in R2: {P_R2:.6f}W")
    
    # Check if power dissipation exceeds 0603 resistor rated power (0.1W)
    if P_R1 > 0.1:
        st.error(f"Power dissipation in R1 exceeds the rated power of a 0603 resistor!")
    if P_R2 > 0.1:
        st.error(f"Power dissipation in R2 exceeds the rated power of a 0603 resistor!")
else:
    st.warning("No valid resistor pair found within the selected range.")
