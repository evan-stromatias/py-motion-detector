from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open('requirements.txt').readlines()]


setup(
    name='py_motion_detector',
    version='0.0.2',
    description='Python Application for Motion Detection Using a Stationary Camera',
    author='Evangelos Stromatias',
    author_email='<evangelos@stromatias.gmailcom>',
    url='https://bitbucket.org/',
    packages=find_packages(exclude='tests'),
    license='MIT',
    install_requires=REQUIREMENTS,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'py_motion_detector = py_motion_detector.api.cli.py_motion_detector_basic:main',
            'py_motion_detector_data_player = py_motion_detector.api.cli.py_motion_detector_data_player:main'
        ]
    }
)
