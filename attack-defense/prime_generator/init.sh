kill $(cat pid)
echo "redeploying... make sure to redeploy as user instead of root/ubuntu"
sleep 4
nohup socat TCP-L:10003,fork EXEC:"python3 ./server.py",reuseaddr,stderr 2>&1 &
echo $! > pid