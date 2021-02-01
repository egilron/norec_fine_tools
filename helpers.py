<<<<<<< HEAD
import random
import os
# from simpletransformers.ner import NERModel
def tagsset(textfile, separator = "\t"):
    '''
    Finds all tags and returns them as set
    '''
    tags = set()
    for sent in textfile.split("\n\n"):
        for line in sent.split("\n"):
            if separator in line:
                tags.update([line.strip().split(separator)[-1]]) 
    return tags

def convert(textfile, separator = "\t"):
    '''
    Takes in the entire text file, converts to space separated, strips the commented text
    '''
    cleansents = []
    for sent in textfile.split("\n\n"):
        cleanlines = []
        for line in sent.split("\n"):
            if separator in line:
                assert " " not in line
                cleanlines.append(line.strip().replace("\t", " "))
        cleansents.append("\n".join(cleanlines))
    return "\n\n".join(cleansents)
            
def nopol(textfile, separator = " "): #Deprecated, use filter_tags
    '''
    Removes the last part of the tag which should be the polarity.
    'I-targ-Negative', 'B-targ-Positive', 'I-targ-Positive', 'B-targ-Negative
    becomes
    'I-targ', 'B-targ', 'I-targ', 'B-targ'
    '''
    cleansents = []
    for sent in textfile.split("\n\n"):
        cleanlines = []
        for line in sent.split("\n"):
            if separator in line and "-" in line:
                cleanlines.append("-".join(line.strip().split("-")[:-1]))
            else:
                cleanlines.append(line.strip())
        cleansents.append("\n".join(cleanlines))
    return "\n\n".join(cleansents)
                


def filter_tags(textfile, filter_rule, separator = " "):
    '''
    Applies the filter_rule on those tags in the dict.
    FIlter_rule can be breated like this:
    unwanted = ['I-targ-conflict', 'B-targ-conflict','B-targ-neutral', 'I-targ-neutral']
    filter_rule = {t:"O" for t in unwanted}
    '''
    cleansents = []
    for sent in textfile.split("\n\n"):
        cleanlines = []
        for line in sent.split("\n"):
            if separator in line:
                token, tag = line.split(separator)
                if tag in filter_rule:
                    tag = filter_rule[tag]
                line = separator.join([token,tag])
            cleanlines.append(line)
        cleansents.append("\n".join(cleanlines))
    return "\n\n".join(cleansents)

def scale(textfile, return_len, separator = " "):
    '''
    return the amount of sentences according to training_samples
    '''
    sents = textfile.split("\n\n")
    orig_len = len(sents)
        # Sample the required amount, and return sentences in same order
    sampled_ids = sorted(random.sample(range(orig_len+1), return_len)) 
    return_text = "\n\n".join([s for i,s in enumerate(sents) if i in sampled_ids])
    return_len = len(return_text.split('\n\n')) # Monitor for errors
    print(f"Scaling training data. Returning {return_len} sentences")
    return return_text

# def one_round(args, out_dir, labels = [ ],train_data = ' ', test_data = ' '):
#      model = NERModel(args['model_type'], args['model_name'], labels = labels, args=args)
#      # Train the model
#      model.train_model(train_data, output_dir= out_dir)
#      # Evaluate the model
#      return model.eval_model(test_data)

def entity_lengths(textfile, separator=" "):
    '''Returns a list of lengths of entities, that is BI-sequences'''
    list_of_lengths = []
    length_this = None
    for sent in textfile.split("\n\n"):
        for line in sent.split("\n"):
            if separator in line:
                token, tag = line.split(separator)
                if tag.startswith("B-"):
                    length_this = 1
                if tag.startswith("I-"):
                    length_this += 1
                if tag.startswith("O") and length_this is not None:
                    list_of_lengths.append(length_this)
                    length_this = None
        #Catch entity if I was last tag
        if length_this is not None:
                list_of_lengths.append(length_this)
                length_this = None
    return list_of_lengths     
                    

def no_en_conll(dfx):
    '''
    Takes a dataframe with NO and en text and tags
    return a text for the NOrwegian and a text for the ENglish, ready to be saved as a conll file
    '''
    no_lines = []
    en_lines = []
    for idx, row in dfx.iterrows():
        no_line = [token+" "+tag for token, tag in zip(row['no_text'].split(" "), row['no_tags'].split(" "))]
        no_lines.append("\n".join(no_line))
        en_line = [token+" "+tag for token, tag in zip(row['en_tokenized'].split(" "), row['en_tags'].split(" "))]
        en_lines.append("\n".join(en_line))
    return ( "\n\n".join(no_lines), "\n\n".join(en_lines))


def dataset_w_tags(train: str, dev: str):
    '''
    Input: paths to train and dev/test
    Extraxts the tags from train, checks that the dev file
    has the same tags. Returns the train, dev, tags tuple
    '''
    with open(train) as rf:
        tags = tagsset(rf.read(), separator = " ")
        assert len(tags) > 1, "Train tags not detected"

    with open(dev) as rf:
        dev_tags = tagsset(rf.read(), separator = " ")
        assert len(dev_tags) > 1, "Dev tags not detected"
        assert dev_tags <= tags, " Train and dev have different tagsets"

    return (train, dev, list(tags))

