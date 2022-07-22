pip-compile --upgrade

pip-compile requirements-dev.in --upgrade

pip install -r requirements.txt
pip install -r requirements-dev.txt
