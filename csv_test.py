import re
import csv
import operator

def generate_errors_file():
    csv_columns = ['Type', 'Occurrences']
    errors = []
    error_type = []

    with open('log_list.txt', 'r') as f:
        for log in f:
            error = {}
            result = re.search(r"ticky: ERROR: ([\w ']*)", log)

            if not result == None:
                error['Type'] = result.groups(0)[0].strip()
                if not error['Type'] in error_type:
                    error['Occurrences'] = 1
                    errors.append(error)
                    error_type.append(error['Type'])
                else:
                    for item in errors:
                        if item['Type'] == error['Type']:
                            item['Occurrences'] += 1
                            break

    with open('error_messages.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(sorted(errors, key=operator.itemgetter('Occurrences'), reverse=True))

def generate_user_stats_file():
    csv_columns = ['Username', 'Type', 'Message', 'Occurrences']
    user_stats = []

    with open('log_list.txt', 'r') as f:
        for log in f:
            user_stat = {}
            result = re.search(r"ticky: ([\w]*): ([\w '\[\]#]*) \(([\w]*)\)", log)

            if not result == None:
                user_stat['Username'] = result.group(3)
                user_stat['Status'] = result.group(1)
                user_stat['Message'] = result.group(2)

                if user_stat['Status'] == 'INFO':
                    if user_stats == []:
                        user_stat['Occurrences'] = 1
                        user_stats.append(user_stat)
                    else:
                        for item in user_stats:
                            if item['Username'] == user_stat['Username'] and item['Message'] == user_stat['Message']:
                                item['Occurrences'] += 1
                                break
                            elif item['Username'] == user_stat['Username'] and item['Message'] != user_stat['Message']:
                                user_stat['Occurrences'] = 1
                                user_stats.append(user_stat)
                                break
                elif user_stat['Status'] == 'ERROR':
                    for item in user_stats:
                        print("Loop reached")
                        if item['Username'] == user_stat['Username'] and item['Message'] == user_stat['Message']:
                            item['Occurrences'] += 1
                            break
                        elif item['Username'] == user_stat['Username'] and item['Message'] != user_stat['Message']:
                            user_stat['Occurrences'] = 1
                            user_stats.append(user_stat)
                            break
                                
    
    print(user_stats)
                    


generate_user_stats_file()