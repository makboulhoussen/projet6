import unicodedata
import re
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.toktok import ToktokTokenizer
from .contractions import CONTRACTION_MAP

class Text_Processor :

	def __init__(self):
		self.stopword_list = set(stopwords.words('english'))
		self.tokenizer = ToktokTokenizer()

	'''
	Méthode qui permet de mettre les contractions dans une forme classique.
	Méthode récupéré depuis github : (c) @dipanjanS
	'''
	def _expand_contractions(self, text, contraction_mapping=CONTRACTION_MAP):
	    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
	                                      flags=re.IGNORECASE|re.DOTALL)
	    def expand_match(contraction):
	        match = contraction.group(0)
	        first_char = match[0]
	        expanded_contraction = contraction_mapping.get(match)\
	                                if contraction_mapping.get(match)\
	                                else contraction_mapping.get(match.lower())                       
	        expanded_contraction = first_char+expanded_contraction[1:]
	        return expanded_contraction
	        
	    expanded_text = contractions_pattern.sub(expand_match, text)
	    expanded_text = re.sub("'", "", expanded_text)
	    return expanded_text


	def _getCleanedText(self, text) :
	    # remove accented char
	    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
	    text = self._expand_contractions(text)
	   
	    # remove non alpha char
	    text = re.sub('[\W\d_]', ' ', text)
	   
	    # convert to lower case
	    text = text.lower()
	   
	    #remove extra newlines
	    text = re.sub(r'[\r|\n|\r\n]+', ' ',text) 
	   
	    # remove extra whitespace
	    text = re.sub(' +', ' ', text)
	   
	    # Remove any single letter except 'c' (correspond au langage)
	    text = ' '.join( [w for w in text.split() if len(w)>1 or w == 'c'] )
	   
	    # remove stopwords
	    tokens = self.tokenizer.tokenize(text)
	    tokens = [token.strip() for token in tokens]
	    meaningful_words = [token for token in tokens if token not in self.stopword_list]
	   
	    # stemming of words
	    porter = PorterStemmer()
	    stemmed = [porter.stem(word) for word in meaningful_words]
	   
	    # join the words back into one string separated by space, 
	    # and return the result.
	    return( " ".join( stemmed ))

	'''
	Retrieve the code text inside the body
	'''
	def _getCleanedBodyCode(self, body) :
		table = str.maketrans('', '', string.punctuation)
		words = re.findall(r"[^\W\d_']+", body.lower())
		stripped = [w.translate(table) for w in words]
		return( " ".join( stripped ))


	def getProcessedText(self, title, body_text, body_code) :
		processed_text = self._getCleanedText(title)
		processed_text = processed_text + ' ' + self._getCleanedText(body_text)
		if body_code :
			processed_text = processed_text + ' ' + self._getCleanedBodyCode(body_code)
		return processed_text 

