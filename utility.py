import math 

language_model = dict()
language_count = dict()
SMOOTHING_CONST = 1
GRAM_SIZE = 4
OTHER_LANGUAGE_GRAM_SENTENCE_PERCENTAGE = 50

def file_to_probability(in_file):
    for line in file(in_file):
        process_training_line(line.lower())
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
        print line.lower()
        prediction = predict_language(line, LM)
        output_file.write(prediction)
    output_file.close()

def predict_language(line, LM):
    new_language = compute_probabilities_for_all_languages(line.lower(), LM)
    print new_language + "\n\n"
    return new_language + " " + line #<-- should use stringbuilder instead? 

def compute_probabilities_for_all_languages(line, LM):
    probabilities = dict()
    all_grams = get_grams(line)

    non_trained_gram_count = 0

    for gram in all_grams:
        if gram in LM:
            for language in LM[gram]:
                if language not in probabilities:
                    probabilities[language] = 0
                probabilities[language] += LM[gram][language]
        else:
            non_trained_gram_count += 1

    print probabilities

    if is_other_language(non_trained_gram_count, len(all_grams)):
        return "other"
    return get_largest_from_dict(probabilities)

def is_other_language(non_trained_count, total_gram_count):
    val = (non_trained_count/float(total_gram_count))*100
    print val
    if val > OTHER_LANGUAGE_GRAM_SENTENCE_PERCENTAGE:
        return True
    else:
        return False

def get_largest_from_dict(probabilities):
    highest_prob_language, highest_prob = "", float(-1)
    for langauge in probabilities:
        if probabilities[langauge] > highest_prob:
            highest_prob_language, highest_prob = langauge, probabilities[langauge]
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
