from __future__ import division, print_function, unicode_literals

# 安装模型
# pip install zh_core_web_sm-2.0.5.tar.gz
# 再为这个模型建立一个链接
# spacy link zh_core_web_sm zh
# 😂

# python -c "import os; path = os.sys.executable;folder=path[0 : path.rfind(os.sep)]; print (folder)"
# python -c "import spacy; print (spacy.__version__)"
# python -c "import os; import spacy; print(os.path.dirname(spacy.__file__))"
# python -c "import os; import zh_core_web_sm; print(os.path.dirname(zh_core_web_sm.__file__))"
# python -m spacy init-model zh /tmp/cc_zh_300_vec --vectors-loc cc.zh.300.vec.gz


import os, re, plac, random, json, time
import spacy
# nlp对象要被用来创建文档，访问语言注释和不同的NLP属性。我们通过加载一个文本文件来创建一个document。
# document = open(filename).read()
# doc = nlp(document)

from spacy import displacy
try:
	import zh_core_web_sm
	nlp = zh_core_web_sm.load()
	Loading_Path = "/home/wangdi498/anaconda3/envs/rasa/lib/python3.6/site-packages/zh_core_web_sm/zh_core_web_sm-2.0.5/"
	print ("\nInfo: The zh_core_web_sm module can be loaded.\n")
except (ModuleNotFoundError, IOError):
	print ("\nWarning! The zh_core_web_sm module cannot be loaded! Consequently BIO tagging, NER, word2vec, hashing, and parsing will not be launched either!\n")
	from spacy.lang.zh import Chinese
	nlp = Chinese()
	Loading_Path = "/home/wangdi498/anaconda3/envs/rasa/lib/python3.6/site-packages/en_core_web_sm/en_core_web_sm-2.0.0/"
except:
	print ("\nError! Neither the en_core_web_sm nor the zh_core_web_sm module can be loaded!\n")

# 因为zn_core_web_sm已经错误地指定了如何分词，所以只能强行让jieba加载自定义字典。频率越高，成词的概率就越大。
# https://github.com/fxsjy/jieba/issues/14
import jieba
customized_jieba_dict = "/home/wangdi498/SpaCy/customized_jieba_dict.txt"
jieba.load_userdict(customized_jieba_dict)


# Token是词或标点，所以其属性有attributes、tags、dependencies等等。 Lexeme是word type，没有内容，所以其属性有shape、stop、flags等等。
# Doc是一些Token的序列，Vocab是一些Lexeme的序列，Span是Doc的一个slice，StringStore是把hash值映射成字符串的字典。 所以遍历doc得到token，遍历vocab得到lexeme，lexeme=doc.vocab[token.text]。
# 如果Doc是nlp(u"2018年9月27日")，那么Span(doc,0,1)=''，Span(doc,0,2)='2018'，Span(doc,0,3)='2018年'……



def Tokenization():
	# .pos_包括： NOUN、 VERB、 PRON、 PROPN、 ADJ、 ADV、 ADP、 DET、 CCONJ、 SPACE、 PART、 SYM、 NUM、 X、 INTJ……
	# .tag_包括： NN、 NNS、 VBP、 JJ、 JJR、 PRP、 DT、 IN……
	# 其他判别包括：is_alpha、is_punct、is_digit、like_num、like_email……
	print ("\nThe outcomes of Tokenization are:")
	doc = nlp(u"京东CEO刘强东在美国明尼苏达涉嫌性侵女大学生。")
	for token in doc:
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(token.text, token.lemma_, token.ent_iob, token.ent_iob_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)) # B=3, I=1, O=2, 中文没有I。
	# NLV = spacy.load("/tmp/cc_zh_300_vec")
	# doc = NLV(u"京东CEO刘强东在美国明尼苏达涉嫌性侵女大学生。")
	# for token in doc:
	# 	print ('\t', token.text)


