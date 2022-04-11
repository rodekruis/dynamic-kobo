from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="dynamic-kobo",
    version="0.0.3",
    description="Replace / update / redeploy KoBo forms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rodekruis/dynamic-kobo",
    author="J. Margutti",
    author_email="jmargutti@redcross.nl",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="KoBo",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=[
        'click>=7.1.2',
        'python-dotenv>=0.20.0',
        'selenium>=4.1.3',
        'selenium_wire>=4.6.3'
    ],
    entry_points={
        "console_scripts": [
            "replace-redeploy=dynamic_kobo.replace_redeploy:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/rodekruis/dynamic-kobo/issues",
        "Source": "https://github.com/rodekruis/dynamic-kobo"
    },
)