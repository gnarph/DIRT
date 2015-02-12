#!/bin/bash
python -m cProfile -o profile_output DIRT.py -i test_data_ignore -pre test_preprocessed/ig -gl 0 -ml 5 -o test_output/ig -l zhi -c simple
