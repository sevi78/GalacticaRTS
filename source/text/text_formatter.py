import locale
import re

SUFFIXES = ['', 'k', 'M', 'B', 'T']


def format_number(n: [int, float], digits: int = 0) -> str:
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


def validate_text_format(text: str, format_dict: dict) -> str:
    """
    Validates a text string against a specified format.

    Args:
    text (str): The text to be validated.
    format_dict (dict): A dictionary specifying the expected format.
                        e.g., {'server': 'xxx.xxx.x.xx', 'port': '0000'}

    Returns:
    str: 'Valid' if the text matches the format, or a description of the error.
    """
    # Remove surrounding braces and split the text into key-value pairs
    try:
        text = text.strip('{}')
        text_dict = {}
        for item in re.findall(r'"([^"]+)"\s*:\s*"?([^",}]+)"?', text):
            key, value = item
            text_dict[key.strip()] = value.strip()
    except Exception:
        return f"Invalid format. Expected: {format_dict}, Received: {text}"

    # Check if all required keys are present
    if set(format_dict.keys()) != set(text_dict.keys()):
        return f"Invalid format. Expected: {format_dict}, Received: {text_dict}"

    # Validate each part
    for key, format_value in format_dict.items():
        if key == 'server':
            ip = text_dict[key]
            ip_parts = ip.split('.')
            if len(ip_parts) != 4:
                return f"Invalid IP address. Expected format: {format_value}, Received: {ip}"
            if not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
                return f"Invalid IP address: each part should be between 0 and 255. Received: {ip}"
            if not (len(ip_parts[2]) == 1 and len(ip_parts[3]) == 2):
                return f"Invalid IP address format. Expected: {format_value}, Received: {ip}"
        elif key == 'port':
            port = text_dict[key]
            if not port.isdigit() or len(port) != len(format_value):
                return f"Invalid port. Expected format: {format_value} ({len(format_value)} digits), Received: {port}"
        else:
            if text_dict[key] != format_value:
                return f"Invalid {key}. Expected: {format_value}, Received: {text_dict[key]}"

    return "Valid"


# Test cases
if __name__ == '__main__':
    format_dict = {'server': 'xxx.xxx.x.xx', 'port': '0000'}

    print(validate_text_format('{"server":"192.168.1.22","port":"5555"}', format_dict))
    print(validate_text_format('{"server":"192.168.1.222","port":"5555"}', format_dict))
    print(validate_text_format('{"server":"192.168.1.22","port":"555"}', format_dict))
    print(validate_text_format('{"server":"192.168.01.22","port":"5555"}', format_dict))
    print(validate_text_format('{"server":"192.168.1.22", "port":"5555"}', format_dict))
    print(validate_text_format('{"server":"192.168.1.22","port":"55555"}', format_dict))

    # Test with a different format
    new_format = {'server': 'xxx.xxx.x.xx', 'port': '00000', 'protocol': 'TCP'}
    print(validate_text_format('{"server":"192.168.1.22","port":"55555","protocol":"TCP"}', new_format))
    print(validate_text_format('{"server":"192.168.1.22","port":"55555","protocol":"UDP"}', new_format))
