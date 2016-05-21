import requests, sys, webbrowser, bs4, random, operator, os

def linkFilters(temp):
    if temp.get("href") != None:
            check = ':' not in temp.get("href")
            check2 = check and 'wikipedia' not in temp.get("href")
            check3 = check2 and 'Wikipedia' not in temp.get("href")
            check4 = check3 and 'wikimedia' not in temp.get("href")
            check5 = check4 and 'Main_Page' not in temp.get("href")
            if '/wiki/' in temp.get("href") and check5:
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

def sortLinks(links):
    results = []
    for link in links:
        if linkFilters(link):
            results.append(link.get("href").split('/')[2])
    return results

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
        results[randNum] = {goal: goal}
    return results

def reportKeysAndValues(links):
    for key, value in links.items():
        print(str(key) + ": " + value.keys()[0] + '\n')
        # value[value.keys()[0]]

def playGame():
    start = 'https://en.wikipedia.org/wiki/'
    print('Type in a starting point: ex: Klay Thompson')
    temp = raw_input()
    win = False
    goal = "Rome"
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
        path.append(paths[choice][paths[choice].keys()[0]])
        if paths[choice][paths[choice].keys()[0]] == goal:
            win = True
        else:
            res = requests.get(start + paths[choice][paths[choice].keys()[0]])
    print "YOU WON! It took you... " + str(steps) + " paths to get there!"
    print path

def crawl():
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

playGame()
