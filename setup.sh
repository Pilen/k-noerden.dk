
# This script is intended to be executed as the ordinary user (vagrant)
sudo -i -u vagrant

cd /
sudo pacman -Syyu
sudo pacman -S python postgresql screen --noconfirm

sudo -u postgres initdb --locale "$LANG" -E UTF8 -D '/var/lib/postgres/data'
sudo systemctl enable --now postgresql.service
sudo -u postgres createuser --superuser vagrant
sudo -u vagrant createdb knoerden.dk

cd /vagrant
rm -rf venv
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