def Tagging():
	print ("\nThe outcomes of Tagging are:")
	from spacy.symbols import ORTH, LEMMA, POS, TAG
	NLU = spacy.load('en_core_web_sm', parser=False, entity=False)
	# 如果load了en_core_web_sm，那么只能用add_special_case指定分词，因为en_core_web_sm无法做中文分词。
	# 如果load了zh_core_web_sm，那么add_special_case无效，因为zn_core_web_sm已经错误地指定了如何分词。
	special_case1 = [{ORTH: u'大', LEMMA: u'大', POS: u'ADJ'}, {ORTH: u'学生', LEMMA: u'生', POS: u'NOUN'}]
	NLU.tokenizer.add_special_case(u'大学生', special_case1)
	for shit in NLU(u"大学生"):
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shit.text, shit.lemma_, shit.pos_, shit.tag_, shit.dep_, shit.shape_, shit.is_alpha, shit.is_stop))
	special_case2 = [{ORTH: u'刘强东', LEMMA: u'刘强东', POS: u'PROPN'}, {ORTH: u'刘强东！', LEMMA: u'刘强东', POS: u'PROPN'}]
	NLU.tokenizer.add_special_case(u'刘强东', [{ORTH: u'刘强东'}])
	for shit in NLU(u"OMG刘强东"):
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shit.text, shit.lemma_, shit.pos_, shit.tag_, shit.dep_, shit.shape_, shit.is_alpha, shit.is_stop))

	from spacy.vocab import Vocab
	vocab = Vocab(strings=[u'刘强东'])
	from spacy.attrs import LEMMA
	print ("\nFuck!!! Tokenization has screwed up Tagging!")
	sentence = "是刘强东害了刘强东自己！"
	indexes = [p.span() for p in re.finditer('刘强东', sentence, flags=re.IGNORECASE)] # '刘强东\w+'
	doc = nlp(sentence)
	print ("The indexes are: {}.".format(indexes))
	for start, end in indexes:
		doc.merge(start_idx=start, end_idx=end)
	for shit in doc:
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shit.text, shit.lemma_, shit.pos_, shit.tag_, shit.dep_, shit.shape_, shit.is_alpha, shit.is_stop))

	# 由于zh_core_web_sm本身的分词错误，一旦调用nlp就会触发pipeline、就会错误地分词，所以后面不论怎样重新组词都只能基于错误的分词上！
	doc = nlp("是刘强东害了刘强东自己！")
	span = doc[1:4]
	with doc.retokenize() as retokenizer:
		retokenizer.merge(span, attrs={LEMMA: doc.vocab.strings[span.text]})
	for shit in doc:
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shit.text, shit.lemma_, shit.pos_, shit.tag_, shit.dep_, shit.shape_, shit.is_alpha, shit.is_stop))

	# 由于zh_core_web_sm本身的分词错误，一旦调用nlp就会触发pipeline、就会错误地分词，所以后面不论怎样重新组词都只能基于错误的分词上！
	doc = nlp("是刘强东害了刘强东自己！")
	span = doc[1:4]
	lemma_id = doc.vocab.strings[span.text] # 用ID来代表字符串：string_id = nlp.vocab.strings[string]
	span.merge(lemma=lemma_id)
	for shit in doc:
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(shit.text, shit.lemma_, shit.pos_, shit.tag_, shit.dep_, shit.shape_, shit.is_alpha, shit.is_stop))


