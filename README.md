# Resort
RESTful API test automation tool

<img src="data/icons/resort_edit.png" alt="Resort Logo" width="250">
<sub><sup><a href="https://www.vecteezy.com/vector-art/146821-palm-tree-collection-vectors">Original Image by Vecteezy</a></sup></sub>

## Work in progress!
The development plan is described in the [TODO](TODO.md) list.

## Basic usage:
Let's suppose you have a server with the RESTful API (`test-server`). You want to introduce some changes to the `test-server` without modifying the API. And you want to be sure that your changes will not bring a regression to existing functionality. It would be nice `store` the `test-server` responses before the changes and `check` that there is no difference later. That is exactly what the `resort` does.

Run resort to generate all boilerplate for the project
```
$ python resort/app.py --create --project=basic-rest-test
$ cd basic-rest-test
```
Configure the resort and provide one or more test specifications. They must be in the project directory and have `test_*` prefix in the file name:
```
$ vim test_first.json
$ cat test_first.json
{
    "info": {
        "description": "generated test stub",
        "version": "1.0.0"
    },
    "server": {
        "url": "http://127.0.0.1:8888"
    },
    "requests": [
        ["/index.html", "get"]
    ]
}
```
The folowing configuration is optional, you may use it to exclude some test files. By default it does nothing. It's safe to delete this file.
```
$ vim config.json
$ cat config.json
{
    'exclude': []
}
```

Now let's memorize the way the test server responds.
```
$ python resort/app.py --store
```
The application will store some files that represent responses from the test-server, they called `etalons`.
Now you can edit the source code of your test-server, restart it, and test that everything works as expected:
```
$ python resort/app.py --check
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


