from picture import Picture as picture

cache = {}
cache_counter = {}
def Picture(filename):
    if filename in cache_counter:
        cache_counter[filename] += 1
    else:
        cache_counter[filename] = 1

    if cache_counter[filename] == 2:
        cache[filename] = picture(filename)
        return cache[filename]

    return picture(filename)
