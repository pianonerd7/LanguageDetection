
language_model = dict()
language_count = dict()
SMOOTHING_CONST = 1

def read_from_file(in_file):
    for line in file(in_file):
        process_training_line(line)
    convert_count_to_probability()

# <4gram, dict<language, probability>>
def process_training_line(line):
    space_index = line.index(' ')
    language = line[:space_index]
    data = line[space_index + 1:]

    if language not in language_count:
        language_count[language] = 0

    for index, char in enumerate(data):
        cur_4_gram = data[index:index + 4]

        if cur_4_gram not in language_model:
            language_model[cur_4_gram] = dict()
        if language not in language_model[cur_4_gram]:
            language_model[cur_4_gram][language] = SMOOTHING_CONST + 1
            language_count[language] += SMOOTHING_CONST + 1
        else:
            language_model[cur_4_gram][language] += 1
            language_count[language] += 1

def convert_count_to_probability():
    for cur_4_gram in language_model:
        for language in language_model[cur_4_gram]:
            language_model[cur_4_gram][language] = language_model[cur_4_gram][language]/float(language_count[language])

read_from_file("./TxtFiles/input.train.txt")
print language_model
