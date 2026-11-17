def add_to_dict(dict: dict, key, val):
    if key in dict.keys():
        dict[key].append(val)
    else:
        dict[key] = [val]
        
def remove_from_dict(dict: dict, key, val):
    if key in dict.keys():
        dict[key].remove(val)
        
        if len(dict[key]) == 0:
            del dict[key]