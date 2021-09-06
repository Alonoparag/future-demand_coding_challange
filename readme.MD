# Code Challange by future-demand
### Alon Parag, Sep 2021

## The Challange:
* Write a script to crawl events from a clients website (date, time, location, title, artists, works, image link
* everything that possible)
* Insert data into database (PostgresSQL), with a self-defined schema
* The script, after crawling, should extract the data from the database and plot the data. The plot should show the total events of each day.
* The solution must be dockerized (including the database). It is recommended to use docker-compose. The repository should include a README with the instruction to run the project.
* Source: https://www.lucernefestival.ch/en/program/forward-festival-2

## Approach:
* 4 docker containers in a network:
  * a container for postgresql server
  * container for elasticsearch
  * container for kibana
  * container that runs the scripts to crawl, insert into the postgres database and perform further actions - aggregate and plot and\or load into elasticsearch database.

## Project outline
```
root
├── db
│   ├── Dockerfile
│   ├── init-db
│   │   └── init-db.sql
│   └── shell_scripts
│       └── alias.sh
├── docker-compose.yml
├── es-data
├── plots
├── postgres-data
├── python_scripts
│   ├── Dockerfile
│   ├── load_plot
│   │   └── aggregate_plot_load.py
│   ├── requirements.txt
│   ├── scraper_writer
│   │   ├── lucerne_event_details.yml
│   │   ├── lucerne_event_list.yml
│   │   ├── __pycache__
│   │   │   └── scrape_functions.cpython-39.pyc
│   │   ├── scrape_and_write.py
│   │   ├── scrape_functions.py
│   │   └── scrape_logs
│   └── shell_scripts
│       └── alias.sh
└── readme.MD

```

## Set up
1. execute `docker-compose up from root folder`
2. execute `docker exec postgres /db/shell_scripts/alias.sh && docker exec future_app shell_scripts/alias.sh`

## Use:
* executing `docker exec future_app scrape_write` will scrape the events from the "Forward Festival" page and load them into the postgres database.
* executing `docker exec postgres check_db` will perform the following query as a intermediate test: `SELECT event_id, date, time, title FROM events LIMIT 3`
* The command `docker exec future_app aggregate_load {plot-image, elastic, both}` either plots the total events per day to `/plots/` and\\or loads the data from the postgresql server to the elasticsearch server.
* elasticsearch could be visualized with kibana at `localhost:5601`

## Ploting in Kibana:
1. On the menu button on the top left corner, click on 'Discover'
2. Click on 'Create Index Pattern'
3. insert 'events' in 'Index pattern name' and click on 'Next step'
4. choose 'date' as time field and click on 'Create index pattern'
5. Open the menu again and click on 'Visualize Library', and click on 'Lens'
6. On the right side, on the dates pane, click on 'Show Dates'
7. In the dialog box, click on the tab 'Absolute'
8. Insert the date range of 19.11.2021 00:00 - 22.11.2021 00:00 and click on 'Update'
9. On the right side, click on 'horizontal axis' and choose 'date histogram', switch 'Custom time interval' On and choose '1 days'
10. Click on 'Vertical axis', select 'Count'. you may rename the field to 'Number of events'
11. Click on Save on the top right corner.