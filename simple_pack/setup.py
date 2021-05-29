from setuptools import setup

setup(
	name='revcomp',
	version='0.0.1',
	description='reverse complement a DNA string',
	py_modules=['revcomp'],		# what people import, not what the pip install
	package_dir={'':  'src'},	# our code is in ./src
)

# Install keeping source here
# pip install -e .