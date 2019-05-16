from setuptools import setup

setup(

    name="TikTag",

    version="0.1.0",

    author="name surname",
    author_email="name@addr.ess",

    packages=["TikTag"],

    #include_package_data=True,

    install_requires=[
        "discogs-client",
		"ffmpeg",
		"fuzzywuzzy",
		"musicbrainzngs",
		"mutagen",
		"Pillow",
		"pyacoustid",
		"PyQt5",
		"python-Levenshtein",
		"spotipy"
    ],
)