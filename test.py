import re

with open('log_list.txt', 'r') as f:
    for log in f:
        result = re.search(r"ticky: INFO: ([\w \'\[\]#]*) \(([\w]*)\)", log)

        if not result == None:
            print("Username is: " + str(result.group(2)))
            print("Process: " + str(result.group(1)))