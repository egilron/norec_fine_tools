import os
import pandas as pd
import json
import urllib
import urllib.request

# Grab the Norec_fine training data from https://github.com/ltgoslo/norec_fine
source_path = "data/norec_fine_json/train.json"
with open (source_path) as rf:
    data = json.load(rf)
write_stem = "data/n_fine_entities_" # Add to this when saving wikified results


## Copied from https://github.com/tomasonjo/trinity-ie
ENTITY_TYPES = ["human", "person", "company", "enterprise", "business", "geographic region",
                "human settlement", "geographic entity", "territorial entity type", "organization"]

## Copied from https://github.com/tomasonjo/trinity-ie
def wikifier(text, lang="en", threshold=0.8):
    """Function that fetches entity linking results from wikifier.com API"""
    # Prepare the URL.
    data = urllib.parse.urlencode([
        ("text", text), ("lang", lang),
        ("userKey", "tgbdmkpmkluegqfbawcwjywieevmza"),
        ("pageRankSqThreshold", "%g" %
         threshold), ("applyPageRankSqThreshold", "true"),
        ("nTopDfValuesToIgnore", "100"), ("nWordsToIgnoreFromList", "100"),
        ("wikiDataClasses", "true"), ("wikiDataClassIds", "false"),
        ("support", "true"), ("ranges", "false"), ("minLinkFrequency", "2"),
        ("includeCosines", "false"), ("maxMentionEntropy", "3")
    ])
    url = "http://www.wikifier.org/annotate-article"
    # Call the Wikifier and read the response.
    req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
    with urllib.request.urlopen(req, timeout=60) as f:
        response = f.read()
        response = json.loads(response.decode("utf8"))
    # Output the annotations.
    results = list()
    for annotation in response["annotations"]:
        # Filter out desired entity classes
        if ('wikiDataClasses' in annotation) and (any([el['enLabel'] in ENTITY_TYPES for el in annotation['wikiDataClasses']])):

            # Specify entity label
            if any([el['enLabel'] in ["human", "person"] for el in annotation['wikiDataClasses']]):
                label = 'Person'
            elif any([el['enLabel'] in ["company", "enterprise", "business", "organization"] for el in annotation['wikiDataClasses']]):
                label = 'Organization'
            elif any([el['enLabel'] in ["geographic region", "human settlement", "geographic entity", "territorial entity type"] for el in annotation['wikiDataClasses']]):
                label = 'Location'
            else:
                label = None

            results.append({'title': annotation['title'], 'wikiId': annotation['wikiDataItemId'],'url': annotation['url'], 'label': label,
                            'characters': [(el['chFrom'], el['chTo']) for el in annotation['support']]})
    return results



target = "mari"
# target = "peter"
json_cache = write_stem+target+".json"
if os.path.exists(json_cache):
    with open(json_cache) as rf:
        entities_list = json.load(rf)
else:
    entities_list = list()
    for i, sent in enumerate(data):
        if target in sent['text'].lower():
            entities = wikifier(sent['text'], threshold=0.8, lang='nb')
            entities_list.extend(
                [{'title': el['title'], 'wikiId': el['wikiId'], 'url': el['url'], 'label': el['label'], 'text':sent['text'], 'sent_id':sent['sent_id']} for el in entities])
    with open(json_cache, "w") as wf:
        json.dump(entities_list, wf, ensure_ascii=False)

target_entities = [e for e in entities_list if target in e['title'].lower() and e['label'] == "Person"]
targets_arranged = {} 
for te in target_entities:
    if te['wikiId'] in targets_arranged:
        targets_arranged[te['wikiId']]['sent_ids'].append(te['sent_id'])
        targets_arranged[te['wikiId']]['texts'].append(te['text'])
    else:
        targets_arranged[te['wikiId']] = te.copy()
        targets_arranged[te['wikiId']]['sent_ids']= [te['sent_id']]
        targets_arranged[te['wikiId']]['texts']= [te['text']]
        del targets_arranged[te['wikiId']]['sent_id']
        del targets_arranged[te['wikiId']]['text']




# print(targets_arranged)
targets_printlist = sorted([(te['title'], te)  for key, te in targets_arranged.items()])
print(f"\nIndividuals found in the training set, containing '{target}':")

for title , info in targets_printlist:
    print(f"\nMentions of {title} in the training set, according to Wikifier:")
    print(f"Web page: {info['url']}")
    for text in info['texts']:
        print(text)

# %%
