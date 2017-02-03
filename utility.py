import math 

languages = ["malaysian", "tamil", "indonesian"]
language_model = dict()
language_count = dict()
SMOOTHING_CONST = 1
GRAM_SIZE = 4
OTHER_LANGUAGE_GRAM_SENTENCE_PERCENTAGE = 50

def file_to_probability(in_file):
    initialize_language_count()
    for line in file(in_file):
        process_training_line(line.lower())
    print "\n\n starting........ \n" 
    print language_count
    convert_count_to_probability()
    print "\n\n starting........ \n" 
    print language_count
    return language_model

# <4gram, dict<language, probability>>
def process_training_line(line):
    language, data = get_language_and_data(line)
    all_grams = get_grams(data)

    for gram in all_grams:
        if contains_digits(gram):
            continue

        if gram not in language_model:
            language_model[gram] = dict()
            for train_language in languages:
                language_model[gram][train_language] = SMOOTHING_CONST
                language_count[train_language] += SMOOTHING_CONST    
        language_model[gram][language] += 1
        language_count[language] += 1
    
def initialize_language_count():
    for language in languages:
        language_count[language] = 0

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
        if contains_digits(gram):
            continue

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

def contains_digits(text):
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for char in text:
        if char in numbers:
            return True
    return False