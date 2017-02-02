import math 

language_model = dict()
language_count = dict()
SMOOTHING_CONST = 1
GRAM_SIZE = 4

def file_to_probability(in_file):
    for line in file(in_file):
        process_training_line(line)
    convert_count_to_probability()
    return language_model

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
        
def convert_count_to_probability():
    for cur_4_gram in language_model:
        cur_4_gram_dict = language_model[cur_4_gram]
        for language in cur_4_gram_dict:
            cur_4_gram_dict[language] = cur_4_gram_dict[language]/float(language_count[language])

def file_to_language_suggestion(in_file, out_file, LM):
    output_file = file(out_file, 'w')
    for line in file(in_file):
        prediction = predict_language(line, LM)
        output_file.write(prediction)

def predict_language(line, LM):
    #compute here
    new_language = compute_probabilities_for_all_languages(line, LM)
    return new_language + " " + line #<-- should use stringbuilder instead? 

def compute_probabilities_for_all_languages(line, LM):
    probabilities = dict()
    all_grams = get_grams(line)

    for gram in all_grams:
        if gram in LM:
            for language in LM[gram]:
                if language not in probabilities:
                    probabilities[language] = 0
                probabilities[language] += math.log(LM[gram][language])
    return get_largest_from_dict(probabilities)

def get_largest_from_dict(probabilities):
    highest_prob_language, highest_prob = "", 0
    for langauge in probabilities:
        if probabilities[langauge] > highest_prob:
            highest_prob_language, highest_prob = langauge, highest_prob
    return highest_prob_language

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
