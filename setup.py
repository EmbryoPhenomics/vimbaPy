from setuptools import setup
# from vimbaPy import __version__


setup(name='vimbaPy',
      version="0.2.1",
      description="vimbaPy is a package containing helper/convenience functions for pymba and VimbaPython.",
      keywords='python, python3, opencv, machine vision, computer vision, vimba, allied vision',
      author='zibbini',
      author_email='ziadibbini@gmail.com',
      license='MIT',
      packages=[
          'vimbaPy',
      ],
      install_requires=[
      	   'pymba'
      ]
)

