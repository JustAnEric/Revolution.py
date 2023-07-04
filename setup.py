from setuptools import setup, find_packages

setup(
    name = "revolution.py",
    version = "5.0.1.1",
    description = "A simple Py package to integrate Revolution's bot API into python.",
    long_description = "A simple Py package to integrate Revolution's bot API into Python. \nhttps://github.com/JustAnEric/Revolution.py",
    author = "JustAnEric",
    maintainer = "Revolution Corporation",
    requires = ["requests"],
    url = "https://revolution-web.repl.co/",
    packages = ["revolution"],
    keywords = ["revolutionpy", "python3", "revolution"],
    #include_dirs=["./revolution_py"]
)