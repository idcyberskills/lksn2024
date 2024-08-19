#!/bin/bash

C2_SERVER="13.212.229.104"
echo "${C2_SERVER} localohst" >> /etc/hosts

git clone https://github.com/itaymigdal/Nimbo-C2
cp ./config.jsonc.template ./Nimbo-C2/Nimbo-C2/config.jsonc
cd Nimbo-C2/Nimbo-C2

docker run -it --rm -p 80:80 -v $(pwd):/Nimbo-C2 -w /Nimbo-C2 itaymigdal/nimbo-dependencies