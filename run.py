""" 

Craigslist-Crawler
Matt VerLee
mtverlee@mavs.coloradomesa.edu
https://github.com/mtverlee/

"""

# Import modules.
import requests
from bs4 import BeautifulSoup as bs4
import os
import time
from termcolor import colored
import notifications.main as notifications

# Settings.
periodInMinutes = 60
appToken = ""
userToken = ""
emailUsername = ""
emailPassword = ""
subject = "Craigslist-Crawler"
emailRecipient = ""

# Main function.
def checkForListings(url, listingStorageFile, crawlerName, sendNotification, sendEmail):
        print('- ' + crawlerName + ' -')
        print("Starting query...")
        print("Time: " + time.strftime("%c"))
        print("URL: " + url)
        rsp = requests.get(url)
        html = bs4(rsp.text, 'html.parser')
        listings = html.find_all('li', attrs={'class': 'result-row'})
        totalListings = str(len(listings))
        print(colored('Listings: ' + str(len(listings)), 'blue'))

        if not os.path.exists(listingStorageFile):
            os.mknod(listingStorageFile)
            tempOpen = open(listingStorageFile, 'w')
            tempOpen.write("0")
            tempOpen.close()
        if os.stat(listingStorageFile).st_size == 0:
            tempOpen = open(listingStorageFile, 'w')
            tempOpen.write("0")
            tempOpen.close()
        if not os.access(listingStorageFile, os.W_OK):
            print("File to record past listings for this URL is not writeable - records will fail to be written.")

        pastListings = open(listingStorageFile, 'r').read()
        listingRecord = open(listingStorageFile, 'w')
        newListings = int(totalListings) - int(pastListings)
        if newListings < 0:
            newListings = 0
        if newListings >= 1:
            print(colored("New Listings: " + str(newListings), 'green'))
        else:
            print(colored("New Listings: " + str(newListings), 'red'))

        if newListings == 1:
            notificationMessage = 'There is a new listing at ' + url + '. (' + crawlerName + ')'
        if newListings > 1:
            notificationMessage = 'There are ' + str(newListings) + ' new listings at ' + url + '. (' + crawlerName + ')'
        if newListings == 0:
            notificationMessage = ' - There are no new listings. (' + crawlerName + ')'

        if newListings:
            listingRecord.truncate()
            listingRecord.write(str(totalListings))
            listingRecord.close()
            if sendNotification:
                notifications.sendPushoverNotification(appToken, userToken, notificationMessage, subject)
            if sendEmail:
                if not notifications.sendEmail(emailRecipient, subject, notificationMessage, emailUsername, emailPassword):
                    print(colored("Email to " + emailRecipient + " sent successfully.", 'white'))
                else:
                    print(colored("Email to " + emailRecipient + " had trouble sending.", 'red'))

            print(" ")
            print(" ")
        else:
            listingRecord.truncate()
            listingRecord.write(str(totalListings))
            listingRecord.close()
            print (" ")

# Run main function.
if __name__ == '__main__':
    notifications.sendPushoverNotification(appToken, userToken, 'The Craigslist Crawler is starting up.', 'Craigslist-Crawler')
    while True:
        checkForListings('https://westslope.craigslist.org/search/jjj?excats=12-1-2-1-7-1-1-1-1-1-19-1-1-3-2-3-2-2-39-25-1-1-1-1-1-1&search_distance=15&postal=81501', 'techListings.txt', 'Technology Jobs', True, False)
        checkForListings('https://westslope.craigslist.org/search/jjj?search_distance=10&postal=81501&employment_type=2', 'generalPartTimeListings.txt', 'General Part-Time Jobs', True, False)
        #checkForListings('https://westslope.craigslist.org/search/apa?hasPic=1&search_distance=10&postal=81501&max_price=700&availabilityMode=0', 'housingListings.txt', 'Housing', True, False)
        checkForListings('https://westslope.craigslist.org/search/jjj?search_distance=10&postal=81501', 'generalListings.txt', 'General Jobs', True, False)
        checkForListings('https://denver.craigslist.org/search/jjj?excats=11-1-1-2-1-7-1-1-1-1-1-19-1-1-1-2-2-3-2-2-14-25-25-1-1-1-1-1-1&is_telecommuting=1', 'denverTechRemoteListings.txt', 'Denver Technology Remote Jobs', True, False)
        checkForListings('https://denver.craigslist.org/search/cta?hasPic=1&searchNearby=2&nearbyArea=319&nearbyArea=210&nearbyArea=713&nearbyArea=287&nearbyArea=288&nearbyArea=320&max_price=7000&auto_make_model=toyota+tacoma&max_auto_miles=175000&condition=10&condition=20&condition=30&condition=40&condition=50', 'tacomaListings.txt', 'Tacoma Listings', True, True)
        checkForListings('https://denver.craigslist.org/search/cta?hasPic=1&searchNearby=2&nearbyArea=319&nearbyArea=210&nearbyArea=713&nearbyArea=287&nearbyArea=288&nearbyArea=320&max_price=7000&auto_make_model=toyota+4runner&max_auto_miles=175000&condition=10&condition=20&condition=30&condition=40&condition=50', '4runnerListings.txt', '4Runner Listings', True, True)
        print("Sleeping for " + str(periodInMinutes) + " minutes...")
        print(" ")
        time.sleep(periodInMinutes * 60)