import requests, sys, webbrowser, bs4, random, operator, os

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
            check5 = check4 and 'Main_Page' not in temp.get("href")
            if '/wiki/' in temp.get("href") and check5:
                searchingForLink = False
    return temp.get("href").split('/')[2]

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
for i in range(int(num)):
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
