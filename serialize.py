import json, os

author = 'name'
file_name = f'{author}.json'

input = str(input('score: '))

if os.path.isfile(file_name):
    print('found file')

    json_file = open(file_name)
    dict = json.load(json_file)
    json_file.close()

    pre_score = dict["score"]
    new_score = int(pre_score) + int(input)

    def_dict = {'score': new_score}

    with open("name.json", "w") as f:
        json.dump(def_dict, f)

    print(new_score)

else:
    print('file not found')
    def_dict = {'score': input}

    with open("name.json", "w") as f:
        json.dump(def_dict, f)
