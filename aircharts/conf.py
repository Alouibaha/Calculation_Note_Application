from aircharts.altitude_to_pressure import altitude_to_pressure
import psychrolib

initial_altitude = 100
initial_area = 36
initial_air_blowing_flow = 6497
initial_people_heat_gains = 120
initial_lighting_heat_gains = 15
initial_pressure = altitude_to_pressure(initial_altitude)

initial_mu_motor = 0.69

initial_equipment_table_n_rows = 9

def set_system_of_units():
    psychrolib.SetUnitSystem(psychrolib.SI)
