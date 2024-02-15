import locale

SUFFIXES = ['', 'k', 'M', 'B', 'T']


def format_number(n, digits=0):
    if n < 0:
        return str(n)
    magnitude = 0
    while n >= 1000 and magnitude < len(SUFFIXES) - 1:
        magnitude += 1
        n /= 1000
    if isinstance(n, float) and n % 1 == 0:
        formatted_number = locale.format_string(f'%.0f', n, grouping=True)
    else:
        formatted_number = locale.format_string(f'%.{digits}f', n, grouping=True)
        formatted_number = formatted_number.rstrip('0').rstrip('.')
    return f'{formatted_number}{SUFFIXES[magnitude]}'


def to_roman(num: int):
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
