## NorBERT with Simpletransformers
I had some problems with using NorBERT with sequence tagging last year, and decided to check the status now, as per January 2022. These is an issue open about the subject here: [https://github.com/ltgoslo/NorBERT/issues/1](https://github.com/ltgoslo/NorBERT/issues/1). 
I have now tried NorBERT and nb-BERT together with m-BERT in a quite minimal setup, doing sequence tagging on NoReC-fine. `['bert-base-multilingual-cased' , 'NbAiLab/nb-bert-base',  'ltgoslo/norbert' ]` 
Since [the issue](https://github.com/ltgoslo/NorBERT/issues/1) reported different behaviour on CPU and GPU, I tried both. For the CPU experiment I used a 400 sentences scaled-down training set, which is enough to get above zero evaluation results, but not much more. The task is Targeted Sentiment Analysis: Identify the the sentiment targets in each sentence.

### What I did
- Create a new Conda environment for CPU only according to the [simpletransformers installation page](https://simpletransformers.ai/docs/installation/)
- Create another Conda environment for GPU and cudatoolkit according to the [simpletransformers installation page](https://simpletransformers.ai/docs/installation/), with the exception that I have the 10.2 cudatoolkit. [conda install pytorch cudatoolkit=10.2 -c pytorch](https://pytorch.org/get-started/locally/)
- Run the [Experiments21_norec_fine_cpu.ipynb](Experiments21_norec_fine_cpu.ipynb) notebook in the CPU environment
- Run the [Experiments21_norec_fine_gpu.ipynb](Experiments21_norec_fine_gpu.ipynb) notebook in the GPU environment

### Results
**For the CPU experiment**, the output reported a running loss. NorBERT was the only model that evaluated to zero precision and recall, but a friend reran the experiment with more epochs and then NorBERT performed as expected. So NorBERT works fine in this setting.

For the GPU experiment, the loss was reported as NaN, using NorBERT.

See the two notebooks for more details.

### Conclution
As per today, 'NbAiLab/nb-bert-base' can be used in my Simpletransformers sequence tagging setup with Simpletransformers, but not 'ltgoslo/norbert'. 

### Bonus material
In the GPU notebook 
[Experiments21_norec_fine_gpu.ipynb](Experiments21_norec_fine_gpu.ipynb) you can find the inference for each model on three example sentences. It is interesting to see how m-bert almost gets it, while nb-bert arrives at some good labels for the sentiment targets.

```
transformer_model bert-base-multilingual-cased:
[{'Mannen': 'B-targ-negative'}, {'på': 'O'}, {'scenen': 'I-targ-negative'}, {'synger': 'O'}, {'stygt': 'O'}]
[{'Damen': 'B-targ-positive'}, {'på': 'I-targ-positive'}, {'scenen': 'I-targ-negative'}, {'synger': 'O'}, {'stygt': 'O'}]
[{'Disse': 'O'}, {'bilene': 'B-targ-positive'}, {'har': 'O'}, {'et': 'O'}, {'fantastisk': 'O'}, {'veigrep': 'O'}]


transformer_model NbAiLab/nb-bert-base:
[{'Mannen': 'B-targ-negative'}, {'på': 'O'}, {'scenen': 'O'}, {'synger': 'O'}, {'stygt': 'O'}]
[{'Damen': 'B-targ-negative'}, {'på': 'O'}, {'scenen': 'O'}, {'synger': 'O'}, {'stygt': 'O'}]
[{'Disse': 'B-targ-positive'}, {'bilene': 'I-targ-positive'}, {'har': 'O'}, {'et': 'O'}, {'fantastisk': 'O'}, {'veigrep': 'O'}]

```



