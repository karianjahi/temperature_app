#!/bin/bash
coverage run -m pytest test.py -s
coverage html
pylint test.py
