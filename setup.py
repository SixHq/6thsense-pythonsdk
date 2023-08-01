from setuptools import setup, find_packages
from pip._internal.req import parse_requirements




VERSION = '0.1.8'
DESCRIPTION = 'Sixth offical python package'
LONG_DESCRIPTION = '''
# **Sixth**


[![N|Solid](https://firebasestorage.googleapis.com/v0/b/test-103bf.appspot.com/o/waves.png?alt=media&token=0fa4c489-d9c9-4a3b-9178-593b2b018613)](https://nodesource.com/products/nsolid)

Sixth helps you proactively identify security vulnerabilities and prevent cyberattacks on your system that could cost you millions of dollars.



## Features

- Automated Penetration Testing
- End to End encryption of data
- DDOS attack mitigation
- Man in the Middle Attack prevention
- No Rate Limit Attack Prevention
- Cross site scripting mitigation
- Cross site request forgery mitigation

Sixth SDK is a lightweight library that helps you make sure your application stays secured from all sorts of cybersecurity threats and attacks and helps you mitigate them. visit our [website](https://withsix.co) to get started!.

## **Installation and usage**
### Python
Sixth SDK is currently only available for [fasiapi](https://fastapi.tiangolo.com/lo/) and can be installed as followed.

#### _Installation_

```sh
pip install sixth-python
```

#### _usage_
```python
#import sixth SDK
from sixth.sdk import Sixth
from fastapi import FastAPI

app = FastAPI()
# initalize app, add routes, middleware, exception handlers etc


#....
Sixth(apikey="api key", app=app).init()
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=PORT)

```

### Javascript
Sixth SDK is currently only available for [express](https://expressjs.com/) and can be installed as followed.

#### _Installation_

```sh
npm i sixth-node
```

#### _usage_
```js
import Sixth from "sixth-node";
import  express  from "express";

const app = express();

const six = new Sixth("apikey", app)
await six.init()
// add routes, middleware, exception handlers etc


// after done adding routes, middleware, etc
six.sync_project();
app.listen(PORT, ()=> console.log(`Server running on port: http://localhost:${PORT}`))
```

'''

# Setting up
setup(
    name="sixth-python",
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
    "zipp",
    "pickleDB"
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