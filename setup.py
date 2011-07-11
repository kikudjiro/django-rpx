import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name = "django-rpx",
    version = "1.0",
    description='django-rpx provides handles site login and user registration using the rpxnow.com service',
    url = 'http://github.com/kikudjiro/django-rpx',
    license = 'BSD',
    long_description=README,

    author = 'Alexander Alexeychuk',
    author_email = 'kikudjiro@gmail.com',
    packages = [
        'django_rpx',
        'django_rpx.templatetags',
    ],
    package_data = {'django_rpx': ['templates/*.html']},
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
