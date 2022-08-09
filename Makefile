run:
	python3 main.py

# Target to create local environment
# Activate using 'source env/bin/activate'
create-env:
	python3 -m venv env 

clean:
	rm -rf users.db
