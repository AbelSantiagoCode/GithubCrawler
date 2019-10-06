import json
import random
import sys
from gitHubCrawler import GitHubCrawler


def readJSON(file):
    with open(file, 'r') as f:
        datastore = json.load(f)
        keywords = datastore["keywords"]
        proxies = datastore["proxies"]
        proxy = proxies[random.randint(0,len(proxies)-1)]
        type = datastore["type"]
        #print(datastore)
        return keywords,proxy,type

def writeJSON(file,results):
    jsonOutput =[]
    with open(file, 'w') as f:
        for result in results:
            result = str(result).replace("'",'''"''')
            result = json.loads(result)
            jsonOutput = jsonOutput + [result]
        json.dump(jsonOutput, f)

def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    output = []
    keywords,proxy,type=readJSON(inputFile)

    # GET LINKS FROM REPOSITORIES, ISSUES OR WIKIS
    search = GitHubCrawler(keywords,proxy)
    if type == "Repositories":
        links = search.getLinksRepos() #type list
    elif type == "Issues":
        links = search.getLinksIssues() #type list
    elif type == "Wikis":
        links = search.getLinksWikis() #type list

    #   WRITE RESULTS TO OUTPUT FILE
    if links == []:
        print("THERE ARE NOT "+type+", PLEASE CHECK YOUR CONNECTION TO YOUR PROXY")
    else:
        for link in links:
            if type == "Repositories":
                # GET EXTRA INFORMATION FOR REPOSITORIES
                try:
                    ower,langs = search.getLangStatRepos(link)
                    output = output + [{"url":link,"extra":{"ower":ower,"language_stats":langs}}]
                except Exception as e:
                    print("THERE ARE NOT EXTRA INFORMATION FOR "+link+ ", PLEASE CHECK YOUR CONNECTION TO YOUR PROXY")
                    output = output + [{"url":link}]
            else:
                output = output + [{"url":link}]
        writeJSON(outputFile,output)



if __name__ == '__main__':
    # python3 main.py <input.json> <output.json>
    main()
