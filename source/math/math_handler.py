def limit_number(n: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(n, max_value))


def get_sum_up_to_n(dict_, n):
    sum_ = 0
    for key, value in dict_.items():
        if key < n:
            sum_ += value

    return sum_