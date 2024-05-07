import locale

SUFFIXES = ['', 'k', 'M', 'B', 'T']


def format_number(n: int, digits: int = 0) -> str:
    """ formats a number (int) based on suffixes:
        ['', 'k', 'M', 'B', 'T']

        if n <=:
        1000 returns 1k
        1'000'000 returns 1M
        ect ...
    """
    if n == 0:
        return "0"
    if n < 0:
        return "-" + format_number(-n, digits)
    magnitude = 0
    while n >= 1000:
        if magnitude == len(SUFFIXES) - 1:
            break
        magnitude += 1
        n /= 1000
    if digits == 0:
        formatted_number = locale.format_string(f'%.0f', n, grouping=True)
    else:
        formatted_number = locale.format_string(f'%.{digits}f', n, grouping=True)
        formatted_number = formatted_number.rstrip('0').rstrip('.')
    return f'{formatted_number}{SUFFIXES[magnitude]}'


def get_reduced_number(number) -> float:
    """ reduces number to next even number like 10, 1000, 10000 ect """
    magnitude = 10 ** (len(str(int(number))) - 1)  # Correctly find the magnitude
    reduced_number = (number // magnitude) * magnitude
    return reduced_number


def to_roman(num: int) -> str:
    """ converts a number (int) into a roman number:
    10      = 'X'
    1000    = 'M'
    ect...
    """

    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    for i in range(len(val)):
        count = int(num / val[i])
        roman_num += syb[i] * count
        num -= val[i] * count
    return roman_num


if __name__ == "__main__":
    print(format_number(0))
    print(format_number(1100))
    print(format_number(10100))
    print(format_number(100010))
    print(format_number(1010000))
    print(format_number(10010000))

    print(format_number(1100, 0))
    print(format_number(10100, 1))
    print(format_number(100010, 2))
    print(format_number(1010000, 4))
    print(format_number(10010000, 5))

    print(format_number(-1100, 0))
    print(format_number(-10100, 1))
    print(format_number(-100010, 2))
    print(format_number(-1010000, 4))
    print(format_number(-10010000, 5))
