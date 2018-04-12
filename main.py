import requests
import traceback
import json
import cloudinary.uploader
import argparse
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
    print(r.status_code, r.reason, r.headers['content-type'], r.json()['guess'][0])

    #get information about book from goodreads using the response from google image search
    query = str(responseGoogle.json()['guess'][0]).replace('cover','').replace(' ','+')
    #^ removing 'cover' here because it's fucking with alot of images
    goodreadsUrl = "https://www.goodreads.com/search/index.xml?q="+query+"&key=be8kYuOF6mv9oVkl70OQrg&search_type=books"
    responseGoodreads = requests.get(goodreadsUrl)

    #parse xml response from goodreads to get information about book
    tree = ElementTree.fromstring(responseGoodreads.content)
    bookInfo = {}
    for child in tree.find("search").find("results").find("work").find("best_book"):
        if child.tag == 'author':
            bookInfo[child.tag] = {}
            for c in child:
                bookInfo[child.tag][c.tag] = c.text
        else:
            bookInfo[child.tag] = child.text
    print(json.dumps(bookInfo, sort_keys = True, indent = 4))
except Exception as e:
    print("Couldn't find book :(")
    print("....error.....")
    traceback.print_exc()
    print("..............")
finally:
    #cleanup --  delete image on cloudinary
    cloudinary.api.delete_resources([imagePublicId], cloud_name = 'nischalbasuti', api_key = '943833127745525', api_secret='ewiEk8AOpmpwfp3h6NvcC92owGs')
