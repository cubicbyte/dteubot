def array_split(array: list, row_size: int) -> list:
    return [array[i:i + row_size] for i in range(0, len(array), row_size)]
