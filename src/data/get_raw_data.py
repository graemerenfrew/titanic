# -*- coding: utf-8 -*-
import requests
from requests import session
import os
from dotenv import load_dotenv, find_dotenv
import logging #so we can show users what's happening

# login then download...
payload = {
    'action':'login',
    'username': os.environ.get("KAGGLE_USERNAME"),
    'password': os.environ.get("KAGGLE_PASSWORD")
}

loginUrl = "https://www.kaggle.com/account/login"

def extract_data(url, file_path):
    ''' 
    extract data from kaggle
    '''
    #as before, do some antiforgery on the session
    #set up the http session to connect and get the data
    with session() as c:
        response = c.get(loginUrl).text
        AFToken = response[response.index('antiForgeryToken')+19:response.index('isAnonymous: ')-12]
        payload['__RequestVerificationToken']=AFToken
        c.post(loginUrl + '?IsModal=true&returnUrl=/', data=payload)
        # get request
        with open(file_path, 'wb') as handle:  #python3 needs wb, python2 only w
            response = c.get(url, stream=True)
            #print(response.text)
            for block in response.iter_content(1024):  #capture the data in k sized chunks
                handle.write(block)

def main(project_dir):
    '''
    main method
    '''
    #get a logger
    logger = logging.getLogger(__name__)
    logger.info('getting the raw data')
    
    # data source URLS
    train_url = 'https://www.kaggle.com/c/titanic/download/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/download/test.csv'
    
    #file paths for storing the data
    raw_data_path = os.path.join(os.path.pardir,'data','raw')
    train_data_path = os.path.join(raw_data_path,'train.csv')
    test_data_path = os.path.join(raw_data_path,'test.csv')

    #extract the data
    extract_data(train_url, train_data_path)
    extract_data(test_url, test_data_path)
    logger.info('downloaded raw training and test data')
    
if __name__ == '__main__':
    # get the root directory   - pardir is 'parent directory'
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    #set up logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    #now find the .env automatically by walking the directories
    dotenv_path = find_dotenv()
    #load the variables
    load_dotenv(dotenv_path)
    
    #call the main methods
    main(project_dir)