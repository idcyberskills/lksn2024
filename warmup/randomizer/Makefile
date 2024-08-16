setup:
	apt-get update && \
	    apt-get -y install python3 socat python3-pip && \
	pip3 install pycryptodome

start:
	# run in background: make start &
	socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"python3 -u main.py"