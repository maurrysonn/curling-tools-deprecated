######################
# Curling Tools Cmd  #
######################

# Clean files
clean:
	find -L . -name "*~" -exec rm -fr {} \;
	find -L . -name "*.pyc" -exec rm -fr {} \;

# Virtual Env Management
env_create:
	virtualenv --distribute --no-site-packages apps

env_upgrade:
	pip install -r env_requirements.txt

env_freeze:
	pip freeze > env_requirements.txt

# Sync DB and add initial values
syncdb:
	python manage.py syncdb

# Run dev server
runserver:
	python -Wd manage.py runserver 0.0.0.0:8000

# Settings
cp_settings:
	cp settings.py.example curling_tools/settings.py
