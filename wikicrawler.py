#!/usr/bin/python

import requests, sys, webbrowser, bs4, random, operator, os

defaultPrompt = '... '
baseUrl = "https://en.wikipedia.org/wiki/"

# returning if a link is legit or not (true or false)
def linkFilters(link):
    hr = link.get('href')
    if hr is not None:
        bad = (':', 'wikipedia', 'Wikipedia', 'wikimedia', 'Main_Page', 'wikisource', 'wiktionary')
        for s in bad:
            if s in hr:
                return False
        if '/wiki/' in hr:
            return True
    return False

# Randomly selects/returns a valid href given a list of link objects
def generateLink(links):
    while True:
        randNum = random.randint(0, len(links) - 1)
        link = links[randNum]
        if linkFilters(link):
            return link.get("href").split('/')[2]

# given all the 'a' elements in the html, sorts out all the valid links
# and plops them in a list which is returned
def sortLinks(links):
    results = [link.get('href').split('/')[2] for link in links if linkFilters(link)]
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
        randNum = random.randint(0, len(filteredLinks) - 1)
        link = filteredLinks[randNum]
        filteredLinks.remove(link)
        results[count] = {link.replace("_", " "): link}
        count += 1
    if goal in filteredLinks:
        randNum = random.randint(0, len(results))
        results[randNum] = {goal.replace("_", " "): goal}
    return results

# prints out the options
def reportKeysAndValues(links):
    for i in xrange(len(links)):
        print('%s : %s' %(i, links[i]))

def printPathResult(path):
    if (len(path) > 0):
        print "START: " + path[0]
    for i in range(1, len(path)):
        print str(i) + ': ' + path[i]

def getIntInput(minny=0, maxxy=None, prompt=defaultPrompt):
    while True:
        user_input = getStrInput(prompt)
        try:
            int_val = int(user_input)
            if (int_val >= minny and int_val <= maxxy):
                return int_val
            else:
                print 'HEY! Need a number between %s and %s' % (minny, maxxy)
        except ValueError:
            print "YO! That's not a number"

def getStrInput(prompt=defaultPrompt):
    while True:
        user_input = raw_input(prompt)
        if user_input:
            return user_input
        else:
            print 'what the heck'

difficulties = {
    1: 'easy.txt',
    2: 'medium.txt',
    3: 'hard.txt'
}
def getAGoal():
    diff = getIntInput(1, 3)
    goalFile = open(difficulties[diff])
    content = goalFile.read()
    goalList = content.split('\n')
    # filters out all empty strings in goalList (0 = False boolean)
    goalList = filter(len, goalList)
    randNum = random.randint(0, len(goalList) - 1)
    return goalList[randNum]

class WikiGame(object):
    # accepts a start wikipage and a goal wikipage
    def __init__(self, start, goal):
        self.current = start
        self.path = [start.name]
        self.goal = goal
        self.steps = 0
        self.win = False

    def clickPage(self, name):
        self.path.append(name)
        self.steps += 1
        if name == self.goal.name:
            self.win = True
        else:
            self.current = WikiPage.fromName(name)

    def gatherTen(self):
        hrefs = self.current.getFilteredHrefs()
        results = []
        paths = min(10, len(hrefs))
        while len(results) < paths:
            randNum = random.randint(0, len(hrefs) - 1)
            temp_href = hrefs[randNum]
            results.append(temp_href.replace('_', ' '))
            hrefs.remove(temp_href)
        if self.goal.href.split('/')[-1] in hrefs:
            randNum = random.randint(0, len(results) - 1)
            results[randNum] = self.goal.name
        return results

class WikiPage(object):
    def __init__(self, href):
        self.name = href.replace('_', ' ')
        self.href = baseUrl + href
        self.soup = bs4.BeautifulSoup(requests.get(self.href).text, 'html.parser')

    def getHrefs(self):
        return [link.get('href') for link in self.soup.select('#content a')]

    def getFilteredHrefs(self):
        return [href.split('/')[2] for href in self.getHrefs() if self.filterHref(href)]

    badLinks = (':', 'wikipedia', 'Wikipedia', 'wikimedia', 'Main_Page', 'wikisource', 'wiktionary')

    def filterHref(self, href):
        if href is None:
            return False
        for check in self.badLinks:
            if check in href:
                return False
        return '/wiki/' in href

    @classmethod
    def fromLink(cls, link):
        return cls(link.get('href'))

    @classmethod
    def fromName(cls, name):
        return cls(name.replace(' ', '_'))

# plays a game, trying to get from one article to a goal article
def playGame():
    print 'Choose a difficulty 1) EZ 2) Medium 3) Hard'
    goal = getAGoal()
    print('Game::::: Type in a starting point: ex: Klay Thompson :::::')
    startPage = getStrInput()
    print ('You trying to get to ' + goal.replace("_", " ") + ' GOOD LUCK')
    startWikiPage = WikiPage.fromName(startPage)
    goalWikiPage = WikiPage.fromName(goal)
    game = WikiGame(startWikiPage, goalWikiPage)

    while not game.win:
        paths = game.gatherTen()
        reportKeysAndValues(paths)
        print "Which path do you choose? ex. 0, 1, 2, 3, 4, etc..."
        choice = raw_input()
        choice = int(choice)
        game.clickPage(paths[choice])

    if game.steps == 1:
        print "YOU WON! It took you... " + str(game.steps) + " click to get there! DID YOU CHEAT?!?!?!?"
    else:
        print "YOU WON! It took you... " + str(game.steps) + " clicks to get there!"
    printPathResult(game.path)

# crawls wiki articles, randomly hopping link to link, prints results at the end
def crawl():
    print('Crawl::::: Type in Something in Wikipedia, ex: Klay Thompson :::::')
    print '~~~~~~~~>',
    temp = raw_input()
    print('How far would you like to crawl')
    num = raw_input()
    temp.replace(" ", "_")
    res = requests.get(baseUrl + temp)
    # uncomment the webbrowser lines if you want to see it in action
    # webbrowser.open(baseUrl + temp)
    storage = {}

    print ('Crawling... --------------- :|')
    for i in range(1, int(num) + 1):
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        links = soup.select('a')
        temp = generateLink(links)
        res = requests.get(baseUrl + temp)
        # webbrowser.open(baseUrl + temp)
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
"""
print ('--------****-****----*$_$*______----')
print ('welcome to k24dizzles wikicrawler')
print ('would you like to 1) play a game or 2) just crawl')
print ('------------------------------------')
choice = getIntInput(1, 2)
if choice == 1:
    playGame()
else:
    crawl()
    """
a = WikiPage('Roman Empire')
c = WikiPage('Rome')
b = WikiGame(a, c)

