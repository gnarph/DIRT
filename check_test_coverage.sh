#!/bin/sh
python `which coverage` run --source=preprocessing,processing,models,utilities run_tests.py
coverage report -m
