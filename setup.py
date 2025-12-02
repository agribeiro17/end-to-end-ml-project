from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "")for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements



setup(
    name="end-to-end-ml-project",
    version="0.0.1",
    author="Antonio Ribeiro",
    author_email="tony.ribeiro1717@gmail.com",
    packages=find_packages(), # checks for __init__.py and includes those folders
    install_requires=get_requirements('requirements.txt'), # read from requirements.txt
)