def Hashing():
	print ("\nThe outcomes of Hashing are:")
	doc = nlp(u"京东CEO刘强东在美国明尼苏达涉嫌性侵女大学生。")
	apple = nlp.vocab.strings['apple'] # 用ID来代表字符串：string_id = nlp.vocab.strings[string]
	try:
		assert nlp.vocab[apple] == nlp.vocab[u'apple'], "\nError! This word cannot be hashed!"
		print ("Info, the vocabulary can correspond to the ID %d." %apple)
	except:
		print ("Error! The vocabulary cannot correspond to the ID %d!" %apple)
	for word in doc:
		lexeme = doc.vocab[word.text]
		print ("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(lexeme.text, lexeme.orth, lexeme.shape_, lexeme.prefix_, lexeme.suffix_, lexeme.is_alpha, lexeme.is_digit, lexeme.is_title, lexeme.lang_))
	# word.orth_和word.text是等效的。ORTH表示token的verbatim值，orth_本质上是用__get__方法调用self.vocab.strings[self.c.lex.orth]。
	# Hashes值不能被恢复成原词。
	print ("The hash of '性侵' is:", doc.vocab.strings[u'性侵'])
	print ("The hash of 'CEO' is:", doc.vocab.strings[u'CEO'])
	# print ("The instance of '8011747669617544689' is:", doc.vocab.strings[8011747669617544689])


def Entity():
	print ("\nThe outcomes of Entity Extraction are:")
	doc = nlp(u"京东CEO刘强东在美国明尼苏达涉嫌性侵女大学生。")
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))

	from spacy.tokens import Span
	doc = nlp(u"奶茶妹妹遇见VP就有90%的几率1位出道……")
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))
	augment = [Span(doc, 0, 1, label=doc.vocab.strings[u'WORK_OF_ART'])]
	doc.ents = list(doc.ents) + augment
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))


def Vectorization1():
	print ("\nThe outcomes of Vectorization1 are:")
	tokens = nlp(u"京东刘强东在某个据说的时间和一个传说的地点遇见奶茶妹妹。")
	for token in tokens:
		print ("\t{}\t{}\t{}\t{}".format(token.text, token.has_vector, token.vector_norm, token.is_oov))
		if token.text == '奶茶':
			print ("\tThe contents of token '{}' is {} with length {}.".format(token.text, token.vector, token.vector.size))
def Vectorization2():
	print ("\nThe outcomes of Vectorization2 are:")
	# python -m spacy init-model zh /tmp/cc_zh_300_vec --vectors-loc cc.zh.300.vec.gz
	# nlp.vocab.vectors.from_glove('...')
	NLV = spacy.load("/tmp/cc_zh_300_vec")
	tokens = NLV(u"京东刘强东在某个据说的时间和一个传说的地点遇见奶茶妹妹。")
	for token in tokens:
		print ("\t{}\t{}\t{}\t{}".format(token.text, token.has_vector, token.vector_norm, token.is_oov))
		if token.text == '奶茶':
			print ("\tThe contents of token '{}' is {} with length {}.".format(token.text, token.vector, token.vector.size))


def Similarity1():
	print ("\nThe outcomes of Similarity1 are:")
	tokens = nlp(u"哥哥妹妹男人女人码农春夏秋冬季节我你他") # Similarity是比较词嵌入或词向量的结果。
	for token1 in tokens:
		for token2 in tokens:
			print ("\t{} <=> {} : {}".format(token1.text, token2.text, token1.similarity(token2)))
def Similarity2():
	print ("\nThe outcomes of Similarity2 are:")
	NLV = spacy.load("/tmp/cc_zh_300_vec")
	tokens = NLV(u"哥哥妹妹男人女人码农春夏秋冬季节我你他") # Similarity是比较词嵌入或词向量的结果。
	for token1 in tokens:
		for token2 in tokens:
			print ("\t{} <=> {} : {}".format(token1.text, token2.text, token1.similarity(token2)))


def Stop():
	print ("\nThe outcomes of Stop Words are:")
	from spacy.lang.en.stop_words import STOP_WORDS
	# print (STOP_WORDS)
	STOP_WORDS.add("your_additional_stop_word_here")
	for word in STOP_WORDS:
		lexeme = nlp.vocab[word]
		lexeme.is_stop = True
		# print (lexeme.text)

	nlp.Defaults.stop_words |= {"了", "啊", "吧", "嗯"} # 单个词可以直接.add()
	nlp.Defaults.stop_words -= {"嗯"} # 单个词可以直接.remove()
	for word in nlp.Defaults.stop_words:
		lexeme = nlp.vocab[word]
		lexeme.is_stop = True
		# print (lexeme.text)
	print (nlp.Defaults.stop_words)


