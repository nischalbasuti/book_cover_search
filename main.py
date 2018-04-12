import requests
import traceback
import json
import cloudinary.uploader
import argparse
from stopwords import stop_words
from xlrd import open_workbook
from xml.etree import ElementTree
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#get local path to image
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True,  help = 'path to file')
args = vars(ap.parse_args())
imagePath = args['image']

#url of local server being run
googleUrl = "http://localhost:5000/search"

#upload image to cloudinary and get url of and public_id of image
uploadResponse = cloudinary.uploader.unsigned_upload(imagePath, "hqhbsw8g", cloud_name="nischalbasuti")
imageUrl = uploadResponse['url']
print(imageUrl)
imagePublicId = uploadResponse['public_id']

#google search by image with imageUrl to get image description
r = responseGoogle = requests.post(googleUrl, json={"image_url":imageUrl})
try:
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
    wordsList = r.json()['guess'][0].split(' ')
    wordsToSearch = []
    for word in wordsList:
        if (word.lower() not in stop_words) and (not is_number(word)):
            wordsToSearch.append(word)
    print(wordsToSearch)

    searchXlsx("./AIT_Publication.xlsx", wordsToSearch)
    searchXlsx("./generalbook.xls", wordsToSearch)

except Exception as e:
    print("Couldn't find book :(")
    print("....error.....")
    traceback.print_exc()
    print("..............")
finally:
    #cleanup --  delete image on cloudinary
    cloudinary.api.delete_resources([imagePublicId], cloud_name = 'nischalbasuti', api_key = '943833127745525', api_secret='ewiEk8AOpmpwfp3h6NvcC92owGs')
