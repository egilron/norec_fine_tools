#!/bin/bash

#SBATCH --job-name=TSA
#SBATCH --account=nn9851k
#SBATCH --mail-type=FAIL
#SBATCH --partition=accel
#SBATCH --gres=gpu:1
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=4

source ${HOME}/.bashrc

# sanity: exit on all errors and disallow unset environment variables
set -o errexit
set -o nounset

# the important bit: unload all current modules (just in case) and load only the necessary ones
module purge
module use -a /cluster/shared/nlpl/software/eb/etc/all/
module load nlpl-nlptools/2021.01-gomkl-2019b-Python-3.7.4
module load nlpl-gensim/3.8.3-gomkl-2019b-Python-3.7.4
module load sentencepiece/0.1.96-gomkl-2019b-Python-3.7.4
module load nlpl-wandb/0.12.6-gomkl-2019b-Python-3.7.4
module load nlpl-simpletransformers/0.61.13-gomkl-2019b-Python-3.7.4


# by default, pass on any remaining command-line options
python3 finetune_tsa.py ${@}