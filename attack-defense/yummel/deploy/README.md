#Hosted dengan systemctl

systemctl daemon-reload
systemctl enable probset.service
systemctl start probset

# Make sure statusnya sudah up, will initiate the bash script and runs every 30s