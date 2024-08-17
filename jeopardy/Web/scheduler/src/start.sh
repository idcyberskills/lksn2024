#!/usr/bin/env sh

DBCON=$(timeout 3 curl -v telnet://db:5432 2>&1 | grep "Connected to")
while [ "${DBCON}" == "" ]
do
    echo $DBCON
    echo -e "[-] Failed to connect database"
    echo -e "[*] Retrying in 5 seconds\n"
    sleep 5
    
    DBCON=$(timeout 3 curl -v telnet://db:5432 2>&1 | grep "Connected to")
done
echo -e "[+] Connected to the database"

# Web application initialization
python3 manage.py collectstatic --clear --noinput
python3 manage.py migrate

/entrypoint.sh