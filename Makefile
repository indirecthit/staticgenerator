clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build
	@echo "removing (.coverage)"
	@rm -f .coverage
	@echo "Done!"
	
unit: clean
	@echo "Running unit tests..."
	@export PYTHONPATH=`pwd`:`pwd`/staticgenerator::$$PYTHONPATH && \
		nosetests -d -s --verbose --with-coverage --cover-inclusive --cover-package=staticgenerator \
			staticgenerator/tests/unit
	