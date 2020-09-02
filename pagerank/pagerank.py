import os
import random
import re
import sys
import numpy as np
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    prob = {}
    n = len(corpus)
    links = corpus[page]
    l = len(links)
    if l == 0: #No link
        for p in corpus:
            prob[p] = 1 / n    
    else:    
        for p in corpus:
            if p in links:
                prob[p] = (1 - damping_factor) / n + damping_factor / l # in link
            else:
                prob[p] = (1 - damping_factor) / n
    return prob

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print(corpus)
    pagerank = {}
    for i in range(n):
        if i == 0:
            page = random.choice(list(corpus.keys()))
            pagerank[page] = 1
        else:
            prob = transition_model(corpus, page, damping_factor)
            page = np.random.choice(list(prob.keys()), p=list(prob.values()))
            if page in pagerank:
                pagerank[page] += 1
            else:
                pagerank[page] = 1
    for page in pagerank:
        pagerank[page] /= n
    return pagerank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    n = len(corpus)
    
    pagerank = {} 
    for p in corpus.keys():
        pagerank[p] = 1 / n
    stop = True
    new_pagerank = copy.deepcopy(pagerank)
    while (stop):
        stop = False
        for p in corpus.keys():
            new_pagerank[p] = (1 - damping_factor) / n # pagerank[pagerank['page'] == p] = (1 - damping_factor) / n
            for p2 in corpus.keys():
                if p != p2:
                    l = len(corpus[p2])
                    if p in corpus[p2]:
                        new_pagerank[p] += damping_factor / l * new_pagerank[p2]# pagerank[pagerank['page'] == p] += damping_factor / len(pagerank[p2]) * pagerank[pagerank['page'] == p]
                    elif l == 0:
                        new_pagerank[p] += damping_factor / n * new_pagerank[p2]
            if abs(new_pagerank[p] - pagerank[p]) > 0.001:
                stop = True
        pagerank = copy.deepcopy(new_pagerank)
    return new_pagerank            


if __name__ == "__main__":
    main()
