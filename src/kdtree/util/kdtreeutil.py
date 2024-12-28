from random import choice
from typing import List

def quickselect_median(l, dimension, pivot_function=choice):
    n = len(l)
    index = n // 2 if n % 2 == 0 else n // 2 + 1
    return quickselect(l, index, pivot_function, dimension)

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
        # assert k == 0
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
    n = len(l)
    index = n // 2 if n % 2 == 0 else n // 2 + 1
    return l[index]

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

def chunked(array: List[tuple[float,float]], chunkSize: int) -> List[tuple[float,float]]:
    """
    Split array it to chunks of chunk_size elements.
    Parameters:
        array - the list to be chunked
        chunkSize - size of one chunk
    Returns:
        Array of subarrays of size chunk_size
    """
    return [array[i:i + chunkSize] for i in range(0, len(array), chunkSize)]

# def partition_array(array: List[tuple[float,float]],dimension):

#     if not array:
#         return None,None,None
#     n = len(array)
#     if n == 1:
#         return None,None,array[0]
#     if n == 2:
#         return [array[0]],[array[1]],min(array[0],array[1],key=lambda element: element[dimension]) 

#     pivot = pick_pivot(array,dimension)
#     # This could cause a problem since it might get the earliest pivot
#     pivot_index = array.index(pivot)
#     array[pivot_index], array[-1] = array[-1], array[pivot_index]

#     i = 0
#     for j in range(n - 1):
#         if array[j] < pivot:
#             array[i], array[j] = array[j], array[i]
#             i += 1

#     array[i], array[-1] = array[-1], array[i]
#     left = array[:max(i-1,0)]
#     right = array[i+1:]

#     return left, right, pivot

def partition_array(array: List[tuple[float, float]], dimension: int):
    """
    Returns arrays of points partitioned by median 
    Parameters:
    array - list of k-dimentional points points
    dimentsion - the index of dimentsion from [0,k-1], which the points should be compared by
    Returs:
    left - all of the elements are less than or equal to median by the given dimension, 
    right - all of the elements are grater than or equal to median by the given dimension,
    pivot - index of the median point
    """
    if not array:
        return None, None, None

    n = len(array)
    if n == 1:
        return None, None, array[0]
    
    if n == 2:
        return [array[0]], [array[1]], min(array[0], array[1], key=lambda element: element[dimension])

    # Select the pivot using the pivot function
    pivot = pick_pivot(array, dimension)
    pivot_index = array.index(pivot)
    array[pivot_index], array[-1] = array[-1], array[pivot_index]

    i = 0
    for j in range(n - 1):
        if array[j][dimension] < pivot[dimension]:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[-1] = array[-1], array[i]

    left = array[:i]  
    right = array[i+1:] 

    return left, right, array[i]