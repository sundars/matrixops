from __future__ import print_function
import json
import requests
import random

class Oxford:
    appid = 'ef6388d2'
    appkey = '275e4baceefd617afe674d7fa37fd1d2'
    domainList = []
    urlBase = 'https://od-api.oxforddictionaries.com:443/api/v1/'
    language = 'en'
    wordList = []
    minWordLength = 7
    category = ''
    numberOfWords = 0
    wordInUse = None

    def __init__(self):
        self.domainList = ['Air Force', 'Alcoholic', 'American Civil War', 'American Football', 'Amerindian', 'Anatomy', 'Ancient History', 'Angling', 'Anthropology', 'Archaeology', 'Archery', 'Architecture', 'Art', 'Artefacts', 'Arts And Humanities', 'Astrology', 'Astronomy', 'Athletics', 'Audio', 'Australian Rules', 'Aviation', 'Ballet', 'Baseball', 'Basketball', 'Bellringing', 'Biblical', 'Billiards', 'Biochemistry', 'Biology', 'Bird', 'Bookbinding', 'Botany']
        self.domainList.extend(['Bowling', 'Bowls', 'Boxing', 'Breed', 'Brewing', 'Bridge', 'Broadcasting', 'Buddhism', 'Building', 'Bullfighting', 'Camping', 'Canals', 'Cards', 'Carpentry', 'Chemistry', 'Chess', 'Christian', 'Church Architecture', 'Civil Engineering', 'Clockmaking', 'Clothing', 'Coffee', 'Commerce', 'Commercial Fishing', 'Complementary Medicine', 'Computing', 'Cooking', 'Cosmetics', 'Cricket', 'Crime', 'Croquet', 'Crystallography', 'Currency', 'Cycling', 'Dance', 'Dentistry', 'Drink', 'Dyeing', 'Early Modern History', 'Ecclesiastical', 'Ecology', 'Economics', 'Education', 'Egyptian History', 'Electoral'])
        self.domainList.extend(['Electrical', 'Electronics', 'Element', 'English Civil War', 'Falconry', 'Farming', 'Fashion', 'Fencing', 'Film', 'Finance', 'Fire Service', 'First World War', 'Fish', 'Food', 'Forestry', 'Freemasonry', 'French Revolution', 'Furniture', 'Gambling', 'Games', 'Gaming', 'Genetics', 'Geography', 'Geology', 'Geometry', 'Glassmaking', 'Golf', 'Goods Vehicles', 'Grammar', 'Greek History', 'Gymnastics', 'Hairdressing', 'Handwriting', 'Heraldry', 'Hinduism', 'History', 'Hockey', 'Honour', 'Horology', 'Horticulture', 'Hotels', 'Hunting', 'Insect', 'Instrument', 'Intelligence', 'Invertebrate', 'Islam'])
        self.domainList.extend(['Jazz', 'Jewellery', 'Journalism', 'Judaism', 'Knitting', 'Language', 'Law', 'Leather', 'Linguistics', 'Literature', 'Logic', 'Lower Plant', 'Mammal', 'Marriage', 'Martial Arts', 'Mathematics', 'Measure', 'Mechanics', 'Medicine', 'Medieval History', 'Metallurgy', 'Meteorology', 'Microbiology', 'Military', 'Military History', 'Mineral', 'Mining', 'Motor Racing', 'Motoring', 'Mountaineering', 'Music', 'Musical Direction', 'Mythology', 'Napoleonic Wars', 'Narcotics', 'Nautical', 'Naval', 'Needlework', 'Numismatics', 'Occult', 'Oceanography', 'Office', 'Oil Industry', 'Optics'])
        self.domainList.extend(['Palaeontology', 'Parliament', 'Pathology', 'Penal', 'People', 'Pharmaceutics', 'Philately', 'Philosophy', 'Phonetics', 'Photography', 'Physics', 'Physiology', 'Plant', 'Plumbing', 'Police', 'Politics', 'Popular Music', 'Postal', 'Pottery', 'Printing', 'Professions', 'Prosody', 'Psychiatry', 'Psychology', 'Publishing', 'Racing', 'Railways', 'Rank', 'Relationships', 'Religion', 'Reptile', 'Restaurants', 'Retail', 'Rhetoric', 'Riding', 'Roads', 'Rock'])
        self.domainList.extend(['Roman Catholic Church', 'Roman History', 'Rowing', 'Royalty', 'Rugby', 'Savoury', 'Scouting', 'Second World War', 'Shoemaking', 'Sikhism', 'Skateboarding', 'Skating', 'Skiing', 'Smoking', 'Snowboarding', 'Soccer', 'Sociology', 'Space', 'Sport', 'Statistics', 'Stock Exchange', 'Surfing', 'Surgery', 'Surveying', 'Sweet', 'Swimming', 'Tea', 'Team Sports', 'Technology', 'Telecommunications', 'Tennis', 'Textiles', 'Theatre', 'Theology', 'Timber', 'Title', 'Tools', 'Trade Unionism', 'Transport', 'University', 'Variety', 'Veterinary', 'Video', 'War Of American Independence', 'Weapons', 'Weightlifting', 'Wine', 'Wrestling', 'Yoga', 'Zoology'])

        self.wordList = []
        while len(self.wordList) is 0:
            domainIndex = random.randint(0, len(self.domainList)-1)
            url = self.urlBase + 'wordlist/' + self.language + '/domains={0:s}?word_length=>{1:d}'.format(
                  self.domainList[domainIndex], self.minWordLength)
            try:
                response = self.GetRequest(url)
                results = dict(response.json())['results']
                metadata = dict(response.json())['metadata']

                self.category = self.domainList[domainIndex]
                self.numberOfWords = metadata['total']

                if self.numberOfWords > 0:
                    for result in results:
                        try:
                            word = dict()
                            word['word'] = '{0:s}'.format(result['word'])
                            word['id'] = '{0:s}'.format(result['id'])

                            if len([c for c in word['word'] if c in ' -_']) is 0:
                                self.wordList.append(word)

                        except Exception as e:
                            pass

            except Exception as e:
                print(e)

    def GetRequest(self, url):
        headers = {'app_id': self.appid, 'app_key': self.appkey}
        response = requests.get(url, headers = headers)
        if response.status_code != 200:
            raise Exception("Request to Oxford APIs failed. Request: <{0:s}>, Response: <{1:s}>".format(url, response.text))

        return response

    def GetEntry(self):
        url = self.urlBase + 'entries/' + self.language + '/' + self.wordInUse['id'].lower()

        try:
            response = self.GetRequest(url)
            results = dict(response.json())['results']
            lexicalEntries = results[0]['lexicalEntries']
            for lexicalEntry in lexicalEntries:
                entries = lexicalEntry['entries']
                for entry in entries:
                    if 'senses' in entry:
                        lexCat = lexicalEntry['lexicalCategory'].encode('utf-8')
                        defn = entry['senses'][0]['definitions'][0].encode('utf-8')

                        try:
                            retVal = '[{0:s}] - {1:s}'.format(lexCat, defn)
                        except Exception as e:
                            retVal = '[{0:s}] - {1:s}'.format(lexCat.decode('utf-8'), defn.decode('utf-8'))

                        return retVal

        except Exception as e:
            print(e)
            return ''

    def ChangeCategory(self, category=''):
        self.wordList = []
        while len(self.wordList) == 0:
            domainIndex = -1
            try:
                if category != '':
                    domainIndex = [d.lower() for d in self.domainList].index(category.lower())
                    category = ''

            except ValueError as e:
                print("Category <{0:s}> is not one of Oxford dictionary's word categories. ".format(category), end='')
                dList = [d.lower() for d in self.domainList]
                for domain in dList:
                    if domain.find(category.lower()) > -1 or category.lower().find(domain) > -1:
                        domainIndex = dList.index(domain)

            if domainIndex == -1:
                domainIndex = random.randint(0, len(self.domainList)-1)
                while self.category == self.domainList[domainIndex]:
                    domainIndex = random.randint(0, len(self.domainList)-1)

            url = self.urlBase + 'wordlist/' + self.language + '/domains={0:s}?word_length=>{1:d}'.format(
                  self.domainList[domainIndex], self.minWordLength)

            try:
                response = self.GetRequest(url)
                results = dict(response.json())['results']
                metadata = dict(response.json())['metadata']

                self.category = self.domainList[domainIndex]
                self.numberOfWords = metadata['total']

                if self.numberOfWords > 0:
                    for result in results:
                        try:
                            word = dict()
                            word['word'] = '{0:s}'.format(result['word'])
                            word['id'] = '{0:s}'.format(result['id'])

                            if len([c for c in word['word'] if c in ' -_']) is 0:
                                self.wordList.append(word)

                        except Exception as e:
                            pass

            except Exception as e:
                print(e)
                return ''

        print("Changing category to <{0:s}>".format(self.category))
        return self.category

    def GetWord(self):
        oldWord = ''
        if self.wordInUse != None:
            oldWord = self.wordInUse['word']
            self.wordInUse = None

        tries = 0

        randPos = random.randint(0, len(self.wordList)-1)
        self.wordInUse = self.wordList[randPos]
        tries += 1
        while len([c for c in self.wordInUse['word'] if c in ' -_']) is not 0 or self.wordInUse['word'] == oldWord or tries < 3:
            randPos = random.randint(0, len(self.wordList)-1)
            self.wordInUse = self.wordList[randPos]
            tries += 1

        if self.wordInUse['word'] == oldWord:
            self.ChangeCategory()
            self.GetWord()

        return self.wordInUse['word']

    def GetCategory(self):
        return self.category
