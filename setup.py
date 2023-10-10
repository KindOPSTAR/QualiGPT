#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages

setup(
    name='QualiGPTApp',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openai',
        'nltk',
        'python-docx',
        'PyQt5',
        'docx2txt',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'qualigptapp = QualiGPTApp:main',  # 请替换your_module_name和main_function_name为你的模块名和主函数名
        ],
    },
    author='He Albert Zhang',
    author_email='hpz5211@psu.edu',
    description='Qualitative Data Analysis Tool using OpenAI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_github_username/your_repository_name',  # 请替换为你的GitHub仓库URL
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

