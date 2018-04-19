try:
    import Image
except ImportError as e:
    from PIL import Image
import pytesseract
import os
import argparse
from stopwords import stop_words
from xlrd import open_workbook

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
    results = [];
    for word in wordsToSearch:
        for row in dict_list:
            rowString = str(row)
            if word.lower() in rowString.lower():
                results.append( row );

    print(len(results))
    print(results)

# get list of meaningful words to search
wordsList = getStringFromFilePath(imagePath).split(' ')
wordsToSearch = []
for word in wordsList:
    if (word.lower() not in stop_words) and (not is_number(word)):
        wordsToSearch.append(word)
print(wordsToSearch)

searchXlsx("./AIT_Publication.xlsx", wordsToSearch)
searchXlsx("./generalbook.xls", wordsToSearch)


# if __name__ == "__main__":
#     if imagePath is not None:
#         print(".....\n File:")
#         print(imagePath)
#         print(".....\n OCR:")
#         print(pytesseract.image_to_string(Image.open(imagePath)))
#         print(".....")
#     if dirPath is not None:
#         for subdir, dirs, files in os.walk(dirPath):
#             for file in files:
#                 filedir = os.path.join(dirPath, file) 
#                 print("..... File:")
#                 print(filedir)
#                 print("..... OCR:")
#                 print(pytesseract.image_to_string(Image.open(filedir)))
#                 print(".....\n\n")
