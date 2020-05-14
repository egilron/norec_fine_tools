**A place to share tools that I have found useful when working with the Norwegian review corpus for fine-grained sentiment analysis.**  
[Norec Fine on github](https://github.com/ltgoslo/norec_fine)
### Reference the metadata for documents
The NoReC Norwegian Review Corpus is found [here.](https://github.com/ltgoslo/norec) When you follow the instructions and download tha data, you get the metadata for the text files. The entire NoReC is larger than norec-fine, but norec_fine has kept the 6-digit document id in their textfile names. NoReC can be used for document-level sentiment analysis, since it has a 1-6 rating for all documents. It also has the category for the review and language (Bokmål nb or nynorsk).

```
  "001392": {
    "authors": [
      "Jørgen Hegstad"
    ],
    "category": "music",
    "day": 5,
    "excerpt": "",
    "id": 1392,
    "language": "nb",
    "month": 5,
    "rating": 3,
    "source": "p3",
    "source-category": "musikk",
    "source-id": 39026,
    "source-tags": [],
    "split": "train",
    "tags": [],
    "title": "Halvhjertet helhet",
    "url": "http://p3.no/musikk/halvhjertet-helhet",
    "year": 2010
  },
```
When working with the norec_fine, I am interested in the category of the text, and I use the metadata.json from NoReC for that. The file, as retrieved May 2020 is in the repo [here](https://github.com/egilron/norec_fine_tools/.