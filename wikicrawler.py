import requests, sys, webbrowser, bs4, random, operator, os

# returning if a link is legit or not (true or false)
def linkFilters(temp):
    if temp.get("href") != None:
            check = ':' not in temp.get("href")
            check2 = check and 'wikipedia' not in temp.get("href")
            check3 = check2 and 'Wikipedia' not in temp.get("href")
            check4 = check3 and 'wikimedia' not in temp.get("href")
            check5 = check4 and 'Main_Page' not in temp.get("href")
            check6 = check5 and 'wikisource' not in temp.get("href")
            if '/wiki/' in temp.get("href") and check6:
                return True
    return False

# Randomly selects/returns a valid href given a list of link objects
def generateLink(links):
    searchingForLink = True;
    temp = ""
    while searchingForLink:
        randNum = random.randint(0, len(links) - 1)
        temp = links[randNum]
        if linkFilters(temp):
            searchingForLink = False
    return temp.get("href").split('/')[2]

# given all the 'a' elements in the html, sorts out all the valid links
# and plops them in a list which is returned
def sortLinks(links):
    results = []
    for link in links:
        if linkFilters(link):
            results.append(link.get("href").split('/')[2])
    return results

# given a list of link hrefs, returns a dict of 10 random links
# connected to a number, if the goal link is present
# it will randomly replace one of the 10 links with that one
# so the user can win
def getTenLinksOnPage(links, goal):
    results = {}
    filteredLinks = sortLinks(links)
    count = 0
    paths = min(10, len(filteredLinks))
    while count < paths:
        count += 1
        randNum = random.randint(0, len(filteredLinks) - 1)
        link = filteredLinks[randNum]
        filteredLinks.remove(link)
        results[count - 1] = {link.replace("_", " "): link}
    if goal in filteredLinks:
        randNum = random.randint(0, len(results))
        results[randNum] = {goal.replace("_", " "): goal}
    return results

# prints out the options
def reportKeysAndValues(links):
    for key, value in links.items():
        print(str(key) + ": " + value.keys()[0] + '\n')
        # value[value.keys()[0]]

def printPathResult(path):
    if (len(path) > 0):
        print "START: " + path[0]
    for i in range(1, len(path)):
        print str(i) + ': ' + path[i]

def getAGoal():
    goalFile = open('data.txt')
    content = goalFile.read()
    goalList = content.split('\n')
    randNum = random.randint(0, len(goalList) - 1)
    return goalList[randNum]


# plays a game, trying to get from one article to a goal article
def playGame():
    print ("Game")
    start = 'https://en.wikipedia.org/wiki/'
    print('Type in a starting point: ex: Klay Thompson')
    temp = raw_input()
    win = False
    goal = getAGoal()
    print ('You trying to get to ' + goal.replace("_", " ") + ' GOOD LUCK')
    temp.replace(" ", "_")
    res = requests.get(start + temp)
    steps = 0
    path = [temp]
    while not win:
        steps += 1
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        links = soup.select('a')
        paths = getTenLinksOnPage(links, goal)
        reportKeysAndValues(paths)
        print "Which path do you choose? ex. 0, 1, 2, 3, 4, etc..."
        choice = raw_input()
        choice = int(choice)
        path.append(paths[choice].keys()[0])
        if paths[choice][paths[choice].keys()[0]] == goal:
            win = True
        else:
            res = requests.get(start + paths[choice][paths[choice].keys()[0]])
    if steps == 1:
        print "YOU WON! It took you... " + str(steps) + " click to get there! DID YOU CHEAT?!?!?!?"
    else:
        print "YOU WON! It took you... " + str(steps) + " clicks to get there!"
    printPathResult(path)

# crawls wiki articles, randomly hopping link to link, prints results at the end
def crawl():
    print ("Crawl")
    start = "https://en.wikipedia.org/wiki/"
    print('Type in Something in Wikipedia, ex: Klay Thompson')
    temp = raw_input()
    print('How far would you like to crawl')
    num = raw_input()
    temp.replace(" ", "_")
    res = requests.get(start + temp)
    # uncomment the webbrowser lines if you want to see it in action
    # webbrowser.open(start + temp)
    storage = {}

    print ('Crawling... --------------- :|')
    for i in range(1, int(num) + 1):
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        links = soup.select('a')
        temp = generateLink(links)
        res = requests.get(start + temp)
        # webbrowser.open(start + temp)
        temp_2 = temp.replace("_", " ")
        # storing the article name
        if temp_2 in storage:
            storage[temp_2] += 1
        else:
            storage[temp_2] = 1
        print str(i) + " " + temp_2

    print '---------------Results--------------'
    sorted_storage = sorted(storage.items(), key=operator.itemgetter(1), reverse=True)
    # printing out the results of the trek
    results_file = open('results.txt', 'w')
    for item in sorted_storage:
        output = item[0] + ": " + str(item[1])
        results_file.write(output + '\n')
        print output

    print "------------------------------------"
    randNum = random.randint(0, len(storage) - 1)
    print("May I suggest reading about: " + sorted_storage[randNum][0])

print ('--------****-****----*$_$*______----')
print ('welcome to k24dizzles wikicrawler')
print ('would you like to 1) play a game or 2) just crawl')
print ('-*****^-------**************)_______')
choice = raw_input()
if choice == '1':
    playGame()
else:
    crawl()
