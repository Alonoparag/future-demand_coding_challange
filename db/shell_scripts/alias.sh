#!/bin/bash
echo -e "#!/bin/bash\npsql -U future_demand -d future_demand_db -c \"SELECT event_id, date, time, title FROM events LIMIT 3\"" >/usr/bin/check_db && chmod 555 /usr/bin/check_db
echo 'alias check_db created'