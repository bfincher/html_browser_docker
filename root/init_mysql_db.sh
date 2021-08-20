#!/usr/bin/with-contenv sh

# nothing to init here.  Just wait until the DB is up
/wait-until "echo 'select 1' | mysql --user=$DB_USER --password=$DB_PASS $DB_NAME -h $DB_HOST" 60

if [ -f ${APP_CONFIG}/hb.sql.bak8 ]; then
    mv ${APP_CONFIG}/hb.sql.bak8 ${APP_CONFIG}/hb.sql.bak9
fi

if [ -f ${APP_CONFIG}/hb.sql.bak7 ]; then
    mv ${APP_CONFIG}/hb.sql.bak7 ${APP_CONFIG}/hb.sql.bak8
fi

if [ -f ${APP_CONFIG}/hb.sql.bak6 ]; then
    mv ${APP_CONFIG}/hb.sql.bak6 ${APP_CONFIG}/hb.sql.bak7
fi

if [ -f ${APP_CONFIG}/hb.sql.bak5 ]; then
    mv ${APP_CONFIG}/hb.sql.bak5 ${APP_CONFIG}/hb.sql.bak6
fi

if [ -f ${APP_CONFIG}/hb.sql.bak4 ]; then
    mv ${APP_CONFIG}/hb.sql.bak4 ${APP_CONFIG}/hb.sql.bak5
fi

if [ -f ${APP_CONFIG}/hb.sql.bak3 ]; then
    mv ${APP_CONFIG}/hb.sql.bak3 ${APP_CONFIG}/hb.sql.bak4
fi

if [ -f ${APP_CONFIG}/hb.sql.bak2 ]; then
    mv ${APP_CONFIG}/hb.sql.bak2 ${APP_CONFIG}/hb.sql.bak3
fi

if [ -f ${APP_CONFIG}/hb.sql.bak1 ]; then
    mv ${APP_CONFIG}/hb.sql.bak1 ${APP_CONFIG}/hb.sql.bak2
fi

mysqldump --user=$DB_USER --password=$DB_PASS $DB_NAME -h $DB_HOST > ${APP_CONFIG}/hb.sql.bak1


