from bs4 import BeautifulSoup
import json
import re


def parse_with_regex_overstock(html_content):
    soupHtml = BeautifulSoup(html_content, 'html.parser')

    allTitles = soupHtml.find_all('table', attrs={'border': '0', 'cellpadding': '0', \
                'cellspacing': '0', 'width': '100%'})[2].find_all('b', text=re.compile('^\d'))
    allContent = soupHtml.find_all('table', attrs={'border': '0', 'cellpadding': '0', \
                'cellspacing': '0', 'width': '100%'})[2].find_all(class_=re.compile("normal"))
    allListPrices = soupHtml.find_all('table', attrs={'border': '0', 'cellpadding': '0', \
                'cellspacing': '0', 'width': '100%'})[2].find_all("s")
    allPrices = soupHtml.find_all('table', attrs={'border': '0', 'cellpadding': '0', \
                'cellspacing': '0', 'width': '100%'})[2].find_all(class_=re.compile("bigred"))
    allSavings = soupHtml.find_all('table', attrs={'border': '0', 'cellpadding': '0', \
                'cellspacing': '0', 'width': '100%'})[2].find_all(class_=re.compile("littleorange"))

    # dictionary
    data = []
    dataLength = len(allTitles)

    for i in range(0,dataLength):
        x = {}
        title = allTitles[i].text
        content = re.sub("\n", " ", allContent[i].contents[0])
        listPrice = allListPrices[i].text
        price = allPrices[i].text
        savingsText = re.split("\s", allSavings[i].text)
        saving = savingsText[0]
        savingPercent = savingsText[1]

        x["Title"] = title
        x["Content"] = content
        x["ListPrice"] = listPrice
        x["Price"] = price
        x["Saving"] = saving
        x["SavingPercent"] = savingPercent
        data.append(x)

    yJson = json.dumps(data)
    #print(yJson)
    return yJson


def parse_with_regex_rtvslo(html_content):
    soupHtml = BeautifulSoup(html_content, 'html.parser')

    # dictionary
    data = {}

    # parsing
    authorName = soupHtml.find(class_=re.compile("author-name")).text
    publishedTime = soupHtml.find(class_=re.compile("publish-meta")).contents[0].strip()
    title = soupHtml.find(re.compile("h1")).text
    subtitle = soupHtml.find(class_=re.compile("subtitle")).text
    lead = soupHtml.find(class_=re.compile("lead")).text
    content = soupHtml.find("article").find_all("p")
    contentText = ''
    for i in content:
        contentText += re.sub("\n", " ", i.text)

    data["AuthorName"] = authorName
    data["PublishedTime"] = publishedTime
    data["Title"] = title
    data["Subtitle"] = subtitle
    data["Lead"] = lead
    data["Content"] = contentText

    yJson = json.dumps(data, ensure_ascii=False)
    # print(data)
    return yJson


def parse_with_regex_avtonet(html_content):
    soupHtml = BeautifulSoup(html_content, 'html.parser')

    allTitles = re.findall(r"<span>(.+)</span>", str(soupHtml.find_all(class_=re.compile("Adlink"))))
    allRegistrations = re.findall(r"\d{4}", str(soupHtml.find_all('li', text=re.compile('Letnik'))))
    allKM = re.findall(r"(\d+)", str(soupHtml.find_all('li', text=re.compile('km'))))
    allMotorData = re.findall(r"<li>(.*?)</li>", str(soupHtml.find_all('li', text=re.compile('kW'))))
    allMenjalniki = re.findall(r"<li>(.*?)</li>", str(soupHtml.find_all('li', text=re.compile('ročni|avtomatski'))))
    allPrices = soupHtml.find_all(class_=re.compile("ResultsAdPriceLogo"))

    # dictionary
    data = []
    dataLength = len(allTitles)
    allKM.insert(35, 0)

    for i in range(0,dataLength):
        x = {}
        x["Ime"] = allTitles[i]
        x["Letnik 1.registracije"] = allRegistrations[i]
        x["Prevoženi km"] = allKM[i]
        x["Motor"] = allMotorData[i]
        x["Menjalnik"] = allMenjalniki[i]
        x["Cena"] = allPrices[i].text.strip()
        data.append(x)

    yJson = json.dumps(data, ensure_ascii=False)
    #print(yJson)
    return yJson


if __name__ == "__main__":
    html1 = "../input/overstock.com/jewelry01.html"
    html2 = "../input/overstock.com/jewelry02.html"

    htmlFile1 = open(html1, 'rb').read()

    json1 = parse_with_regex_overstock(htmlFile1)
    print(json1)

    html3 = "../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    html4 = "../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"

    htmlFile2 = open(html3, 'r', encoding='utf-8').read()

    json2 = parse_with_regex_rtvslo(htmlFile2)
    print(json2)

    html5 = "../input/avto.net/avtonet1.html"
    html6 = "../input/avto.net/avtonet2.html"

    htmlFile3 = open(html5, "rb").read()

    json3 = parse_with_regex_avtonet(htmlFile3)
    print(json3)
