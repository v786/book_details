import sys
import getopt
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET


"""
{
"title":"A Song of Ice and Fire (A Song of Ice and Fire, #1-5)",
"average_rating":4.64,
"ratings_count":22072,
"num_pages":5216,
"image_url":"https://images.gr-assets.com/books/1339340118m/12177850.jpg",
"publication_year":"2000",
"authors":"George R.R. Martin"
}
"""


class GoodreadsAPIClient():

    def get_book_details(self, request):
        url = request+".xml?key="+self.get_key()

        try:
            response = requests.request("GET", url, headers={})
        except:
            return {}
        root = ET.fromstring(response.text)

        book = root.find("book")

        if book == None:
            return None

        book_details = {}
        elems = [
            "title",
            "average_rating",
            "ratings_count",
            "num_pages",
            "image_url",
            "publication_year",
        ]

        for each in elems:
            data = book.find(each)
            if data != None:
                book_details[each] = data.text

        elem = book.find("authors")

        book_details["author"] = []

        for each in elem.findall("author"):
            data = each.find("name")
            if data != None:
                book_details["author"].append(data.text)


        return book_details

    def get_key(self):
        with open('secret_key.txt') as f:
            return f.read().strip()


def main(argv):
    print(argv)
    api = GoodreadsAPIClient()
    print(api.get_book_details(argv[0]))


if __name__ == "__main__":
    main(sys.argv[1:])
