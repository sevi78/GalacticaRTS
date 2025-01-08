# import time
# import random
#
# w = 3
# velocities = [(x, y) for x in range(-w, w) for y in range(-w, w)]
# loops = 10000000
#
#
# print (velocities)
# # random_v = [(random.randint(-2, 2), random.randint(-2, 2)) for _ in range(8)]
#
# start_time = time.time()
# for _ in range(loops):
#     v = random.choice(velocities)
#
# end_time = time.time()
# print(f"random.choice time: {end_time - start_time}")
#
# start_time = time.time()
# for _ in range(loops):
#     v = (random.randint(-w, w), random.randint(-w, w))
#
# end_time = time.time()
# print(f"random.randint time: {end_time - start_time}")

#
# def find_first_nonzero_after_decimal(number):
#     # Convert the number to a string
#     num_str = str(number)
#
#     # Find the decimal point
#     decimal_index = num_str.find('.')
#
#     # If there's no decimal point, return the length of the string
#     if decimal_index == -1:
#         return len(num_str)
#
#     # Start checking from the position after the decimal point
#     for i, digit in enumerate(num_str[decimal_index + 1:], start=1):
#         if digit != '0':
#             return i
#
#     # If all digits after decimal are zero, return the length of the string
#     return len(num_str) - decimal_index - 1
#
#
# # Test cases
# test_numbers = [0.0002, 0.0005, 0.0045, 0.00983, 0.0356, 0.06, 0.342, 0.543, 1.876, 1.098, 10.456, 43.987, 100.8765, 300.567, 1890.8, 4321.9]
#
# for num in test_numbers:
#     result = find_first_nonzero_after_decimal(num)
#     print(f"{num}: {result}")
#
#
#
#     """
#     result = :
#     0.0002: 4
# 0.0005: 4
# 0.0045: 3
# 0.00983: 3
# 0.0356: 2
# 0.06: 2
# 0.342: 1
# 0.543: 1
# 1.876: 1
# 1.098: 2
# 10.456: 1
# 43.987: 1
# 100.8765: 1
# 300.567: 1
# 1890.8: 1
# 4321.9: 1
#     """
import math


def find_first_nonzero_digit_index(number):
    if number == 0:
        return 0

    abs_number = abs(number)

    # Calculate the negative logarithm base 10
    log_value = -math.log10(abs_number)

    # fix
    # if abs_number >= 1:
    #     return 0
    # Floor the log value to get the correct index
    floor_value = math.floor(log_value)
    log_value = floor_value
    return log_value


# Test cases
test_numbers = [0.0002, 0.0005, 0.0045, 0.00983, 0.0356, 0.06, 0.342, 0.543, 1.876, 1.098, 10.456, 43.987, 100.8765,
                300.567, 1890.8, 4321.9]


def ndigits(v: float, digit=4) -> int:
    """return a number of digits for a float:

    set digit to lowest number of digits, for example 0.0001 would be 4
    """

    n = 0

    if v < 1.0:
        n = max(0, math.ceil(-math.log10(abs(v))))
        n -= digit
    if v >= 1.0:
        n = max(0, math.ceil(math.log10(abs(v))))
        n += digit - 1

    return abs(n)


for num in test_numbers:
    result = find_first_nonzero_digit_index(num)
    # print(f"{num}: {result}")

    print("ndigits:", ndigits(num))



color = [2323.0011, 0.011, 0.001, 0.0]
print (all(color) == 0.0)
