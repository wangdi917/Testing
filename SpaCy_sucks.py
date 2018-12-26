from __future__ import division, print_function, unicode_literals

# pip install spacy
# python -m spacy download en
# pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz
# python -m spacy download en_core_web_md

# python -c "import os; path = os.sys.executable;folder=path[0 : path.rfind(os.sep)]; print (folder)"
# python -c "import spacy; print (spacy.__version__)"
# python -c "import os; import spacy; print(os.path.dirname(spacy.__file__))"
# python -c "import os; import en_core_web_sm; print(os.path.dirname(en_core_web_sm.__file__))"


import os
import spacy
NLP = spacy.load('en')											# load model with shortcut link "en"
NLP = spacy.load('en_core_web_sm')								# load model package "en_core_web_sm"
# NLP = spacy.load('/home/wangdi498/testing/en_core_web_sm')	# load package from a directory

import en_core_web_sm
NLP = en_core_web_sm.load()

# standard import:
from spacy.lang.xx import MultiLanguage
nlp = MultiLanguage()

# lazy import:
from spacy.util import get_lang_class
nlp = get_lang_class('xx')


def Tokenization():
	print ("\nThe outcomes of Tokenization are:")
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(u"Apple isn't looking at buying U.S.A. startup for $1 billion.")
	for token in doc:
		print ('\t', token.text)


def Tagging():
	print ("\nThe outcomes of Lemmatization and POS Tagging are:")
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(u"Apple isn't looking at buying U.S.A. startup for $1 billion.")
	for token in doc:
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop))

	print ("\n\tAs to the word 'Apple',")
	apple = doc[0]
	print('\tFine-grained POS tag:', apple.pos_, apple.pos)
	print('\tCoarse-grained POS tag:', apple.tag_, apple.tag)
	print('\tWord shape:', apple.shape_, apple.shape)
	print('\tAlphanumeric characters?', apple.is_alpha)
	print('\tPunctuation mark?', apple.is_punct)

	print ("\n\tAs to the word 'billion',")
	billion = doc[10]
	print('\tDigit?', billion.is_digit)
	print('\tLike a number?', billion.like_num)
	print('\tLike an email address?', billion.like_email)


def Entity():
	print ("\nThe outcomes of Entity Extraction are:")
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(u"Apple isn't looking at buying U.S.A. startup for $1 billion.")
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_))

	from spacy.tokens import Span
	doc = nlp(u"FB is hiring a new VP of global policy.")
	doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u'ORG'])]
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_))


def Similarity():
	print ("\nThe outcomes of Similarity are:")
	import en_core_web_md
	nlp = spacy.load('en_core_web_md') # This is a larger model including GloVe vectors.
	tokens = nlp(u"dog cat banana") # Similarity is determined by comparing word vectors or word embeddings.
	for token1 in tokens:
		for token2 in tokens:
			print ("\t{} <=> {} : {}".format(token1.text, token2.text, token1.similarity(token2)))


def Vectorization():
	print ("\nThe outcomes of Vectorization are:")
	import en_core_web_md
	nlp = spacy.load('en_core_web_md')
	tokens = nlp(u"dog cat banana fuck_spacy")
	for token in tokens:
		print ("\t{}\t{}\t{}\t{}".format(token.text, token.has_vector, token.vector_norm, token.is_oov))


def Lexemization():
	print ("\nThe outcomes of Lexemization are:")
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(u"I don't drink coffee.")
	for word in doc:
		lexeme = doc.vocab[word.text]
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(lexeme.text, lexeme.orth, lexeme.shape_, lexeme.prefix_, lexeme.suffix_, lexeme.is_alpha, lexeme.is_digit, lexeme.is_title, lexeme.lang_))
	# Hashes cannot be reversed and there's no way to resolve 3197928453018144401 back to "coffee".
	print ("The hash of 'coffee' is:", doc.vocab.strings[u'coffee'])
	print ("The instance of '3197928453018144401' is:", doc.vocab.strings[3197928453018144401])


def TrainUpdate():
	print ("\nThe outcomes of Training and Updating are:")
	import random
	nlp = spacy.load('en')
	# When you call nlp on a text, spaCy first tokenizes the text to produce a Doc object.
	# This Doc is then processed in several different steps which forms the pipeline ["tagger", "parser", "ner"].
	print ("When the pipeline is:", nlp.pipe_names)
	train_data = [ ("Uber blew through $1 million.", {'entities': [(0, 4, 'ORG')]}), ("I love Lacy.", {'entities': [(7, 10, 'PERSON')]}), ("I come from U.S.A.", {'entities': [(12, 17, 'GPE')]})]
	with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != 'ner']):
		optimizer = nlp.begin_training()
		for i in range(10):
			random.shuffle(train_data)
			for text, annotations in train_data:
				nlp.update([text], [annotations], sgd=optimizer)
	nlp.to_disk("/home/wangdi498/SpaCy/models")


def DependencyParsing():
	print ("\nThe outcomes of Dependency Parsing are:")
	from spacy import displacy
	doc_dep = nlp(u"This is a sentence.")
	displacy.serve(doc_dep, style='dep')
	doc_ent = nlp(u"When Sebastian Thrun started working on self-driving cars at Google "
				  u"in 2007, few people outside of the company took him seriously.")
	displacy.serve(doc_ent, style='ent')


def SyntacticParsing():
	print ("\nThe outcomes of Syntactic Parsing are:")
	doc = nlp(u"When Sebastian Thrun started working on self-driving cars at Google "
			  u"in 2007, few people outside of the company took him seriously.")
	dep_labels = []
	for token in doc:
		while token.head != token:
			dep_labels.append(token.dep_)
			token = token.head
	print ('\t', dep_labels)


def Pipeline():
	print ("\nThe outcomes of Piping are:")
	lang = 'en'
	pipeline = ['tagger', 'parser', 'ner']
	data_path = "/home/wangdi498/anaconda3/envs/rasa/lib/python3.6/site-packages/en_core_web_sm/en_core_web_sm-2.0.0/"
	cls = spacy.util.get_lang_class(lang)
	nlp = cls()
	for name in pipeline:
		component = nlp.create_pipe(name) # Create the pipeline components.
		nlp.add_pipe(component) # Add the component to the pipeline.
		print ("When the component is:", component)
	nlp.from_disk(data_path)



### $$$ %%% ===

if __name__ == "__main__":
	print ("\nHere we go...\n")
	Tokenization()
	Tagging()
	Entity()
	Similarity()
	Vectorization()
	Lexemization()
	TrainUpdate()
	# DependencyParsing()
	# SyntacticParsing()
	Pipeline()
	print ("\nDone!\n")