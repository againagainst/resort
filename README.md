# Resort
RESTful API test automation tool

<img src="data/icons/resort_edit.png" alt="Resort Logo" width="250">
<sub><sup><a href="https://www.vecteezy.com/vector-art/146821-palm-tree-collection-vectors">Original Image by Vecteezy</a></sup></sub>

## Work in progress!
Development plan is described in the [TODO](TODO.md) list.

## Basic usage:
Let's suppose you have a server with the RESTful API (`test-server`). You want to introduce some changes to the `test-server` without modifying the API. And you want to be sure that your changes will not bring a regression to existing functionality. It would be nice `store` the `test-server` responses before the changes and `check` that there is no difference later. That is exactly what the `resort` does.

Run resort to create all boilerplate for the project
```
$ python resort/app.py --create --project=basic-rest-test
$ cd basic-rest-test
```
Configure the resort and provide an API specification of the test-server
```
$ vim config.json
$ cat config.json
{
    "server": {
        "spec": "basic-apispec.json",
        "url": "http://localhost:8888"
    }
}
$ vim basic-apispec.json
$ cat basic-apispec.json
{
    "paths": {
        "/ping": {...},
        "/echo/?{entity}": {...}
    }
}
```
Now let's memorize the way the test server responds.
```
$ python resort/app.py --store --config=config.json
```
The application will store some files that represents responses from the test-server, they called `etalons`.
Now you can make some changes in the test-servers's code, restart it, and let's check that everything works as expected:
```
$ python resort/app.py --check --config=config.json
```

### How to prepare the dev environment:
```
$  python3 -m venv .venv
$ .venv/bin/python3 -m pip install -r reqirements.txt
```

### How to start the REST-test server:
```
(.venv) $ python ./basic_rest/app.py
```

VSCode: `F5 (Run Task...) -> "Basic REST Server"`


