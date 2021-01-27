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



