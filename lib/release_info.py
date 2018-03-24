# coding:utf-8

name = "HouseLoanAutoPy3"
description = "HouseLoanAutoPy3: 房贷UI自动化代码框架"

_version_major = 4
_version_minor = 0
_version_patch = 0
_version_extra = ''

_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))

if _version_extra:
	__version__ = __version__ + _version_extra

version = __version__
version_info = (_version_major, _version_minor, _version_patch, _version_extra)

author = 'Shixiong Tan'

author_email = 'tanshixiong1@xiaoniu66.com'

url = 'https://github.com/Tanshixiong/HouseLoanAutoPy3'

platforms = ['Linux', 'Mac OSX', 'Windows']

classifiers = [
	'Framework :: Unittest, define',
	'Intended Audience :: Developers',
	'Intended Audience :: Science/Research',
	'License :: OSI Approved :: BSD License',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3',
	'Topic :: System '
	]
