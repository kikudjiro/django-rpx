from distutils.core import setup

setup(name='django_rpx',
    version='1.0',
    description='RPX (rpxnow.com) support for django',
    author='Alexander Alexeychuk',
    author_email='kikudjiro@gmail.com',
    url='http://github.com/kikudjiro/django_rpx',
    packages=['django_rpx', 'django_rpx.templatetags'],
    package_dir={'django_rpx': '', 'django_rpx.templatetags': 'templatetags'},
    package_data={'django_rpx': ['templates/*.html']},
)