def Parsing():
	print ("\nThe outcomes of Parsing are:")

	# 中文无法直接分句！
	paragraph = nlp(u"京东CEO刘强东, 在美国明尼苏达，涉嫌性侵女大学生. 奶茶妹妹。遇见VP就有90%的几率1位出道……")
	for sent in paragraph.sents:
		print("\t{}".format(sent.text))

	# 自定义中文分句。
	from spacy.pipeline import SentenceSegmenter
	def split_on_punctuation(doc):
		start = 0
		whether_segmenter = False
		for word in doc:
			if whether_segmenter and not word.is_space:
				yield doc[start:word.i]
				start = word.i
				whether_segmenter = False
			elif word.text in ",.:;?!，。：；？！":
				whether_segmenter = True
		if start < len(doc):
			yield doc[start:len(doc)]
	punctuation = re.compile(r",.:;?!，。：；？！")
	SS = SentenceSegmenter(nlp.vocab, strategy=split_on_punctuation)
	nlp.add_pipe(SS)
	paragraph = nlp(u"京东CEO刘强东, 在美国明尼苏达，涉嫌性侵女大学生. 奶茶妹妹……遇见VP就有90%的几率1位出道。")
	for sent in paragraph.sents:
		print("\t{}".format(sent.text))

	print ("\n")
	sentence = nlp("京东CEO刘强东在美国明尼苏达涉嫌性侵女大学生。")
	for word in sentence:
		print("\t{}: {}".format(word, str(list(word.children))))


