ip=$(hostname -I)
echo starting quokka-ui with host IP address: ${ip}
cp quokka-ui/.env-bak quokka-ui/.env
sed -i "s/<quokka-ip>/${ip}/" quokka-ui/.env
cat quokka-ui/.env
cd ~/quokka/quokka-ui
npm start
