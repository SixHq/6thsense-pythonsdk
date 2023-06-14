from setuptools import setup, find_packages
from pip._internal.req import parse_requirements




VERSION = '0.0.4'
DESCRIPTION = 'Six offical python ackage'
LONG_DESCRIPTION = 'Six is a package that helps you automate pen testing and also helps you protect your API from cybersecurity threats. Visit https://withsix.co to get started.'

# Setting up
setup(
    name="sixth-sense",
    version=VERSION,
    author="6thSense",
    author_email="tech@withsix.co",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["anyio",
    "CacheControl",
    "cachetools",
    "certifi",
    "cffi",
    "charset-normalizer",
    "click",
    "crypto",
    "cryptography",
    "dnspython",
    "exceptiongroup",
    "fastapi",
    "firebase-admin",
    "google-api-core",
    "google-api-python-client",
    "google-auth",
    "google-auth-httplib2",
    "google-cloud-core",
    "google-cloud-firestore",
    "google-cloud-storage",
    "google-crc32c",
    "google-resumable-media",
    "googleapis-common-protos",
    "grpcio",
    "grpcio-status",
    "h11",
    "httplib2",
    "idna",
    "importlib-metadata",
    "msgpack",
    "Naked",
    "passlib",
    "proto-plus",
    "protobuf",
    "pyasn1",
    "pyasn1-modules",
    "pycparser",
    "pydantic",
    "PyJWT",
    "pyparsing",
    "python-dotenv",
    "PyYAML",
    "requests",
    "rsa",
    "shellescape",
    "six",
    "sniffio",
    "starlette",
    "typing_extensions",
    "uritemplate",
    "urllib3",
    "uvicorn",
    "zipp"
    ],
    keywords=['python', 'cybersecurity', 'pentesting', 'encryption', 'rate limiting', 'xss prevention'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)