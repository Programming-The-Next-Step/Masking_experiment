import setuptools

setuptools.setup(
		name = "masking_package",
		version = "1.0.1",
		author = "Dom",
		autor_email = "dominik-bachmann@uva.student.nl",
		description = "A package for implementing masking experiments",
		python_requires = ">=3.6",
		packages = setuptools.find_packages(),
		install_requires = ['psychopy.visual', 'psychopy.core',
					        'psychopy.event', 'random'],
	   # Importing images
       include_package_data = True
)