

# %% [markdown]
# ### Spacy with neural coreference resolution
# Use the implementation from `https://github.com/tomasonjo/trinity-ie` 
# 
# - Grab my pre-existing translation of Norec-fine into English
# - Get the SpaCy pipeline and coref_resolution() from tomasonjo working
# - Save the results in a meaningful way, transfer it back from English to Norwegian
# - See how this can be used together with the wikifier
# 

# %%
import os
import itertools
import json
import spacy
import neuralcoref
import pandas as pd
from string import punctuation
import en_core_web_sm
nlp = en_core_web_sm.load()
neuralcoref.add_to_pipe(nlp)






# %%
# ! python -m spacy download en_core_web_sm

if __name__ == "__main__":
    # raw = ["Dean Martin was a lousy actor.", "He did not know how to behave on stage."]
    # raw = " ".join(raw)
    # raw = "Angela lives in Boston. She is quite happy in that city."
    # print(nlp(raw)._.coref_clusters)

    source_path = "data/norec_eng"
    for file_name in os.listdir(source_path):
        with open(os.path.join(source_path, file_name) ) as rf:
            text = rf.read()
        coref_cs = nlp(text)._.coref_clusters
        for coref_c in coref_cs:
            if "Mari" in coref_c.main.text:
                print(coref_c)




