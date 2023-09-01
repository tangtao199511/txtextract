# Modified by TaoTao 2021

import sys
import csv
import importlib
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
Parse PDF text and save it to a txt file.
'''
csvfile = open("list.csv", "r")
reader = csv.reader(csvfile)
filename = list(reader)
names = filename

def parse():
    fp = open(path2, 'rb')  # Open in binary read mode
    # Create a PDF parser object using the file object
    praser = PDFParser(fp)
    # Create a PDF document object
    doc = PDFDocument()
    # Link parser and document object
    praser.set_document(doc)
    doc.set_parser(praser)

    # Provide an initialization password
    # Create an empty string if no password is needed
    doc.initialize()

    # Check if the document allows text extraction. If not, ignore.
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # Create a PDF resource manager to manage shared resources
        rsrcmgr = PDFResourceManager()
        # Create a PDF device object
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Loop through each page in the document
        for page in doc.get_pages():  # doc.get_pages() returns a list of pages
            interpreter.process_page(page)
            # Obtain the LTPage object for the current page
            layout = device.get_result()
            # Extract text and write it to a txt file
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(path4, 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')

def solve():
    # Parsing the text
    import jieba
    excludes = {}  # exclude words which will not be detected
    txt = open(path4, "r", encoding='utf-8').read()
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        if len(word) == 1:  # Exclude words that are a single character
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    for word in excludes:
        del (counts[word])
    # count the frequency of the words.
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    fo = open(path5, "w")
    for item in items:
        ls = list(item)
        ls[1] = str(ls[1])
        fo.write(",".join(ls) + "\n")
    fo.close()


if __name__ == '__main__':
    for path3 in names:
        path2 = "\r".join(path3)
        path = path2[0:10]
        path4 = path + '.txt'
        path5 = path + '.csv'
        parse()
        solve()
