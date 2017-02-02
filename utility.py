
language_model = dict()
language_count = dict()
SMOOTHING_CONST = 1
GRAM_SIZE = 4

def file_to_probability(in_file):
    for line in file(in_file):
        process_training_line(line)
    convert_count_to_probability()

# <4gram, dict<language, probability>>
def process_training_line(line):
    language, data = get_language_and_data(line)

    if language not in language_count:
        language_count[language] = 0

    all_grams = get_grams(data)
    
    for gram in all_grams:
        if gram not in language_model:
            language_model[gram] = dict()
        cur_gram_dict = language_model[gram]
        if language not in cur_gram_dict:
            cur_gram_dict[language] = SMOOTHING_CONST + 1
            language_count[language] += SMOOTHING_CONST + 1
        else:
            cur_gram_dict[language] += 1
            language_count[language] += 1

    return language_model, language_count
        
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

# Returns the language of the string, and the string to extract n-gram from
def get_language_and_data(line):
    space_index = line.index(' ')
    language = line[:space_index]
    data = line[space_index + 1:]
    return language, data

# Given a string, returns all the n-gram in that string where the length of the gram 
# is specified by the GRAM_SIZE constant
def get_grams(data):
    grams = []
    for index, char in enumerate(data):
        grams.append(data[index:index + GRAM_SIZE])
    return grams