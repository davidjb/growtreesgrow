from setuptools import setup, find_packages

version = '0.1.dev0'

long_description = (
    open('README.rst').read()
    + '\n')

setup(name='growtreesgrow',
      version=version,
      description="Simple scripts for taking Pi camera photos and uploading to the web.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Pi Raspberry Camera picamera Twitter Flickr',
      author='David Beitey',
      author_email='david' + chr(64) + 'davidjb.com',
      url='https://github.com/davidjb/growtreesgrow',
      license='MIT',
      py_modules=['growtreesgrow'],
      include_package_data=True,
      zip_safe=False,
      setup_requires=['setuptools-git', 'begins'],
      install_requires=[
          'setuptools',
          'begins>=0.9',
          'picamera>=1.10',
          'pyyaml>=3.11',
          'twython>=3.2.0',
          'requests>=2.7.0',
          'flickrapi>=2.0'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      upload-pi-photo = growtreesgrow:main.start
      """,
      )
