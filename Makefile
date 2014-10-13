init:
	pip install -r requirements.txt

run:
	python main.py

debug:
	python main.py --env dev

test:
	nosetests tests

clean:
	find . -iname \*.pyc -exec rm {} \;
