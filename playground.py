def print_username(string):
    split_string = string.split(" ")
    response = ""
    if "I am" in string or "i am" in string:
        name_index = split_string.index("am") + 1
        print(name_index)
        response = "Hello" + split_string[name_index]
        print(response)
    return response


string = "I am Sam Collins"
print_username(string)


