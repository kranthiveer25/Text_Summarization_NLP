import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week to 2007."""
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

    tokens = [token.text for token in doc]

    # Calculate word frequencies
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq:
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    #print("Word Frequencies:", word_freq)

    # Find maximum frequency
    max_freq = max(word_freq.values())
    print("Maximum Frequency:", max_freq)

    # Normalize frequencies
    for word in word_freq:  # Corrected iteration
        word_freq[word] = word_freq[word] / max_freq

    #print("Normalized Frequencies:", word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] = word_freq[word.text]
    #print(sent_scores)

    select_len = int(len(sent_tokens)*0.6)
    #print(select_len)
    summary = nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)
    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)
    #print(text)
    #print(summary)
    #print("length of original text" ,len(text.split(' ')))
    #print("length of summary text ",len(summary.split(' ')))

    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))