from setuptools import find_namespace_packages, setup

setup(
	name='NEMO',
	version='4.4.0.dev',
	python_requires='>=3.8',
	packages=find_namespace_packages(exclude=['NEMO.tests', 'NEMO.tests.*']),
	include_package_data=True,
	url='https://github.com/usnistgov/NEMO',
	license='Public domain',
	author='Center for Nanoscale Science and Technology',
	author_email='CNSTapplications@nist.gov',
	description='NEMO is a laboratory logistics web application. Use it to schedule reservations, control tool access, track maintenance issues, and more.',
	long_description='Find out more about NEMO on the GitHub project page https://github.com/usnistgov/NEMO',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Science/Research',
		'Intended Audience :: System Administrators',
		'License :: Public Domain',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.8',
	],
	install_requires=[
		'cryptography==39.0.0',
		'Django==3.2.16',
		'django-auditlog==2.2.2',
		'django-filter==22.1',
		'django-mptt==0.14.0',
		'djangorestframework==3.14.0',
		'drf-excel==2.2.0',
		'drf-flex-fields==1.0.0',
		'ldap3==2.9.1',
		'Pillow==9.4.0',
		'pymodbus==3.1.1',
		'python-dateutil==2.8.2',
		'pytz==2022.7.1',
		'requests==2.28.2',
	],
	entry_points={
		'console_scripts': ['nemo=NEMO.provisioning:entry_point'],
	},
)
