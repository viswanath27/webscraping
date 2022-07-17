def remove_unrelated_words(data):
    new_data = {}
    for k, values in data.items():
        new_list = []
        for item in values:
            if len(item) >= 1:
                if item.lower()[0] == k:
                    new_list.append(item)
        new_data[k] = new_list
    print(new_data)


