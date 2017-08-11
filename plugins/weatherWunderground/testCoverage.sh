#!/bin/bash

py.test --verbose --cov=../weatherWunderground --cov-report= test.py
coverage report --show-missing
