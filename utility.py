
language_models = dict()
SMOOTHING_CONST = 1

def read_from_file(in_file):
    for line in file(in_file):
        process_training_line(line)


def process_training_line(line):
    space_index = line.index(' ')
    language = line[:space_index]

    data = line[space_index + 1:]
    print line[space_index+1:-4]
    for index, char in enumerate(data):
        cur_4_gram = data[index:index + 4]

        if language not in language_models:
            language_models[language] = dict()
        language_model = language_models[language]

        if cur_4_gram in language_model:
            language_model[cur_4_gram] = language_model[cur_4_gram] + 1
        else:
            language_model[cur_4_gram] = 1 + SMOOTHING_CONST

        print cur_4_gram
        if index == len(data) -4:
            break

str = "malaysian hello hello world, this is a sample string that has no actual content"
process_training_line(str)
print language_models