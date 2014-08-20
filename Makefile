init:
	pip install -r requirements.txt

test:
	nosetests tests

clean:
	find . -iname \*.pyc -exec rm {} \;
