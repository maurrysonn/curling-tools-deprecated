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

env_upgrade: requirements.txt
	pip install -r env_requirements.txt

env_freeze:
	pip freeze > env_requirements.txt

# Run dev server
runserver:
	python -Wd manage.py runserver 0.0.0.0:8000
