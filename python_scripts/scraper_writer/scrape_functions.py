import re
import datetime

def format_musical_pieces(in_l):
    """helper function to remove encoded chararcters from musical_pieces

    Args:
        in_l list of strings

    Returns:
        string representing musical pieces
    """
    return re.sub('\\xa0',' ',', '.join(in_l))

def format_image_link(in_d):
    """formats the image link for a given

    Args:
        in_d (dict): ictionary with css styles

    Returns:
        string: image url
    """
    return re.findall('https.*\\)',in_d['image_style'])[0][:-1]

def format_performance_times(in_s):
    """Given performance times for an artist, format the times into 24h format datetime.time objects

    Args:
        in_s (string):string of performance times

    Returns:
        string of performance times seperated by [', ']
    """
    n_str=in_s[7:-5]
    n_str=re.sub('\\xa0','',n_str)
    n_str=re.sub(' p.m. ','|',n_str)
    n_l=n_str.split('a.m.')
    n_am=n_l[0].split('|')
    n_am=list(map(lambda x: x.strip(),n_am))
    n_pm=list(map(lambda x:str(round(float(x.strip())+12,2)),n_l[1].split('|')))
    n_am.extend(n_pm)
    n_l=[]
    for ind,t in enumerate(n_am):
        if len(t)==4:
            if float(t)==0 and round(float(n_am[ind+1])) == 10:
                n_l.append(format_time('1'+t).strftime('%H:%M'))
            else:
                n_l.append(format_time(t+'0').strftime('%H:%M'))
        else:
            n_l.append(format_time(t).strftime('%H:%M'))
    return ', '.join(n_l)

def format_date(in_date_s,in_time_s):
    """Format date entries from strings into datetime.date objects

    Args:
        in_date_s (string): date string
        in_time_s (string): time string

    Returns:
        datetime.datetime: full date of evnet
    """
    date_list=list(map(lambda x:int(x),in_date_s.split(',')[1].split('.')[:-1]))
    time_list=list(map(lambda x:int(x),in_time_s.split('.')))
    year=2021
    month=date_list[1]
    day=date_list[0]
    hour=time_list[0]
    minute=time_list[1]
    return datetime.datetime(year,month,day,hour,minute)
    
def format_time(in_s):
    """formats time given in string to datetime.time objects

    Args:
        in_s (string): strings as hh.mm

    Returns:
        datetime.time
    """
    time_list=list(map(lambda x:int(x),in_s.split('.')))
    return datetime.time(*time_list)
       
def format_data(in_d):
    """Wrapper function for data formatting

    Args:
        in_d (dict): scrapped data from festival page

    Returns:
        dict: formatted dict
    """
    for i in in_d:
        if type(i['musical_pieces']) == list:
            i['musical_pieces']=format_musical_pieces(i['musical_pieces'])
        if type(i['image_link'])==dict:
            i['image_link']=format_image_link(i['image_link'])
        if i['performance_duration']:
            i['performance_duration']=i['performance_duration'][9:]
        if i['performance_times']:
            i['performance_times']=format_performance_times(i['performance_times'])
        if i['additional_information']:
            new_str=re.sub('\\xa0',' ',' '.join(i['additional_information']))
            i['additional_information']=new_str
        if i['artists']:
            i['artists']=', '.join(i['artists'])
        i['date']=format_date(i['date'],i['time'])
        i['time']=format_time(i['time'])
    return in_d