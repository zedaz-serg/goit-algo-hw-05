def binary_search_ceiling(arr: list[float], target: float) -> tuple[int, float | None]:
    
    n = len(arr)
    if n == 0:
        return (0, None)

    low = 0
    high = n - 1
    iterations = 0
    ceiling = None 

    while low <= high:
        iterations += 1
        
        mid = low + (high - low) // 2
        
        mid_value = arr[mid]

        if mid_value == target:
            return (iterations, mid_value)
        
        elif mid_value < target:
            low = mid + 1
        
        else:
            ceiling = mid_value
            high = mid - 1
            
    return (iterations, ceiling)