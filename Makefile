
install:spec
	rm -rf build
	python setup.py build
	python setup.py install
spec:
	ipython kernelspec install root
