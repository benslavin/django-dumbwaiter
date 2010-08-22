from distutils.core import setup

setup(name='django-dumbwaiter',
      version='0.1',
      description='Asynchronous function execution with cached results',
      author='Ben Slavn',
      author_email='benjamin.slavin@gmail.com',
      url='https://github.com/benslavin/django-dumbwaiter/',
      packages=['dumbwaiter'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )