#!/usr/bin/with-contenv sh

# nothing to init here.  Just wait until the DB is up
/wait-until "echo 'select 1' | mysql --user=$DB_USER --password=$DB_PASS $DB_NAME -h $DB_HOST" 60