def Serialization():
	print ("\nThe outcomes of Serialization are:")
	try:
		text = open("/home/wangdi498/SpaCy/diary2.txt", 'r').read() # 'r'会按编码格式进行解析，read()返回的是str；'rb'：会按二进制进行解析，read()返回的是bytes。
		print ("\nInfo: The Serialization file can be read.\n")
	except FileNotFoundError:
		print ("\nError! The Serialization file cannot be read!\n")
		sys.exit(0) # os._exit()会直接将python程序终止，之后的所有代码都不会继续执行。
	except:
		print ("\nError! The .txt file must be UTF-8 encoded format!\n")
	doc = nlp(text)
	doc.to_disk("/home/wangdi498/SpaCy/diary1.bin")

	from spacy.tokens import Doc
	from spacy.vocab import Vocab
	doc = Doc(Vocab()).from_disk("/home/wangdi498/SpaCy/diary1.bin")
	print ("The texts are:\n{}".format(doc))
	
	from spacy.tokens import Span
	doc = nlp(text)
	print ("\nThe 1st round of Save and Load is:")
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))
	assert len(doc.ents) != 0, "\nError! This document cannot be empty!" # 防止Doc为空。
	augment = [Span(doc, 0, 2, label=doc.vocab.strings[u'EVENT'])]
	doc.ents = list(doc.ents) + augment
	doc.to_disk("/home/wangdi498/SpaCy/diary2.bin")
	print ("\nThe 2nd round of Save and Load is:")
	for ent in doc.ents:
		print ("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))

	paragraph = Doc(Vocab()).from_disk("/home/wangdi498/SpaCy/diary2.bin")
	assert len(paragraph.ents) != 0, "\nError! This document cannot be empty!" # 防止Doc为空。
	print ("\nThe 3rd round of Save and Load is:")
	for ent in paragraph.ents:
		print ("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))
	assert [(ent.text, ent.label_) for ent in paragraph.ents] != [(u'2018年9月27日', u'EVENT')], "\nHere! The entity '%s' has matched the specified one." %ent.text


def Pipeline():
	print ("\nThe outcomes of Pipelining are:")
	lang = 'zh'
	pipeflow = ['tagger', 'parser', 'ner']
	cls = spacy.util.get_lang_class(lang)
	nlp = cls()
	for name in pipeflow:
		component = nlp.create_pipe(name)
		nlp.add_pipe(component) # 只有调用nlp才能触发pipeline，才能依次运行dummy_component、tagger、 parser、 ner！
	print ("The model has been saved into the disk.")
	nlp.from_disk(Loading_Path)

	doc = nlp.make_doc(u"京东CEO刘强东在美国明尼苏达涉嫌性侵女大学生。")
	for name, proc in nlp.pipeline:
		print ("\tHere the component is: {}\t{}".format(name, proc))
		doc = proc(doc)
		# print ("The pipeline is:", nlp.pipeline)
	print ("\n")
	print ("Before adding a component, the pipes are:", nlp.pipe_names)

	def dummy_component(doc):
		print ("Since this component is called, this doc '%s' has %d tokens." %(doc, len(doc)))
		return doc
	nlp.add_pipe(dummy_component, name='dummy_info', first=True)
	print ("After adding a component, the pipes are:", nlp.pipe_names)
	doc = nlp(u"京东刘强东在某个据说的时间和一个传说的地点遇见奶茶妹妹。") # 只有调用nlp才能触发pipeline，才能依次运行dummy_component、tagger、 parser、 ner！



def convert_JSON_python(source_file = "/home/wangdi498/SpaCy/NER_example2.json"):
	def store(target_file, data):
		with open(target_file, 'w') as json_file:
			json_file.write(json.dumps(data))
	def load(source_file):
		with open(source_file) as json_file:
			data = json.load(json_file)
			return data
	data = load(source_file)
	try:
		result = []
		for example in data['rasa_nlu_data']['common_examples']:
			marking_dict = {}
			marking_list = []
			for entity in example['entities']:
				marking_list.append((entity['start'], entity['end'], entity['entity']))
				marking_dict['entities'] = marking_list
			result.append((example['text'], marking_dict))
	except (IndexError, IOError) as e:
		print ("\nError! Incorrect data! {}".format(e))
	else:
		print ("\nThe convertion result is\n{}".format(result))
		return result


# GoldParse object是Doc object的实例化，收集训练数据作为gold standard，然后编码标注。所以Doc的内容是text，而GoldParse的内容是label。
def Train():
	print ("\nThe outcomes of Training and Updating are:")
	from spacy.tokens import Doc
	from spacy.vocab import Vocab
	from spacy.gold import GoldParse
	vocab = Vocab(tag_map={'N': {'pos': 'NOUN'}, 'V': {'pos': 'VERB'}})
	doc = Doc(vocab, words=['用户', '体验', 'APP'])
	gold = GoldParse(doc, tags=['N', 'V', 'N'])
	doc = Doc(Vocab(), words=['陆金所', '成立', 'AI实验室', '已经', '一年'])
	gold = GoldParse(doc, entities=['U-ORG', 'O', 'U-TECHNOLOGY', 'O', 'U-DATE'])
	doc = Doc(nlp.vocab, words=[u'刘强东', u'章泽天', u'大学生', u'遇见'], spaces=[False, False, False, False])
	gold = GoldParse(doc, entities=[u'PERSON', u'PERSON', u'PRODUCT', u'O'])

	train_data = convert_JSON_python('/home/wangdi498/SpaCy/NER_example2.json')
	with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != 'ner']):
		optimizer = nlp.begin_training()
		for i in range(10):
			random.shuffle(train_data)
			# 每轮都会shuffle训练数据，保证模型不会根据训练顺序来做generalizations。也可以设置dropout rate让模型以一定几率放弃一些features和representations来避免模型过牢地记住训练数据。
			for text, annotations in train_data:
				# doc = nlp.make_doc(text)
				# gold = GoldParse(doc, entities=entity_offsets)
				# nlp.update([doc], [gold], drop=0.5, sgd=optimizer)
				nlp.update([text], [annotations], sgd=optimizer) # 用得到的数据更新模型。
	nlp.to_disk("/home/wangdi498/SpaCy/models")



from pathlib import Path

TRAIN_DATA = [
    ('Who is Shaka Khan?', {
        'entities': [(7, 17, 'PERSON')]
    }),
    ('I like London and Berlin.', {
        'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
    })
]

