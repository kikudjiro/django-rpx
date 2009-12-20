from distutils.core import setup

setup(name='django_rpx',
    version='1.0',
    description='RPX (rpxnow.com) support for django',
    author='Alexander Alexeychuk',
    author_email='kikudjiro@gmail.com',
    url='http://github.com/kikudjiro/django_rpx',
    packages=['', 'templatetags'],
    data_files=[('templates', ['templates/*.html'])],
)

