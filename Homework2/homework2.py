from urllib import request
from bs4 import BeautifulSoup
import string
from collections import Counter
import numpy as np


# cosine similarity
def cosine_similarity(d1, d2):
    '''
    Parameters
    ----------
    d1, d2 : dictionary
        The dictionaries of the frequency counted in the texts
    Returns
    -------
    res : float
        Cosine Similarity
    '''
    A, B, AB = 0,0,0
    # print(type(d1))
    for word in d1.keys():
        if word in d2.keys():
            AB += d1[word] * d2[word]
        A += d1[word]**2
    for v in d2.values():
        B += v**2
    res = round( A / np.sqrt(A*B), 4)
    return res

# get url
def get_url():
    """
    Return
    -------
    res: list
        The list of urls
    """
    res = []
    file =  open("./hw2.txt", 'r')
    for line in file.readlines():
        res.append(line.strip())
    file.close()
    return res

# count the word frequency
def count_word(url):
    '''
    Parameters
    ----------
    url : str
        The url
    Returns
    -------
    res : dictionary
        The dictionaries of the frequency counted in the texts
    '''
    #url = "https://en.wikipedia.org/wiki/Chase_Bank"
    #url = "https://en.wikipedia.org/wiki/Citibank"
    #url = "http://bankofamerica.com/"
    #url = "https://www.jpmorgan.com/country/US/en/jpmorgan"
    #url = "https://www.business.rutgers.edu/"
    html = request.urlopen(url).read()
    #soup = BeautifulSoup(html)
    soup = BeautifulSoup(html, "lxml")
    # remove all script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    # now retrieve text
    text = soup.get_text()
    for c in string.punctuation:
        text = text.replace(c, "")
    text = text.split()
    res = Counter(text)
    return res

def get_matrix():
    '''
    Returns
    -------
    res : list
        The Matrix
    '''
    urlpaths = get_url()
    #print(urlpaths)
    count_list = []
    for path in urlpaths:
        count = count_word(path)
        #print(count)
        count_list.append(count)

    #print(count_results)
    res = []
    n = len(count_list)
    for i in range(n):
        d1 = count_list[i]
        # print(curr_d)
        row = [0]*n
        row[i] = 1
        for j in range(i+1, n):
            d2 = count_list[j]
            row[j] = cosine_similarity(d1, d2)
        res.append(row)

    for i in range(1, len(res)):
        for j in range(i):
            res[i][j] = res[j][i]
    return res



Matrix = get_matrix()
urls_name = get_url()

urls = []
for i in range(len(Matrix)):
    urls.append("url_"+str(i+1))

titile = "\t"
for url in urls:
    titile += url+"\t"
print(titile)

f = open("output.txt", "w")
f.write(titile+"\n")

for i in range(len(urls)):
    row = urls[i]+"\t"
    for j in range(i+1):
        row += str(Matrix[i][j]) + "\t"
    print(row)
    # with open("./output.txt", "a") as f:
    f.write(row+"\n")

print()
f.write("\n")
print()
for i in range(len(Matrix)):
    single_res = Matrix[i]
    new_single_res = single_res[:i]+single_res[i+1:]
    max_index = single_res.index(max(new_single_res))
    print("The most similar page of {} ({}) is: {} ({})".format(urls[i], urls_name[i], urls[max_index], urls_name[max_index]))
    # with open("./output.txt", "a") as f:
    f.write("The most similar page of {} ({}) is: {} ({})".format(urls[i], urls_name[i], urls[max_index], urls_name[max_index]))
    f.write("\n")

f.close()

