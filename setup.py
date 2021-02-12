from setuptools import setup

setup(
    name='datadog_log_monitor',
    version='0.1',
    packages=['tests', 'tests.tasks', 'tests.tasks.stat_modules', 'tests.config', 'tests.models', 'tests.runner',
              'log_monitor', 'log_monitor.tasks', 'log_monitor.tasks.stat_modules', 'log_monitor.config',
              'log_monitor.models', 'log_monitor.runner'],
    package_data={
        'log_monitor.config': ['config_default.yml'],
    },
    scripts=['bin/datadog_log_monitor'],
    install_requires=[
        "clfparser==0.3",
        "mock==4.0.3",
        "pathlib==1.0.1",
        "pytest==6.2.2",
        "pyyaml==5.4.1",
        "wheel",
    ],
    author='Eloi Charpentier',
    author_email='eloi.charpentier@epita.fr',
    description='Datadog recruitement project',
    long_description=open('README.md').read(),
)
