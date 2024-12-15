from random import choice
from typing import List

# TODO:
# Write all of the descriptions and comments

def quickselect_median(l, dimension, pivot_function=choice):
    return quickselect(l, len(l) // 2, pivot_function, dimension)


def quickselect(array, k, pivot_function,dimension):
    """
    Select the kth element in the array
    Parameters:
    list - List of elements
    k - index of the midpoint
    pivot_function: Function to choose a pivot, defaults to random.choice
    Returs:
    The kth element of the array
    """
    if len(array) == 1:
        assert k == 0
        return array[0]

    pivot = pivot_function(array,dimension)

    lows = [element for element in array if element[dimension] < pivot[dimension]]
    highs = [element for element in array if element[dimension] > pivot[dimension]]
    pivots = [element for element in array if element[dimension] == pivot[dimension]]

    if k < len(lows):
        return quickselect(lows, k, pivot_function, dimension)
    # In this case, if k is contained on the interval [len(rows)+1,len(rows)+len(pivots)], that means we have found the pivot
    elif k < len(lows) + len(pivots):
        return pivots[0]
    else:
        return quickselect(highs, k - len(lows) - len(pivots), pivot_function,dimension)


def nlogn_median(l,dimension):
    l = sorted(l,key=lambda elem: elem[dimension])
    return l[len(l) // 2]

def pick_pivot(l,dimension):
    """
    Pick a good pivot within l, a list of numbers
    This algorithm runs in O(n) time.
    """
    assert len(l) > 0

    # If there are < 5 items use the O(nlog(n)) method, as it's in O(1) time anyways 
    if len(l) < 5:
        return nlogn_median(l,dimension)

    chunks = chunked(l, 5)
    full_chunks = [chunk for chunk in chunks if len(chunk) == 5]


    # In this case, array is split into smaller chunks of size 5, therefore the size of new array will be n/5
    # In each array the median can be found in O(1) time, for each element of the array that gives us O(n) for finding each median
    sorted_groups = [sorted(chunk, key=lambda element: element[dimension]) for chunk in full_chunks]

    # The median of each chunk must be at the index 2
    medians = [chunk[2] for chunk in sorted_groups]
    
    # Then the quickselect runs in pessimistic time of O(k^2) where k is the size of given array, but since this value is constant (5 in this case)
    # We obtain max of 25 iteration per array, that still gives us O(n) time complexity for the whole algorithm
    median_of_medians = quickselect_median(medians, dimension, pick_pivot)
    return median_of_medians

def chunked(array: List[tuple[float,float]], chunk_size: int) -> List[tuple[float,float]]:
    """
    Split array it to chunks of chunk_size elements.
    Parameters:
        TODO
    Returns:
        Array of subarrays of size chunk_size
    """
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]

def partition_array(array: List[tuple[float,float]],dimension):
    """
    
    """
    if array == None:
        return None,None,None
    n = len(array)
    if n == 1:
        return array,None,array[0]
    if n == 2:
        return [array[0]],[array[1]],min(array[0],array[1]) 

    pivot = pick_pivot(array,dimension)
    # This could cause a problem since it might get the earliest pivot, TODO
    pivot_index = array.index(pivot)
    array[pivot_index], array[-1] = array[-1], array[pivot_index]

    i = 0
    for j in range(n - 1):
        if array[j] < pivot:
            array[i], array[j] = array[j], array[i]
            i += 1

    array[i], array[-1] = array[-1], array[i]
    left = array[:i]
    right = array[i+1:]

    return left, right, pivot