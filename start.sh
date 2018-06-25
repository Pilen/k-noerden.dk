screen -dmS server
screen -S server -X stuff "cd /vagrant\n"
screen -S server -X stuff "source venv/bin/activate\n"
screen -S server -X stuff "./run\n"
