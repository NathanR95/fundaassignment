import requests
import json
from collections import Counter

def get_most_common_agents(url_addition=''):

    #starting conditions
    key = 'secret'
    is_last_page = False
    page = 1
    objects = []

    while not is_last_page:
    #get the listing objects from every page and add to objects list

        url = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/json/{}/?type=koop&zo=/amsterdam{}/&page={}&pagesize=200'.format(key, url_addition, page)

        #get real estate information from api
        print('Retrieving page {}...'.format(page), end='\r')

        r = requests.get(url)

        #try the request again in case of error
        while r.status_code != 200:
            r = requests.get(url)
        
        json_response = json.loads(r.text)
        new_objects = json_response['Objects']

        #check for last page
        if new_objects != []:
            objects += new_objects
            page += 1
        else:
            is_last_page = True

    print('Listings are in...\nProceed with listing the real estate agents...')

    #add real estate agents to list
    rea_list = []
    for object in objects:
        rea_list.append(object['MakelaarNaam'])

    print('Determining most common agencies...')
    #count and order occurences
    c = Counter(rea_list)

    #output the results
    print('Results:')
    rank = 1
    for record in c.most_common(10):
        print(str(rank)+'. ' + record[0] + ', Amount of listings: '+ str(record[1]))
        rank += 1

if __name__ == '__main__':

    #get the agency with most listings in amsterdam
    print('Start finding real estate agents with most listings in Amsterdam')
    get_most_common_agents()

    #get agency with most listings with a garden in amsterdam
    print('\nStart finding real estate agents with most listings with a garden in Amsterdam')
    get_most_common_agents('/tuin')