from bs4 import BeautifulSoup, Comment

def funcRoadRunnerWrapper(html1, html2):
    html1 = BeautifulSoup(html1, 'html.parser')
    html2 = BeautifulSoup(html2, 'html.parser')

    bodyTagHtml1 = html1.body
    bodyTagHtml2 = html2.body

    for tag in bodyTagHtml1.findAll(True):
        tag.attrs = {}

    for tag in bodyTagHtml2.findAll(True):
        tag.attrs = {}

    for script in bodyTagHtml1(["script", "style", "noscript", "iframe", "map"]):  # remove all javascript and stylesheet code
        script.extract()

    for script in bodyTagHtml2(["script", "style", "noscript", "iframe", "map"]):  # remove all javascript and stylesheet code
        script.extract()

    comments = html1.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    comments = html2.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    root_childs1 = [e for e in bodyTagHtml1.children if e.name is not None]
    #print(root_childs1)
    root_childs2 = [e for e in bodyTagHtml2.children if e.name is not None]
    #print(root_childs2)

    dataLength = len(root_childs1)
    result = "<html><body>"

    for i in range(0,dataLength):
        if root_childs1[i] == root_childs2[i] and root_childs1[i].text == root_childs2[i].text:
            result = result + str(root_childs1[i])
        else:
            tag1 = root_childs1[i]
            tag2 = root_childs2[i]
            if numberOfChildren(tag1) != 0 and numberOfChildren(tag2) != 0:
                firPageTag = tagChildren(tag1)[0]
                secPageTag = tagChildren(tag2)[0]
                if getParentTag(firPageTag) != getParentTag(secPageTag):
                    # print("TAG MISMATCH")
                    # handle mismatches / needs more work
                    result = result + "("
                    result = result + str(firPageTag)
                    result = result + ")+"
                else:
                    result = result + str(getParentTag(firPageTag))
                    if firPageTag.text != secPageTag.text:
                        result = result + "#PCDATA"

    result = result + '</body></html>'
    return result

def numberOfChildren(tag):
    return len([e.name for e in tag.children if e.name is not None])

def tagChildren(tag):
    return [e for e in tag.children if e.name is not None]

def getParentTag(tag):
    return "<"+tag.parent.name+">"

def getTagText(tag):
    return tag.text

if __name__ == "__main__":
    html1 = "../input/avto.net/avtonet1.html"
    html2 = "../input/avto.net/avtonet2.html"

    #html1 = "../input/overstock.com/jewelry01.html"
    #html2 = "../input/overstock.com/jewelry02.html"

    #html1 = "../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    #html2 = "../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"

    htmlFile1 = open(html1, 'rb').read()
    htmlFile2 = open(html2, 'rb').read()

    result = funcRoadRunnerWrapper(htmlFile1, htmlFile2)
    print(result)
