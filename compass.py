import gspread
import csv
import os
import readline
import getpass
import json
from collections import defaultdict


class ResponseReader:

    CLASS_COL = 3 #The column recording the class (course section) in the spreadsheet

    def __init__(self, configFile=None, update = True):
        self._password = None
        if configFile:
            #Configure
            with open(configFile, 'r') as c:
                config = json.loads(c.read())
            self._uname = config['uname']
            self._docKey = config['docKey']
            self._password = config['password']
            self._csv = self._fetch_responses(update)
            return
        self._uname = self._get_uname()
        self._docKey = self._get_docKey()
        self._csv = self._fetch_responses(update)
        self._dump()
        

        
    def _get_uname(self):
        self._clear()
        return self._prompt('Enter gmail address associated with the form:\n\n\t')

    def _get_docKey(self):
        self._clear()
        return self._prompt('Copy/paste the doc key from the URL of your response sheet:\n\n\t')
   
   
    
    def _fetch_responses(self, update):
        self._clear()
        self._print('\t'+self._uname+'\n')
        
        if update:
            if self._password:
                passwd = self._password
            else:
                passwd = getpass.getpass()
            
            try:
                self._print('Retrieving spreadsheet from Google Drive...')
                gc = gspread.login(self._uname, passwd)
                responses = gc.open_by_key(self._docKey)
                sheet = responses.get_worksheet(0)
                copy = sheet.get_all_values()
                with open('responses.csv', 'w') as f:
                    csv.writer(f).writerows(copy)
            except:
                self._print('Failed!  Loading saved csv...')
                with open('responses.csv', 'r') as f:
                    copy = list(csv.reader(f))
        
        else:
            self._print('Working off saved csv...')
            with open('responses.csv', 'r') as f:
                copy = list(csv.reader(f))
        return copy
        
    def _dump(self):
        config = {}
        config['uname'] = self._uname
        config['docKey'] = self._docKey
        config['password'] = self._password
        with open('config.json', 'w') as c:
            c.write(json.dumps(config))
        return self
        
    def _clear(self):
        os.system('cls' if os.name=='nt' else 'clear') 
        return self

    def _print(self, string):
        print(string)

    def _prompt(self, string):
        return input(string)

    def __date_convert(self, date):
        temp = date.split('/')
        return '/'.join([temp[2], temp[0], temp[1]])

    def dates(self):
        return sorted(list(set([ x[0].split(' ')[0] for x in self.rows() ])))

    def labels(self):
        return self._csv[0]

    def rows(self):
        return [x for x in self._csv[1:]]

    def cols(self):
        return zip(*self.rows())

    def classes(self, date = None):
        classdict = defaultdict(list)
        if date:
            rows = self.rows_after_date(date)
        else:
            rows = self.rows()
        for x in rows:
            classdict[x[self.CLASS_COL]].append(x)
        return classdict
    
    def rows_after_date(self, date):
        return [x for x in self.rows() if self.__date_convert(date) <= self.__date_convert(x[0].split(' ')[0])]

    def cols_by_dates(self, date):
        return zip(*self.rows_after_date(date))
        


    
