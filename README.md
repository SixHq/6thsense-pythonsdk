# **Sixth**


[![N|Solid](https://firebasestorage.googleapis.com/v0/b/test-103bf.appspot.com/o/waves.png?alt=media&token=0fa4c489-d9c9-4a3b-9178-593b2b018613)](https://nodesource.com/products/nsolid)

Six helps you proactively identify security vulnerabilities and prevent cyberattacks on your system that could cost you millions of dollars.



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
pip install six-python
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
import SixthSense from "sixth-node";
import  express  from "express";

const app = express();

const six = new SixthSense("apikey", app)
await six.init()
// add routes, middleware, exception handlers etc


// after done adding routes, middleware, etc
six.sync_project();
app.listen(PORT, ()=> console.log(`Server running on port: http://localhost:${PORT}`))
```
