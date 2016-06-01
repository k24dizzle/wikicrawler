#!/usr/bin/python

import requests, webbrowser, bs4, random, operator, os

defaultPrompt = '... '
baseUrl = "https://en.wikipedia.org/wiki/"

# Can use this to update the difficulty settings
difficulties = {
    1: 'easy.txt',
    2: 'medium.txt',
    3: 'hard.txt'
}

# prints out the 'path' options
def reportKeysAndValues(links):
    for i in xrange(len(links)):
        print('%s : %s' %(i, links[i]))

# Given a min and max, asks the user for an int between this range
# and returns it
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

# Asks the user for a string and returns it
def getStrInput(prompt=defaultPrompt):
    while True:
        user_input = raw_input(prompt)
        if user_input:
            return user_input
        else:
            print 'what the heck'

# Returns a goal given a user inputted difficulty
def getAGoal():
    diff = getIntInput(1, len(difficulties))
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
        self.current = start # current page the user is on
        self.path = [start.name] # path that the user takes
        self.goal = goal # goal page the user wants to reach
        self.steps = 0 # counts the user's score
        self.win = False # have you won yet?

    # given an article name, updates the path, steps, and
    # winning status, if the article name isn't the goal
    # will update the current article
    def clickPage(self, name):
        self.path.append(name)
        self.steps += 1
        if name == self.goal.name:
            self.win = True
        else:
            self.current = WikiPage.fromName(name)

    # Given a list of article names, prints them out
    # to the console in formatted style
    def printPathResult(self):
        if (len(self.path) > 0):
            print "START: " + self.path[0]
        for i in range(1, len(self.path)):
            print str(i) + ': ' + self.path[i]

    # gathers 10 random article names on the current page
    # if the goal article is there will randomly nestle it
    # within the list
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
        self.href = href
        self.soup = bs4.BeautifulSoup(requests.get(baseUrl + self.href).text, 'html.parser')

    # returns all the hrefs in the content part of the page
    def getHrefs(self):
        return [link.get('href') for link in self.soup.select('#content a')]

    # returns all the hrefs that match the filters
    def getFilteredHrefs(self):
        return [href.split('/')[2] for href in self.getHrefs() if self.filterHref(href)]

    badLinks = (':', 'wikipedia', 'Wikipedia', 'wikimedia', 'Main_Page', 'wikisource', 'wiktionary')

    # returns true if the href fits the given filters
    def filterHref(self, href):
        if href is None:
            return False
        for check in self.badLinks:
            if check in href:
                return False
        return '/wiki/' in href

    def getRandomHref(self):
        filteredHrefs = self.getFilteredHrefs()
        randNum = random.randint(0, max(len(filteredHrefs) - 1, 1))
        return filteredHrefs[randNum]

    # creates a WikiPage given a link
    @classmethod
    def fromLink(cls, link):
        return cls(link.get('href'))

    # creates a WikiPage given an article name
    @classmethod
    def fromName(cls, name):
        return cls(name.replace(' ', '_'))

# plays a game, trying to get from one article to a goal article
def playGame():
    print 'Choose a difficulty 1) EZ 2) Medium 3) Hard'
    goal = getAGoal()
    print('::::: Type in a starting point: ex: Klay Thompson :::::')
    startPage = getStrInput()
    startWikiPage = WikiPage.fromName(startPage)
    goalWikiPage = WikiPage.fromName(goal)
    print ('You trying to get to ***- %s -***' %(goalWikiPage.name))
    print ('Good Luck!')
    game = WikiGame(startWikiPage, goalWikiPage)

    while not game.win:
        print '--------------------'
        paths = game.gatherTen()
        reportKeysAndValues(paths)
        print "Which path do you choose? ex. 0, 1, 2, 3, 4, etc..."
        choice = getIntInput(0, len(paths) - 1)
        game.clickPage(paths[choice])
    print '------------------'
    if game.steps == 1:
        print "YOU WON! It took you... %s click to get there! DID YOU CHEAT?!?!?!?" % (game.steps)
    else:
        print "YOU WON! It took you... %s clicks to get there!" % (game.steps)
    game.printPathResult()

# crawls wiki articles, randomly hopping link to link, prints results at the end
def crawl():
    print('::::: Type in Something in Wikipedia, ex: Klay Thompson :::::')
    currentPage = WikiPage.fromName(getStrInput())
    print('How far would you like to crawl')
    num = getIntInput(1, 24242424)
    res = requests.get(baseUrl + currentPage.href)
    # uncomment the webbrowser lines if you want to see it in action
    # webbrowser.open(baseUrl + temp)
    storage = {currentPage.name: 1}
    print ('Crawling... --------------- :|')
    print 'START: %s' % (currentPage.name)

    for i in range(1, num + 1):
        newHref = currentPage.getRandomHref()
        currentPage = WikiPage(newHref)
        res = requests.get(baseUrl + currentPage.href)
        # storing the article name
        if currentPage.name in storage:
            storage[currentPage.name] += 1
        else:
            storage[currentPage.name] = 1
        print str(i) + " " + currentPage.name

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
print ('------------------------------------')
choice = getIntInput(1, 2)
if choice == 1:
    playGame()
else:
    crawl()
