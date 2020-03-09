from files import read_json_file
from pathlib import Path
from nltk.stem import WordNetLemmatizer 
from spacy.lang.en.stop_words import STOP_WORDS
import re
import spacy
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules import CITATION_PATTERNS

nlp = spacy.load("en_blackstone_proto")
sentence_segmenter = SentenceSegmenter(nlp.vocab, CITATION_PATTERNS)
nlp.add_pipe(sentence_segmenter, before="parser")

# Build a List of Stopwords
stopwords = list(STOP_WORDS)


def tokenize(text):
    lemmatizer = WordNetLemmatizer() 
    tokenized_para = []
    split = text.split()
    # TODO need to remove special characters from token and replace with space
    for word in split :
        if word.lower() not in stopwords :
            #lemmatize the words
            tokenized_para.append(lemmatizer.lemmatize(word))
            
    return tokenized_para


def extract_sent_from_para(para, token_count = 4):
    sent = []
    docx = nlp(para)
    for sentence in docx.sents:
        if(len(tokenize(sentence.text)) > token_count):
            sent.append(sentence.text)
    return sent
    


def extract_para_from_judgement(filepath):
    data = read_json_file(filepath)
    processed_paras = []
    if data:
        judgement = data["judgement"]
        for para in judgement:
            txt = para['txt'].strip()
            tag = para['id'].strip()

            if(tag and txt and not "pre" in tag):
                # remove newlines and replace with space
                para_txt = (' '.join(txt.split())).strip()
                # removes the paragraph lables 1. or 2. etc.
                para_txt = re.sub(r'(^|"[ ]{0,})(\d\d\d|\d\d|\d)\.', '', para_txt).strip()
                # remove the paragraph lables A. etc
                para_txt = re.sub(r'(^|"[ ]{0,})([A-Za-z]*)\.', '', para_txt).strip()
                # remove the quotes and other special charater from end of string
                # para_txt = re.sub(r'(^|"[ ]{0,})([A-Za-z]*)\.', '', para_txt).strip()
                # remove any character from start of string which is not qoute, alpha or number
                para_txt = re.sub(r'^[^-zA-Z0-9"]', '', para_txt).strip()
                # remove extra space and multiple .
                para_txt = re.sub(r'[\. ]{1,}[\.]{1,}[\. ]*', '', para_txt).strip()
                # # removes dot(.) i.e File No.1063
                # para_txt = re.sub(r'(?<=[a-zA-Z])\.(?=\d)', '', para_txt)
                # # to remove the ending dot of abbr
                # para_txt = re.sub(r'(?<=\d|[a-zA-Z])\.(?=\s[\da-z])', ' ', para_txt)
                # # to remove the ending dot of abbr
                # para_txt = re.sub(r'(?<=\d|[a-zA-Z])\.(?=\s?[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~])', '', para_txt)
                # # removes the other punctuations
                # para_txt = re.sub(r'(?<!\.)[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]', ' ', para_txt)
                processed_paras.append(para_txt)
            else:
                pass
    return processed_paras


def extract_sent_from_judgement(filepath, token_count):
    sent = []
    paras = extract_para_from_judgement(filepath)
    for para in paras:
        sent.extend(extract_sent_from_para(para, token_count))
    return sent


print(extract_sent_from_judgement(Path("/Users/ujjwalks/Desktop/al/cases/supreme_court/judgements/1957/1261450.json")))