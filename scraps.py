non_lowercase_letter = ""
for value in user_message:
    if value not in list(string.ascii_lowercase):
        value = non_lowercase_letter