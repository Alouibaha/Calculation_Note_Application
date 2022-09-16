def altitude_to_pressure(altitude_meters):
    return (1.19745*(10**-8))*(288.15-0.0065*altitude_meters)**5.25588
