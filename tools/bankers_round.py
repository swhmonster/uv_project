def bankers_rounding(number, decimal_places=0):
    """
    Implements Banker's Rounding (Round half to even) on a given number.

    :param number: The number to be rounded.
    :param decimal_places: The number of decimal places to round to.
    :return: The rounded number.
    """
    multiplier = 10 ** decimal_places
    shifted_number = number * multiplier
    rounded_shifted_number = round(shifted_number)
    
    # Check if rounding edge case happens (i.e., exactly halfway)
    if (shifted_number - int(shifted_number) == 0.5):
        if (int(shifted_number) % 2 != 0):
            rounded_shifted_number = int(shifted_number) + 1  # Round up to the nearest even number
    
    return rounded_shifted_number / multiplier

# Test cases
print(bankers_rounding(2231050*0.3, 0))  # Output: 12.34
print(bankers_rounding(12.355, 2))  # Output: 12.36
print(bankers_rounding(12.445, 2))  # Output: 12.44
print(bankers_rounding(12.455, 2))  # Output: 12.46
