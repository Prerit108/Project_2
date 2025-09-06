
"""The setup. py file is an essential part of packaging and
distributing Python projects. It is used by setuptools
(or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more"""

from typing import List

## List is used for type hinting, especially when you want to specify that a variable, function argument, or return value is a list containing elements of a specific type.


from setuptools import find_packages,setup
## find_packages find the __init__.py files and consider the folder as a package
## setup will provide all the information regarding the project

def get_requirements()->List[str]:
    "this function will return list of requirements"
    requirement_list = []
    try:
        with open("requirements.txt","r") as  file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                
                ## "-e ." is responsible for triggering the setup.py and install the libraries from pip.
                ## ignoring the empty lines and "-e ."
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list

print(get_requirements())

## Creating a package with metadata and dependencies of the project
setup(
    name = "mlproject2",
    version = "0.0.1",
    author = "Prerit",
    author_email="cloudsharma909@gmail.com",
    packages = find_packages(),  ## find all the packages in the project
    install_requires = get_requirements()  ## Installs all the libraries mentioned in requirements.txt
)

