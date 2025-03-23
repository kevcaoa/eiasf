from setuptools import setup, find_packages

setup(
    name="eiasf",
    description="Everything Is A Service Framework",
    version="0.0.3",
    author="Kevin Cao",
    author_email="kevcaoa@gmail.com",
    install_requires=[
        'slack-sdk',
        'ratelimit',
        'backoff',
    ],
    packages=find_packages(),
)
