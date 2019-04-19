def recursive_items(dictionary, root, root_time):
    for key, value in dictionary.items():
        if type(value) is dict:
            if root:
                t = 5
                root_time = t
            else:
                print('t', root_time)
            print(key, value)
            recursive_items(value, False, root_time)
        else:
            print(key, value)

a = {'a': {1: {1: 2, 3: 4}, 2: {5: 6}}}

recursive_items(a, True, 0)
