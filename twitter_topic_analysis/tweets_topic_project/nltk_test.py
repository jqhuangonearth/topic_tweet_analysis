import nltk
import re
import topic
from nltk.tree import *

print nltk.corpus.stopwords.words('english')
sentence = """At eight o'clock on Thursday morning    ... Arthur didn't feel very good."""

tokens = nltk.word_tokenize(sentence)
print tokens

text = "#HonestyHour I'd rather not be around highly emotional people. I didn't come from a family how wore their emotions on there's sleeves. @FredyGarcia10 @thatchick_macy http:\\/\\/t.co\\/DmFH97GNYy".lower()
words = re.sub(r'http:[\\/.a-z0-9]+\s?', '', text)
print words
words = re.sub(r'(@\w+\s?)|(@\s+)', '', words)
print words
words = re.sub(r'[\#\-\+\*\`\.\;\:\"\?\<\>\[\]\{\}\|\~\_\=]', '', words)
print words
words = re.sub(r'rt\s?', '', words)
print words
words = words.strip()

token = nltk.word_tokenize(words)
print token
words = words.split()
print words

mytopic = topic.topic()
print mytopic.process_sentence(text)


# Tree manipulation

# Extract phrases from a parsed (chunked) tree
# Phrase = tag for the string phrase (sub-tree) to extract
# Returns: List of deep copies;  Recursive
def ExtractPhrases( myTree, phrase):
    myPhrases = []
    if (myTree.node == phrase):
        myPhrases.append( myTree.copy(True) )
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = ExtractPhrases(child, phrase)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases

#mini_grammar = ContextFreeGrammar(Nonterminal('S'), treebank.parsed_sents()[0].productions())
#parser = nltk.parse.EarleyChartParser(mini_grammar)
#print parser.parse(treebank.sents()[0])
groucho_grammar = nltk.data.load("file:/home/bolun/Downloads/large_grammars/atis.cfg")
sent = words
parser = nltk.ChartParser(groucho_grammar)
trees = parser.nbest_parse(sent)
for tree in trees:
    test = Tree.parse('(S (NP I) (VP (V enjoyed) (NP my cookies)))')

print "Input tree: ", test

print "\nNoun phrases:"
list_of_noun_phrases = ExtractPhrases(test, 'NP')
for phrase in list_of_noun_phrases:
    print " ", phrase