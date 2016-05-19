import requests, sys, webbrowser, bs4, time, random

# Randomly selects/returns a valid href given a list of link objects
def generateLink(links):
    searchingForLink = True;
    temp = ""
    while searchingForLink:
        randNum = random.randint(0, len(links) - 1)
        temp = links[randNum]
        if temp.get("href") != None:
            check = ':' not in temp.get("href")
            check2 = check and 'wikipedia' not in temp.get("href")
            check3 = check2 and 'Wikipedia' not in temp.get("href")
            check4 = check3 and 'wikimedia' not in temp.get("href")
            # duplicate links (links linking to itself)
            if '/wiki/' in temp.get("href") and check4:
                searchingForLink = False 
    return temp.get("href").split('/')[2]

start = "https://en.wikipedia.org/wiki/"
print('Type in Something in Wikipedia')
temp = raw_input()
print('How far many links would you like to crawl')
num = raw_input()
temp.replace(" ", "_")
res = requests.get(start + temp)
# webbrowser.open(start + temp)
storage = {}
for i in range(int(num)):
    time.sleep(0)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = soup.select('a')
    temp = generateLink(links)
    res = requests.get(start + temp)
    # webbrowser.open(start + temp)
    temp_2 = temp.replace("_", " ")
    if temp_2 in storage:
        storage[temp_2] += 1
    else:
        storage[temp_2] = 1
    print str(i) + " " + temp_2
for key in sorted(storage):
    print key + ": " + str(storage[key])
