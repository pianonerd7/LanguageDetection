
language_models = dict()
language_count = dict()
SMOOTHING_CONST = 1

def read_from_file(in_file):
    for line in file(in_file):
        process_training_line(line)
    convert_count_to_probability()


def process_training_line(line):
    space_index = line.index(' ')
    language = line[:space_index]
    data = line[space_index + 1:]

    if language not in language_count:
        language_count[language] = 0

    for index, char in enumerate(data):
        cur_4_gram = data[index:index + 4]

        if language not in language_models:
            language_models[language] = dict()
        language_model = language_models[language]

        if cur_4_gram in language_model:
            language_model[cur_4_gram] = language_model[cur_4_gram] + 1
        else:
            language_model[cur_4_gram] = 1 + SMOOTHING_CONST
        
        language_count[language] += 1

def convert_count_to_probability():
    for lang_model in language_models:
        count = language_count[lang_model]
        cur_dictionary = language_models[lang_model]
        for gram in cur_dictionary:
            cur_dictionary[gram] = cur_dictionary[gram]/float(count)

read_from_file("./TxtFiles/input.train.txt")
print language_models
