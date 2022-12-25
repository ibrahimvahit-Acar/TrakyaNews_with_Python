import spacy
import nltk
import pytextrank
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

nlp = spacy.load('en_core_web_md')
nlp.add_pipe("textrank")


def pyTextRank(text):

    result = ""
    doc = nlp(text)
    # for p in doc._.phrases:
    #   print('{:.4f} {:5d}  {}'.format(p.rank, p.count, p.text))
    #  print(p.chunks)
    for sent in doc._.textrank.summary(limit_phrases=20, limit_sentences=4):
        result += str(sent)
    return result


def ozetle(metin):
    ozet_luhn = LuhnSummarizer()
    parser = PlaintextParser.from_string(metin, Tokenizer("turkish"))
    ozet = ozet_luhn(parser.document, 2)
    a = ""
    for cumle in ozet:
        a = a+str(cumle)
    return a
