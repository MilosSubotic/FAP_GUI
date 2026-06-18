#!/usr/bin/env bash
#
# install.sh — instalira sve zavisnosti potrebne za pokretanje aplikacije.
#
# Pokretanje:
#     chmod +x install.sh
#     ./install.sh
#
set -e  # prekini ako bilo koja komanda padne

echo "==> Instaliraju se sistemski paketi (apt)..."
# libasound2-dev je potreban da bi se 'simpleaudio' izgradio na Linuxu.
# python3-venv i python3-pip su potrebni za pravljenje okruzenja i instalaciju.
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libasound2-dev

echo "==> Pravi se (.venv)..."
python3 -m venv .venv
source .venv/bin/activate

echo "==> Instaliraju se Python paketi (pip)..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "==> Gotovo! Sve je instalirano."
echo "Da pokrenes aplikaciju:"
echo "    source .venv/bin/activate"
echo "    python3 app.py        


