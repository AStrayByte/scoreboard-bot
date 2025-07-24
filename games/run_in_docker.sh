apt-get update
git config --global --add safe.directory /code
git pull
pip install --upgrade pip
pip install -r requirements.txt
python3 main.py
