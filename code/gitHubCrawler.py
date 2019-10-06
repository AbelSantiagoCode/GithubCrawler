# importing the requests library
import requests


class GitHubCrawler(object):
    """docstring for GitHubCrawler."""

    def __init__(self, keywords,proxy):
        self.__urlSearch = "https://github.com/search?q="
        for key in keywords:
            self.__urlSearch = self.__urlSearch + key +"+"
        self.__urlSearch = self.__urlSearch[:-1]
        self.__proxy = {"https": "https://"+proxy} #"185.57.222.138:8080"

    def __getHTML(self):
        #return the HTML of Get request
        return requests.get(url = self.__urlSearch,proxies=self.__proxy).text

    def __getHTMLType(self, type):
        #return the HTML of Get request
        return requests.get(url = self.__urlSearch+"&type="+type,proxies=self.__proxy).text

    def __getLinksFromListHTML(self,html,startListID,endListID,itemID,isWiki):
        urls = []
        startListHTML = html.find(startListID)
        if startListHTML != -1:
            endListHTML = html.find(endListID,startListHTML)
            listHTML = html[startListHTML:endListHTML]
            while 1:
                startItemHTML = listHTML.find(itemID)
                if startItemHTML != -1:
                    endItemHTML = listHTML.find(itemID,startItemHTML+27)
                    item = listHTML[startItemHTML:endItemHTML]

                    if isWiki:
                        startHref = item.find("href=")
                        startHref = item.find("href=",startHref+6)+6
                        startHref = item.find("href=",startHref+6)+6
                    else:
                        startHref = item.find("href=")+6
                    endHref = item.find('''">''',startHref)
                    href = item[startHref:endHref]
                    urls = urls + ["https://github.com"+href]
                    listHTML = listHTML[endItemHTML:]

                else:
                    break
        return urls

    def getLinksRepos(self):
        try:
            html = self.__getHTMLType("Repositories")
            return self.__getLinksFromListHTML(html,'''<ul class="repo-list"''',"</ul>",'''<li class="repo-list-item''',False)
        except Exception as e:
            print("Fuction getLinksRepos: FAILED TO CONNECT THROUGH PROXY, PLEASE USE ANOTHER PROXY")
            return []
    def getLinksIssues(self):
        try:
            html = self.__getHTMLType("Issues")
            return self.__getLinksFromListHTML(html,'''<div class="issue-list">''','''<div class="footer container-lg width-full p-responsive"''','''<div class="issue-list-item''',False)
        except Exception as e:
            print("Fuction getLinksIssues: FAILED TO CONNECT THROUGH PROXY, PLEASE USE ANOTHER PROXY")
            return []

    def getLinksWikis(self):
        try:
            html = self.__getHTMLType("Wikis")
            return self.__getLinksFromListHTML(html,'''<div id="wiki_search_results">''','''<div class="footer container-lg width-full p-responsive"''','''<div class="wiki-list-item''',True)
        except Exception as e:
            print("Fuction getLinksWikis: FAILED TO CONNECT THROUGH PROXY, PLEASE USE ANOTHER PROXY")
            return []

    def getLangStatRepos(self, repository):
        extraInfo = []
        languages = {}
        ower = repository[19:].split('/')[0]
        try:
            html = requests.get(url = repository,proxies=self.__proxy).text
        except Exception as e:
            print("Fuction getLangStatRepos: FAILED TO CONNECT THROUGH PROXY, PLEASE USE ANOTHER PROXY")
            return {}
        startListHTML = html.find('''<ol class="repository-lang-stats-numbers">''')
        endListHTML = html.find("</ol>",startListHTML)
        listHTML = html[startListHTML:endListHTML]
        while 1:
            startLangHTML = listHTML.find('''<span class="lang">''')
            if startLangHTML != -1:
                startLangHTML+=19
                endLangHTML = listHTML.find("</span>",startLangHTML)
                lang = listHTML[startLangHTML:endLangHTML]

                startPercentHTML = listHTML.find('''<span class="percent">''')+22
                endPercentHTML = listHTML.find("</span>",startPercentHTML)
                percent = listHTML[startPercentHTML:endPercentHTML-1]

                languages[lang] = percent
                listHTML = listHTML[endPercentHTML:]
            else:
                break
        extraInfo = extraInfo + [ower, languages]
        return extraInfo