def epoch_results(parent: str):
    '''
    Input: path to parent folder that contains 
    folders for each epoch evaluation with simpletransformers
    returns a dataframe with all experiments

    '''
    results = {}
    for p in os.walk(parent):
        if "-epoch-" in p[0] and 'eval_results.txt' in p[2]:
            with open(os.path.join(p[0], 'eval_results.txt' )) as rf:
                result = {}
                for line in rf.read().strip().split("\n"):
                    key, value = line.strip().split(" = ")
                    result[key.strip()] = float(value.strip())

                results[int(p[0].split("epoch-")[1])] = result

    return results

if __name__ == "__main__":
    ps = epoch_results("/media/egil/Data/prosjekter/WNNLP-2019/outputs/bert-base-multilingual-cased_1558")
    for i in range(1, len(ps)+1):
        print(i)
        print(ps[i])
=======
import random
# from simpletransformers.ner import NERModel
def tagsset(textfile, separator = "\t"):
    '''
    Finds all tags and returns them as set
    '''
    tags = set()
    for sent in textfile.split("\n\n"):
        for line in sent.split("\n"):
            if separator in line:
                tags.update([line.strip().split(separator)[-1]]) 
    return tags

def convert(textfile, separator = "\t"):
    '''
    Takes in the entire text file, converts to space separated, strips the commented text
    '''
    cleansents = []
    for sent in textfile.split("\n\n"):
        cleanlines = []
        for line in sent.split("\n"):
            if separator in line:
                assert " " not in line
                cleanlines.append(line.strip().replace("\t", " "))
        cleansents.append("\n".join(cleanlines))
    return "\n\n".join(cleansents)
            
def nopol(textfile, separator = " "): #Deprecated, use filter_tags
    '''
    Removes the last part of the tag which should be the polarity.
    'I-targ-Negative', 'B-targ-Positive', 'I-targ-Positive', 'B-targ-Negative
    becomes
    'I-targ', 'B-targ', 'I-targ', 'B-targ'
    '''
    cleansents = []
    for sent in textfile.split("\n\n"):
        cleanlines = []
        for line in sent.split("\n"):
            if separator in line and "-" in line:
                cleanlines.append("-".join(line.strip().split("-")[:-1]))
            else:
                cleanlines.append(line.strip())
        cleansents.append("\n".join(cleanlines))
    return "\n\n".join(cleansents)
                


def filter_tags(textfile, filter_rule, separator = " "):
    '''
    Applies the filter_rule on those tags in the dict.
    FIlter_rule can be breated like this:
    unwanted = ['I-targ-conflict', 'B-targ-conflict','B-targ-neutral', 'I-targ-neutral']
    filter_rule = {t:"O" for t in unwanted}
    '''
    cleansents = []
    for sent in textfile.split("\n\n"):
        cleanlines = []
        for line in sent.split("\n"):
            if separator in line:
                token, tag = line.split(separator)
                if tag in filter_rule:
                    tag = filter_rule[tag]
                line = separator.join([token,tag])
            cleanlines.append(line)
        cleansents.append("\n".join(cleanlines))
    return "\n\n".join(cleansents)

def scale(textfile, return_len, separator = " "):
    '''
    return the amount of sentences according to training_samples
    '''
    sents = textfile.split("\n\n")
    orig_len = len(sents)
        # Sample the required amount, and return sentences in same order
    sampled_ids = sorted(random.sample(range(orig_len+1), return_len)) 
    return_text = "\n\n".join([s for i,s in enumerate(sents) if i in sampled_ids])
    return_len = len(return_text.split('\n\n')) # Monitor for errors
    print(f"Scaling training data. Returning {return_len} sentences")
    return return_text

# def one_round(args, out_dir, labels = [ ],train_data = ' ', test_data = ' '):
#      model = NERModel(args['model_type'], args['model_name'], labels = labels, args=args)
#      # Train the model
#      model.train_model(train_data, output_dir= out_dir)
#      # Evaluate the model
#      return model.eval_model(test_data)

def entity_lengths(textfile, separator=" "):
    '''Returns a list of lengths of entities, that is BI-sequences'''
    list_of_lengths = []
    length_this = None
    for sent in textfile.split("\n\n"):
        for line in sent.split("\n"):
            if separator in line:
                token, tag = line.split(separator)
                if tag.startswith("B-"):
                    length_this = 1
                if tag.startswith("I-"):
                    length_this += 1
                if tag.startswith("O") and length_this is not None:
                    list_of_lengths.append(length_this)
                    length_this = None
        #Catch entity if I was last tag
        if length_this is not None:
                list_of_lengths.append(length_this)
                length_this = None
    return list_of_lengths     
                    

def no_en_conll(dfx):
    '''
    Takes a dataframe with NO and en text and tags
    return a text for the NOrwegian and a text for the ENglish, ready to be saved as a conll file
    '''
    no_lines = []
    en_lines = []
    for idx, row in dfx.iterrows():
        no_line = [token+" "+tag for token, tag in zip(row['no_text'].split(" "), row['no_tags'].split(" "))]
        no_lines.append("\n".join(no_line))
        en_line = [token+" "+tag for token, tag in zip(row['en_tokenized'].split(" "), row['en_tags'].split(" "))]
        en_lines.append("\n".join(en_line))
    return ( "\n\n".join(no_lines), "\n\n".join(en_lines))



>>>>>>> 9102ebed5087873ab68b69784cdceb87b1d6e819
