import pandas as pd
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib
from .textProcessor import Text_Processor



def init(model_file='./data/tags_SGDClassifier.pkl', multiLabelBin_file = './data/tags_multiLabelBin.pkl', ntags=5) :
    global predictionModel, multiLabelBinarizer, texpP, num_tags
    predictionModel = joblib.load(model_file)
    multiLabelBinarizer = joblib.load(multiLabelBin_file)
    num_tags = ntags
    texpP = Text_Processor()


def suggest_tags(title, body_text, body_code=''):
	text_data = texpP.getProcessedText(title, body_text, body_code)
	predictions = predictionModel.predict_proba([text_data])
	top_classes= np.argsort(-predictions)[:,:num_tags]
	tags_pred = multiLabelBinarizer.classes_[top_classes]
	return tags_pred.tolist()


'''
if __name__ == "__main__":
    title = 'Python def call function'
    body = 'How to run a python code'
    code = 'return re.sub(' +',' ',cleaned_text.strip())'
    init()
    print(suggest_tags(title,body,code ))
'''