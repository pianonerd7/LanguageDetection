import constants

language_model = dict()
language_count = dict()

# file_to_probabilty takes in a file and outputs a language model with probability
def file_to_probability(in_file):
    initialize_language_count()
    for line in file(in_file):
        process_training_line(line.lower())
    convert_count_to_probability()
    return language_model

# file_to_language_suggestion takes an input file of sentences and a language model, 
# goes through the file line by line to assign a language based on the LM and writes
# to the out_file
def file_to_language_suggestion(in_file, out_file, LM):
    output_file = file(out_file, 'w')
    for line in file(in_file):
        prediction = predict_language(line, LM)
        output_file.write(prediction)
    output_file.close()

# initialize_language_count loops through all the training languages 
# (specified in constants.py) and gives them a value of 0
def initialize_language_count():
    for language in constants.languages:
        language_count[language] = 0

# <4gram, dict<language, probability>>
# process_training_line takes a line, breaks down to grams, and inserts to language model.
# skips if a number is present in the gram
def process_training_line(line):
    language, data = get_language_and_data(line)
    all_grams = get_grams(data)

    for gram in all_grams:
        if contains_digits(gram):
            continue
        if gram not in language_model:
            language_model[gram] = dict()
            for train_language in constants.languages:
                language_model[gram][train_language] = constants.SMOOTHING_CONST
                language_count[train_language] += constants.SMOOTHING_CONST    
        language_model[gram][language] += 1
        language_count[language] += 1

# convert_count_to_probability converts the count in the language model to a probability
def convert_count_to_probability():
    for cur_gram in language_model:
        cur_gram_dict = language_model[cur_gram]
        for language in cur_gram_dict:
            cur_gram_dict[language] = cur_gram_dict[language]/float(language_count[language])

# predict_language takes a line and a language model and predicts what language 
# this line is in
def predict_language(line, LM):
    new_language = compute_probabilities_for_all_languages(line.lower(), LM)
    return new_language + " " + line #TODO(@Anna) should use stringbuilder instead? 

# compute_probabilities_for_all_languages takes a line and a language model, and 
# computes the probability for all languages based on the LM
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

    if is_other_language(non_trained_gram_count, len(all_grams)):
        return "other"
    return get_largest_from_dict(probabilities)

# get_largest_from_dict retrieves the largest probability from the probabilities argument
def get_largest_from_dict(probabilities):
    highest_prob_language, highest_prob = "", float(-1)
    for langauge in probabilities:
        if probabilities[langauge] > highest_prob:
            highest_prob_language, highest_prob = langauge, probabilities[langauge]
    return highest_prob_language

# get_grams takes a string, returns all the n-gram in that string where the length of the gram 
# is specified by the GRAM_SIZE constant
def get_grams(data):
    grams = []
    for index, char in enumerate(data):
        grams.append(data[index:index + constants.GRAM_SIZE])
    return grams

# get_language_and_data takes a sentence, and returns the language of the string, 
# and the string to extract n-gram from
def get_language_and_data(line):
    space_index = line.index(' ')
    language = line[:space_index]
    data = line[space_index + 1:]
    return language, data

# is_other_language returns the percent of non-trained words in a sentence and determine if 
# is it a language that we did not train for
def is_other_language(non_trained_count, total_gram_count):
    val = (non_trained_count/float(total_gram_count))*100
    if val > constants.OTHER_LANGUAGE_GRAM_SENTENCE_PERCENTAGE:
        return True
    else:
        return False

# contains_gitis checks if the text contains string, if yes, short circuit and return true.
# Worse case O(n), but very unlikely to hit worse case everytime
def contains_digits(text):
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for char in text:
        if char in numbers:
            return True
    return False