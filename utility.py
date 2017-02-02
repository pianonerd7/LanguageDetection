
language_model = dict()
language_count = dict()
SMOOTHING_CONST = 1

def file_to_probability(in_file):
    for line in file(in_file):
        process_training_line(line)
    convert_count_to_probability()

# <4gram, dict<language, probability>>
def process_training_line(line):
    language, data = get_language_and_data(line)

    if language not in language_count:
        language_count[language] = 0

    for index, char in enumerate(data):
        cur_4_gram = data[index:index + 4]

        if cur_4_gram not in language_model:
            language_model[cur_4_gram] = dict()
        cur_4_gram_dict = language_model[cur_4_gram]
        if language not in cur_4_gram_dict:
            cur_4_gram_dict[language] = SMOOTHING_CONST + 1
            language_count[language] += SMOOTHING_CONST + 1
        else:
            cur_4_gram_dict[language] += 1
            language_count[language] += 1
    return language_model

def convert_count_to_probability():
    for cur_4_gram in language_model:
        cur_4_gram_dict = language_model[cur_4_gram]
        for language in cur_4_gram_dict:
            cur_4_gram_dict[language] = cur_4_gram_dict[language]/float(language_count[language])

def file_to_language_suggestion(in_file, out_file, LM)
    output_file = file('output-file', 'w')
    for line in file(in_file):
        prediction = predict_language(line)
        output_file.write(prediction)

def predict_language(line):
    language, data = get_language_and_data(line)
    #compute here
    new_language = null
    return new_language + " " + data #<-- should use stringbuilder instead? 

#returns the language of the string, and the string to extract n-gram from
def get_language_and_data(line):
    space_index = line.index(' ')
    language = line[:space_index]
    data = line[space_index + 1:]
    return language, data

def get_grams(line):
