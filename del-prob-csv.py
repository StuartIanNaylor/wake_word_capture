#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prob_file', default='./prob-del.txt', help='Sample file prob results default=./prob.txt')
args = parser.parse_args()

Probs = open(args.prob_file, 'r')
while True:
  Prob = Probs.readline()
  if Prob:
    file_path = Prob.split(",")[0]
    #print(file_path)
    #break
    try:
      os.remove(file_path)
      print(f"File '{file_path}' deleted successfully.")

    except FileNotFoundError:
      print(f"File '{file_path}' not found.")
  else:
    break

