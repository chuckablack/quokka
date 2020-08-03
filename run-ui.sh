ip=$(hostname -I)
sed -i "s/192.168.254.114/${ip}/" quokka-ui/.env
cat quokka-ui/.env
cd quokka-ui
npm start
