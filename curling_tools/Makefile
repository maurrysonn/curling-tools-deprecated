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
	mv curling_tools.sqlite curling_tools.sqlite.save
	python manage.py syncdb --noinput

# Run dev server
runserver:
	python -Wd manage.py runserver 0.0.0.0:8000

# Settings
settings_freeze:
	cp curling_tools/settings.py settings.py.example

settings_upgrade:
	cp settings.py.example curling_tools/settings.py

# Initial Data
dump_initial_data:
	mv initial_data.json initial_data.json.save
	python manage.py dumpdata --indent=2 --natural auth.User > initial_data.json
	python manage.py dumpdata --natural --indent=2 base.Country > curling_tools/base/fixtures/country_data.json
	python manage.py dumpdata --natural --indent=2 base.City > curling_tools/base/fixtures/city_data.json
	python manage.py dumpdata --natural --indent=2 base.address > curling_tools/base/fixtures/address_data.json
	python manage.py dumpdata --natural --indent=2 base.Club > curling_tools/base/fixtures/club_data.json
	python manage.py dumpdata --natural --indent=2 base.Rink > curling_tools/base/fixtures/rink_data.json
	python manage.py dumpdata --natural --indent=2 base.Person > curling_tools/base/fixtures/person_data.json
	python manage.py dumpdata --natural --indent=2 base.Player > curling_tools/base/fixtures/player_data.json
	python manage.py dumpdata --natural --indent=2 base.Coach > curling_tools/base/fixtures/coach_data.json
	python manage.py dumpdata --natural --indent=2 base.Team base.TeamMembership > curling_tools/base/fixtures/team_data.json

load_data:
	python manage.py loaddata curling_tools/base/fixtures/country_data.json
	python manage.py loaddata curling_tools/base/fixtures/city_data.json
	python manage.py loaddata curling_tools/base/fixtures/address_data.json
	python manage.py loaddata curling_tools/base/fixtures/club_data.json
	python manage.py loaddata curling_tools/base/fixtures/rink_data.json
	python manage.py loaddata curling_tools/base/fixtures/person_data.json
	python manage.py loaddata curling_tools/base/fixtures/player_data.json
	python manage.py loaddata curling_tools/base/fixtures/coach_data.json
	python manage.py loaddata curling_tools/base/fixtures/team_data.json
