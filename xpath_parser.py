from bs4 import BeautifulSoup
from lxml import etree
import json
import re


def parse_with_xpath_overstock(html_content):
    soupHtml = BeautifulSoup(html_content, 'html.parser').prettify()
    dom = etree.HTML(soupHtml)

    allTitles = dom.xpath('//a[@href]/b[contains(text(), "1")]')
    allContent = dom.xpath('//span[@class="normal"]')
    allListPrices = dom.xpath('//s')
    allPrices = dom.xpath('//span[@class="bigred"]/b')
    allSavings = dom.xpath('//td[@align="left"]/span[@class="littleorange"]')

    # dictionary
    data = []
    dataLength = len(allTitles)

    for i in range(0, dataLength):
        x = {}
        title = allTitles[i].text.strip()
        content = re.sub("\n", " ", allContent[i].text.strip())
        listPrice = allListPrices[i].text.strip()
        price = allPrices[i].text.strip()
        savingsText = re.split("\s", allSavings[i].text.strip())
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
    # print(yJson)
    return yJson


def parse_with_xpath_rtvslo(html_content):
    soupHtml = BeautifulSoup(html_content, 'html.parser').prettify()
    dom = etree.HTML(soupHtml)

    authorName = dom.xpath('//div[@class="author-name"]/text()')[0].strip()
    publishedTime = dom.xpath('//div[@class="publish-meta"]/text()')[0].strip()
    title = dom.xpath('//h1/text()')[0].strip()
    subtitle = dom.xpath('//div[@class="subtitle"]/text()')[0].strip()
    lead = dom.xpath('//p[@class="lead"]/text()')[0].strip()
    content = dom.xpath('//article[@class="article"]/p/text()')
    contentText = ''
    for text in content:
        contentText += re.sub("\n", " ", text.strip())

    # dictionary
    data = {}
    data["AuthorName"] = authorName
    data["PublishedTime"] = publishedTime
    data["Title"] = title
    data["Subtitle"] = subtitle
    data["Lead"] = lead
    data["Content"] = contentText

    yJson = json.dumps(data, ensure_ascii=False)
    # print(data)
    return yJson


if __name__ == "__main__":
    html1 = "WebPages/overstock.com/jewelry01.html"
    html2 = "WebPages/overstock.com/jewelry02.html"

    htmlFile1 = open(html1, 'rb').read()

    json1 = parse_with_xpath_overstock(htmlFile1)
    print(json1)

    html3 = "WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    html4 = "WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"

    htmlFile2 = open(html3, 'r', encoding='utf-8').read()

    json2 = parse_with_xpath_rtvslo(htmlFile2)
    print(json2)
