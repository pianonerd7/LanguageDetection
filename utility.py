
language_models = dict()

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


        if cur_4_gram in language_model:
            switch(language):
                case "indonesian":
                    language_model[cur_4_gram][0] = language_model[cur_4_gram][0] + 1
                    #language_model.update({cur_4_gram:})
                    break
                case "malaysian":
                    language_model[cur_4_gram][1] = language_model[cur_4_gram][1] + 1
                    break
                case "tamil":
                    language_model[cur_4_gram][2] = language_model[cur_4_gram][2] + 1
                    break
        else:
            language_model[cur_4_gram] = 

        print cur_4_gram
        if index == len(data) -4:
            break

str = "hello world, this is a sample string that has no actual content"
process_training_line(str)