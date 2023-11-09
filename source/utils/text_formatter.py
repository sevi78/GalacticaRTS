import locale



SUFFIXES = ['', 'k', 'M', 'B', 'T']

def format_number(n, digits=0):
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