TRAIN_DATA = convert_JSON_python("/home/wangdi498/_rasa_chatbot_vip/data/invest_nlu_data_train.json")
TEST_DATA = convert_JSON_python("/home/wangdi498/_rasa_chatbot_vip/data/invest_nlu_data_test.json")

@plac.annotations(
	model = ("Language model", "option", "m", str),
	output_dir = ("Output directory", "option", "o", Path),
	number_iterations = ("Number of training iterations", "option", "n", int))

def DIDA_NER(model=None, output_dir="/home/wangdi498/SpaCy/models", number_iterations=50):
	if model is not None:
		nlp = spacy.load(model)
		print ("In NER the goddamn language model {} already exists so it will be loaded.".format(model))
	else:
		nlp = spacy.blank('zh')
		print ("In NER the goddamn language model does not exist so 'zh_core_web_sm' will be loaded.")
	if 'ner' not in nlp.pipe_names:
		ner = nlp.create_pipe('ner') # create_pipe()只对SpaCy承认的component有效。
		nlp.add_pipe(ner, last=True)
	else:
		ner = nlp.get_pipe('ner')

	for _, annotations in TRAIN_DATA:
		for ent in annotations.get('entities'): # get可以返回None。
			ner.add_label(ent[2])

	# 其余component必须在NER训练时被终止！
	other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
	with nlp.disable_pipes(*other_pipes):
		optimizer = nlp.begin_training()
		for iteration in range(number_iterations):
			random.shuffle(TRAIN_DATA)
			# 每轮都会shuffle训练数据，保证模型不会根据训练顺序来做generalizations。也可以设置dropout rate让模型以一定几率放弃一些features和representations来避免模型过牢地记住训练数据。
			losses = {}
			for text, annotations in TRAIN_DATA:
				nlp.update([text], [annotations], drop=0.5, sgd=optimizer, losses=losses) # 用得到的数据更新模型。
			print ("In round {} of {} NER the loss is {}.".format(iteration, number_iterations, losses))

	# 姑且用训练数据直接测试。
	for text, _ in TRAIN_DATA:
		doc = nlp(text)
		print ("\n{}".format([(ent.text, ent.label_) for ent in doc.ents]))
		# print ("\nHow can I trust the entities without test?!\n{}".format([(ent.text, ent.label_) for ent in doc.ents]))
		# print ("\nHow can I trust the tokens without test?!\n{}".format([(token.text, token.ent_type_, token.ent_iob_) for token in doc]))

    # 存储训练好的模型。
	if output_dir is not None:
		output_dir = Path(output_dir)
		if not output_dir.exists():
			output_dir.mkdir()
		nlp.to_disk(output_dir)
		print ("\nThe NER model is saved to {}. This is the end of training.".format(output_dir))

		# 读取训练好的模型。
		print ("\nThe NER model is loaded from {}. This is the beginning of testing.".format(output_dir))
		nlu = spacy.load(output_dir)
		for text, _ in TEST_DATA:
			doc = nlu(text)
			print ("\n{}".format([(ent.text, ent.label_) for ent in doc.ents]))
			# print ("\nI can trust the entities with test.\n{}".format([(ent.text, ent.label_) for ent in doc.ents]))
			# print ("\nI can trust the tokens with test.\n{}".format([(token.text, token.ent_type_, token.ent_iob_) for token in doc]))



### $$$ %%% ===

if __name__ == "__main__":
	print ("\nHere we go...\n")
	# Tokenization()
	# Tagging()
	# Hashing()
	# Entity()
	# Vectorization1() # 128维词空间，|奶茶|=23.189319610595703。
	# Vectorization2() # 300维词空间，|奶茶|=2.2992143630981445。
	# Similarity1()
	# Similarity2()
	# Stop()
	# Parsing()
	# Serialization()
	# Pipeline()
	# Train()
	plac.call(DIDA_NER)
	print ("\nDone!\n")
