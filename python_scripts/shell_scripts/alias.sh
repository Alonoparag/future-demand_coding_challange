#!/bin/bash
echo -e "#!/bin/bash\npython scrape_and_write.py --db-username $POSTGRES_USER --db-password $POSTGRES_PASSWORD --db-host $HOST --database-name $DB_NAME">/usr/bin/scrape_write && chmod 555 /usr/bin/scrape_write
echo -e "#!/bin/bash\npython aggregate_plot_load.py --db-username $POSTGRES_USER --db-password $POSTGRES_PASSWORD --db-host $HOST --database-name $DB_NAME --action \$1">/usr/bin/aggregate_load && chmod 555 /usr/bin/aggregate_load
echo 'commands scrape_write and aggregate_load created'