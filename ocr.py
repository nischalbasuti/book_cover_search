try:
    import Image
except ImportError as e:
    from PIL import Image
import pytesseract
import os
import argparse
import re
from stopwords import stop_words
from xlrd import open_workbook
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", help="path to directory with file(s)")
ap.add_argument("-i", "--image", help="path to file")
args = vars(ap.parse_args())

imagePath = args['image']
dirPath = args['dir']

def getStringFromFilePath(filePath):
    print(".....\n File:")
    print(imagePath)
    print(".....\n OCR:")
    print(pytesseract.image_to_string(Image.open(imagePath)))
    print(".....")
    return pytesseract.image_to_string(Image.open(imagePath))
    #check if number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def pretty(l, indent=0):
    for d in l:
        print(d)
#search for words in dict list.
def searchXlsx(filename, wordsToSearch):
    # Read xlsx file and save each row as a dict in dict_list.
    book = open_workbook(filename);
    sheet = book.sheet_by_index(0);
    # read header values into the list    
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

    dict_list = []
    for row_index in range(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value 
             for col_index in range(sheet.ncols)}
        dict_list.append(d)

    # get matches in results[]
    results = []
    titles = []
    for word in wordsToSearch:
        print(word)
        for row in dict_list:
            rowNameString = str(row["TITLE"])
            if re.search(r'\b%s\b'%(word.lower()), rowNameString.lower()):
                results.append(row);

    finalResults = []
    for word in wordsToSearch:
        print(word)
        for row in results:
            rowTitleString = str(row["AUTHOR"])
            # print(row['TITLE'])
            if re.search(r'\b%s\b'%(word.lower()), rowTitleString.lower()):
                finalResults.append( str( row  )+ "\n" );

    countedDict = Counter( finalResults )
    for result in countedDict:
        print(result)
        print(countedDict[result])

# get list of meaningful words to search
wordsList = re.findall(r"[\w']+",getStringFromFilePath(imagePath))
wordsToSearch = []
for word in wordsList:
    if (word.lower() not in stop_words) and (not is_number(word)):
        wordsToSearch.append(word)

searchXlsx("./AIT_Publication.xlsx", wordsToSearch)
searchXlsx("./generalbook.xls", wordsToSearch)

print(wordsToSearch)
