from flask import Flask
from .app import app
from . import tagsSuggestion
import logging as lg

## VARIABLES
model_file='./data/tags_SGDClassifier.pkl'
multiLabelBin_file = './data/tags_multiLabelBin.pkl'
number_tags = 5


log = lg.getLogger('werkzeug')
#log.setLevel(lg.DEBUG)

tagsSuggestion.init(model_file, multiLabelBin_file, number_tags)
   