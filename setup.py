import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name='cfgr',
  version='0.0.1',
  description='cfgr separates logic from data',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='http://github.com/markkorput/pycfgr',
  author='Short Notion',
  author_email='shortnotion@gmail.com',
  license='MIT',
  packages=setuptools.find_packages(), #['cfgr'],
  #install_requires=['evento', 'python-osc'],
  test_suite='nose.collector',
  tests_require=['nose'],
  zip_safe=False)