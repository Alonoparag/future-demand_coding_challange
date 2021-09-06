import requests
from selectorlib import Extractor
import datetime
import pandas as pd
from scrape_functions import format_data
from sqlalchemy import create_engine,Table ,Column, DateTime, Time, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import argparse
import os

def scrape_and_write(db_usrname=None,db_psswd=None,db_name=None,db_host=None):
    """
    Scraping wrapper to scrape events from lucernefestival
    site and insert them into a postgresql database
    
    
    Returns:
        pandas.core.DataFrame: A DataFrame object containg scraped and formatted data

    Args:
        db_usrname (string):database user name
        db_psswd (string):database password
        db_name (string):database name
    """
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' ,
        'Accept-Language':'en-US,en;q=0.5' ,
        'DNT':'1' ,
        'Connection':'keep-alive' ,
        'Upgrade-Insecure-Requests':'1' ,
        'Sec-Fetch-Dest':'document' ,
        'Sec-Fetch-Mode':'navigate' ,
        'Sec-Fetch-Site':'none' ,
        'Sec-Fetch-User':'?1',
    }
    with requests.Session() as s:
        s.headers=headers
        try:
            if not os.path.exists(f'{os.getcwd()}/scrape_logs/'):
                os.makedirs(f'{os.getcwd()}/scrape_logs/')
        except FileNotFoundError:
            os.makedirs(f'{os.getcwd()}/scrape_logs/')

        logfile=open(f'{os.getcwd()}/scrape_logs/log_{datetime.datetime.now()}.txt','w')
        url_home='https://www.lucernefestival.ch'
        url_f='https://www.lucernefestival.ch/en/program/forward-festival-21'
        s.headers=headers
        extractor_list=Extractor.from_yaml_file('lucerne_event_list.yml')
        extractor_event=Extractor.from_yaml_file('lucerne_event_details.yml')
        logfile.write('Scraping begin\n')
        r=s.get(url_f)
        logfile.write(f'url responded with {r.status_code}\n')
        events_list=extractor_list.extract(r.text)['event_links']
        logfile.write(f'{len(events_list)} events were found.\n')
        events_list=list(map(lambda x: url_home+x,events_list))
        raw_scrape_data=[extractor_event.extract(s.get(e).text) for e in events_list]
        
        
        
        try:
            connection_string=f'postgresql+psycopg2://{db_usrname}:{db_psswd}@{db_host}/{db_name}'
            engine=create_engine(connection_string)
            
            Base=declarative_base()
            
            class Event(Base):
                __tablename__='events'
                event_id =Column(Integer, primary_key=True)
                date =Column(DateTime)
                time =Column(String)
                location =Column(String)
                title =Column(String)
                surtitle =Column(String)
                subtitle =Column(String)
                artists =Column(String)
                musical_pieces =Column(String)  
                additional_information =Column(String)
                biography =Column(String)
                performance_times =Column(String)
                performance_duration =Column(String)
                image_link =Column(String)
                
            Base.metadata.create_all(engine)
            
            Session=sessionmaker(bind=engine)
            session=Session()
            event_object_list=[]
            for event in format_data(raw_scrape_data):
                e=Event(date=event['date'],
                        time=event['time'],
                        location=event['location'],
                        title=event['title'],
                        surtitle=event['surtitle'],
                        subtitle=event['subtitle'],
                        artists=event['artists'],
                        musical_pieces=event['musical_pieces'],
                        additional_information=event['additional_information'],
                        biography=event['biography'],
                        performance_times=event['performance_times'],
                        performance_duration=event['performance_duration'],
                        image_link=event['image_link'],)
                event_object_list.append(e)
            session.add_all(event_object_list)
            session.commit()
            
            
        except Exception as e:
            exception_text=f"""
                #####################\n
                Exception Occured
                Exception:\n\n
                {str(e)}\n\n
            """
            logfile.write(exception_text)
            raise e
    
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--db-username',action='store',type=str,required=True,dest='db_usrname')
    parser.add_argument('--db-password',action='store',type=str,required=True,dest='db_psswd')
    parser.add_argument('--db-host',action='store',type=str,required=True,dest='db_host')
    parser.add_argument('--database-name',action='store',type=str,required=True,dest='db_name')
    args=parser.parse_args()
    scrape_and_write(**vars(args))