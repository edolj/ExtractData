from bs4 import BeautifulSoup
import re

def funcRoadRunnerWrapper(html1, html2):

    return []


if __name__ == "__main__":
    html1 = "../input/avto.net/avtonet1.html"
    html2 = "../input/avto.net/avtonet2.html"

    htmlFile1 = open(html1, 'rb').read()
    htmlFile2 = open(html2, 'rb').read()

    result = funcRoadRunnerWrapper(htmlFile1, htmlFile2)
    print(result)
