def merge_and_deduplicate(lists):
    """
    Merge multiple lists and remove duplicates using functional programming with lambda.
    
    Parameters:
    lists (list of lists): The list of lists to be merged.
    
    Returns:
    list: A merged list with duplicates removed.
    """
    # Flatten the list of lists
    flattened_list = list(chain.from_iterable(lists))
    
    # Deduplicate using reduce with a lambda function
    deduplicated_set = reduce(lambda acc, item: acc.union({item}), flattened_list, set())
    
    # Convert the set back to a list
    return list(deduplicated_set)
