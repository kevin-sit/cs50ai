import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    mapping = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding='utf-8') as f:
            mapping[file] = f.read()
    return mapping

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    return [word.lower() for word in nltk.word_tokenize(document) if not all(c in string.punctuation for c in word) and word not in nltk.corpus.stopwords.words("english")]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    n_doc = len(documents)
    idfs = {}
    for doc in documents:
        words.update(documents[doc])
    for w in words:
        f = sum(w in documents[doc] for doc in documents)
        idfs[w] = math.log(n_doc/ f)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = {
        filename: sum(files[filename].count(qword) * idfs[qword] for qword in query) 
        for filename in files 
    }
    return list(list(zip(*sorted(tfidf.items(), key=lambda x: x[1], reverse=True)))[0])[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rank = {}
    for s in sentences:
        idfs_word = 0
        i = 0
        for qword in query:
            if qword in sentences[s]:
                count = sentences[s].count(qword)
                i += count
                idfs_word += idfs[qword] * count
                print(s, qword, idfs[qword])
        if i > 0:
            rank[s] = (idfs_word, i/len(s))
                
    return list(list(zip(*sorted(rank.items(), key=lambda x: x[1], reverse=True)))[0])[:n]

if __name__ == "__main__":
    main()
