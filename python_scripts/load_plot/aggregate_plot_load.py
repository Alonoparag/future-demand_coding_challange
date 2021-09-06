from sqlalchemy import create_engine, Column, DateTime, Time, Integer, String, text#, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os


def writer(db_usrnm= None, db_psswd=None,db_host=None, db_name=None,action=None):
    """Wrapper function to create the plot or to load data to alsticsearch database

    Args:
        db_usrnm (string, optional): postgres
        db_psswd (string, optional): postgresserver password
        db_host (string, optional): postgres host address
        db_name (string, optional): database name
        action (string, optional): specify the action plot-image,elastic or both
    """
    engine=create_engine(f'postgresql+psycopg2://{db_usrnm}:{db_psswd}@{db_host}/{db_name}')
    Session=sessionmaker(bind=engine)
    
    Base=declarative_base()
    
    class Event(Base):
        """
        Mapper for the events table

        """
        __tablename__='events'
        event_id=Column(Integer, primary_key=True)
        date =Column(DateTime)
        time =Column(Time)
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
    
    s=Session()
    r=s.query(Event).all()
    if action=='elastic' or action=='both':
        es=Elasticsearch({'elasticsearch'})
        
        if not es.indices.exists('events'):
            actions=[{
                '_index':'events',
                '_type':'doc',
                '_source':{
                    'event_id': row.event_id,
                    'date': row.date,
                    'time': row.time if type(row.time) == str else row.time.strftime('%H:%M'),
                    'location': row.location,
                    'title': row.title,
                    'surtitle': row.surtitle,
                    'subtitle': row.subtitle,
                    'artists': row.artists,
                    'musical_pieces': row.musical_pieces,
                    'additional_information': row.additional_information,
                    'biography': row.biography,
                    'performance_times': row.performance_times,
                    'performance_duration': row.performance_duration,
                    'image_link': row.image_link,
                }} for row in r]

            helpers.bulk(es,actions)
    if action == 'plot-image' or action=='both':
        plt_dst=os.getcwd()+'/plots/'
        print('plotting in ',plt_dst)

        df=pd.read_sql_table('events',engine)
        aggregation={
        'Events':pd.NamedAgg(column='event_id',aggfunc='count')
        }
        events_agg=df.groupby(
            pd.Grouper(
                key='date',
                freq='D'
            )
        ).agg(**aggregation)
        fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(12,9))

        ax.bar(x=list(map(lambda x: x.strftime(r'%d.%m.%Y'),events_agg.index)), height=events_agg.Events, color='g')
        ax.set_title('Events per day',size='x-large',y=1.05)
        ax.set_xlabel('Date',size='x-large',y=-1.5)
        ax.set_ylabel('Number of events', rotation=90,size='x-large')
        ax.set_ylim([0,5])
        ax.grid(b=True, which='major',axis='y')
        plt.tight_layout(w_pad=0.5)

        try:
            plt.savefig(f'{plt_dst}events_per_day_fig.png',edgecolor='w', pad_inches=.5, bbox_inches='tight')            
        except FileNotFoundError:
            os.makedirs(plt_dst)
            plt.savefig(f'{plt_dst}events_per_day_fig.png',edgecolor='w', pad_inches=.5, bbox_inches='tight')


        
    
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--db-username',action='store',type=str,required=True,dest='db_usrnm')
    parser.add_argument('--db-password',action='store',type=str,required=True,dest='db_psswd')
    parser.add_argument('--database-name',action='store',type=str,required=True,dest='db_name')
    parser.add_argument('--db-host',action='store',type=str,required=True,dest='db_host')
    parser.add_argument('--action',action='store',type=str,choices=['plot-image','elastic','both'],required=True,dest='action')
    args=parser.parse_args()
    writer(**vars(args))