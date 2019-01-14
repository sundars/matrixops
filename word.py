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
    minWordLength = 5
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

        domainIndex = random.randint(0, len(self.domainList)-1)
        url = self.urlBase + 'wordlist/' + self.language + '/domains={0:s}?word_length=>{1:d}'.format(self.domainList[domainIndex],
                                                                                                      self.minWordLength)
        try:
            response = self.GetRequest(url)
            results = dict(response.json())['results']
            metadata = dict(response.json())['metadata']

            self.category = self.domainList[domainIndex]
            self.numberOfWords = metadata['total']

            for result in results:
                word = dict()
                word['word'] = '{0:s}'.format(result['word'])
                word['id'] = '{0:s}'.format(result['id'])

                self.wordList.append(word)

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
            retVal = '[{0:s}] - {1:s}'.format(results[0]['lexicalEntries'][0]['lexicalCategory'],
                                              results[0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0])
            return retVal

        except Exception as e:
            print(e)
            return ''

    def ChangeCategory(self):
        domainIndex = random.randint(0, len(self.domainList)-1)
        while self.category == self.domainList[domainIndex]:
            domainIndex = random.randint(0, len(self.domainList)-1)

        url = self.urlBase + 'wordlist/' + self.language + '/domains={0:s}?word_length=>{1:d}'.format(self.domainList[domainIndex],
                                                                                                      self.minWordLength)

        try:
            response = self.GetRequest(url)
            results = dict(response.json())['results']
            metadata = dict(response.json())['metadata']

            self.category = self.domainList[domainIndex]
            self.numberOfWords = metadata['total']

            for result in results:
                word = dict()
                word['word'] = '{0:s}'.format(result['word'])
                word['id'] = '{0:s}'.format(result['id'])

                self.wordList.append(word)

            return self.category

        except Exception as e:
            print(e)
            return ''

    def GetWord(self):
        randPos = random.randint(0, len(self.wordList))
        self.wordInUse = self.wordList[randPos]
        while ' ' in self.wordInUse['word']:
            randPos = random.randint(0, len(self.wordList))
            self.wordInUse = self.wordList[randPos]

        return self.wordInUse['word']

    def GetCategory(self):
        return self.category
