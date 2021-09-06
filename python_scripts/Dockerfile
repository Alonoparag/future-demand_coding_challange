FROM python:3.9.1

USER root
ENV PYTHONPATH "${PYTHONPATH}:/src"
RUN apt-get update
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY scraper_writer /code/
COPY load_plot /code/
COPY shell_scripts /code/shell_scripts/
RUN chmod -R 555 /code/shell_scripts/*
# RUN  echo "ls home" && ls -a /home/
# RUN touch /root/.bashrc 
# RUN echo 'alias scrape_write=python scrape_and_write.py --db-username $POSTGRES_USER --db-password $POSTGRES_PASSWORD --db-host $HOST --database-name $DBBANE'>>/root/.bashrc 
# RUN echo 'alias aggregate_load=python aggregate_plot_load.py --db-username $POSTGRES_USER --db-password $POSTGRES_PASSWORD --db-host $HOST --database-name $DBBANE'>>/root/.bashrc  
# RUN ls -a /
# RUN ls -a ~
# RUN source /root/.bashrc
# RUN \
# echo 'alias scrape_write=python scrape_and_write.py --db-username $POSTGRES_USER --db-password $POSTGRES_PASSWORD --db-host $HOST --database-name $DBBANE'>>~/.bashrc && \
# echo 'alias aggregate_load=python aggregate_plot_load.py --db-username $POSTGRES_USER --db-password $POSTGRES_PASSWORD --db-host $HOST --database-name $DBBANE'>>~/.bashrc && \ 
# source ~/.bashrc

