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

# def print_some_times():
#     print('running')
#     s.enter(5, 1, reminder, ())
#     s.run()
#
# @route("/chat", method='POST')
# def reminder():
#     print("go")
#     return json.dumps({"animation": "bored", "msg": "C'mon, I'm getting bored. Say something!"})

# print_some_times()
