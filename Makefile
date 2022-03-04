init:
	pip install -r requirements.txt
    
clean:
	rm -rf .cache
	rm -rf build
	rm -rf pip_services3_gcp.egg-info
	rm -f pip_services3_gcp/*.pyc
	rm -f pip_services3_gcp/**/*.pyc
	rm -rf test/__pycache__
	rm -rf test/**/__pycache__
	
install:
	pip install -e .

.PHONY: test
test:
	py.test test -s

docgen:
	rm -rf build/doc
	sphinx-apidoc -f -e -o doc/api pip_services3_gcp
	mv build/doc/modules.rst build/doc/index.rst
	rm -rf doc/api
	sphinx-build -b html build/doc doc/api -c .
