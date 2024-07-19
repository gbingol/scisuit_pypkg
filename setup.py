from setuptools import setup, find_packages, Distribution
import platform
import sys



Distribution.has_ext_modules=lambda *args: True



def get_platform_tag():
	"""Get platform tag for the current system."""
	system = platform.system()
	architecture = platform.machine()

	system_map = {'Windows': 'win', 'Linux': 'manylinux1', 'Darwin': 'macosx'}
	arch_map = {'x86_64': 'amd64', 'aarch64': 'arm64', 'armv7l': 'armv7'}
	system_tag = system_map.get(system, system.lower())
	arch_tag = arch_map.get(architecture, architecture.lower())

	return f'{system_tag}_{arch_tag}'


def get_python_abi_tag():
	"""Get the Python ABI tag for the current interpreter."""
	py_version = f'cp{sys.version_info.major}{sys.version_info.minor}'
	return py_version


pybindfile = f"pybind{sys.version_info.major}{sys.version_info.minor}.dll"

setup(
	name = 'scisuit',
	version = '1.3.5',
	author = 'Gokhan Bingol, PhD',
	author_email = 'gbingol@pebytes.com',
	description = 'Scientific Computing Package',
	long_description = open('README.md').read(),
	long_description_content_type = 'text/markdown',
	license = 'GPLv3',
	url = 'https://www.pebytes.com',
	classifiers = [
		'Programming Language :: Python :: 3',
		'Programming Language :: C++',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: Microsoft :: Windows',
		'Intended Audience :: Education',
		'Intended Audience :: Manufacturing',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering'
	],
	python_requires = '>=3.10',
	install_requires = ['numpy'], #no need to use limitation on numpy 'numpy<=2.0'
	packages = find_packages(),
	package_data = {
		'': ['README.md'], 
		'scisuit':['boost*.dll', 'wx*.dll', 'scisuit*.dll', pybindfile]
		},
	setup_requires = ['setuptools>=61.0'],
	options={
		'bdist_wheel': {
			'python_tag': get_python_abi_tag(),  # Specify the Python ABI tag
			'plat_name': get_platform_tag()  # Specify the platform explicitly
		}
	}
)
