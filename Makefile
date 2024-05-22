create-venv:
	python3 -m venv venv

activate-venv:
	source venv/bin/activate

pip-upgrade:
	python -m pip install --upgrade pip 
	
install-req:
	pip install -r requirements.txt

update-ui:
	pyuic5 gui.ui -o gui.py