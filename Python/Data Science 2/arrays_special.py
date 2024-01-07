def float_range(start_value, end_value, step):
    values = []
    if start_value >= end_value or step <= 0.00:
        return []
    else:
        while start_value < (end_value - round(step/2,2)):
            start_value += step
            values.append(round(start_value,2))
    return values