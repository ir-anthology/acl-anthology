def find_char_after(string, char, index):
    pos = find_char_after_no_error(string, char, index)
    if pos == -1:
        raise IndexError("Can't find the char >"+char+"<")
    return pos

def find_char_after_no_error(string, char, index):
    for i in range(index, len(string)):
        if string[i]==char:
            return i
    return -1