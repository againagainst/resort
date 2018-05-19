
### First steps
- [x] Setup environment 
- [x] Create a basic method for API definition
- [x] Fetch an etalon
- [x] Provide options support
- [x] Create a basic etalon definition (`--store` mode)
- [x] Create an etalon-reader (`--check` mode)

### Alpha-release (python -m resort)
- [ ] Add tests and use TDD
- [ ] Docstring all classes and methods
- [ ] Setup exhaustive logging
- [ ] Create the app
- [ ] Add error (exception) handling 
- [ ] Write exhaustive help system (`--help`)
- [ ] Replace arguments with commands (`--store`->`store`)
- [ ] Add instalation procedures (setup.py)

### Release: a basic test generator
- [ ] Module and application modes `$ python3 -m resort --help` and `$ resort --help`
- [ ] CLI storing (`$ resort store`)
- [ ] CLI checking (`$ resort check`)
- [ ] Boilerplate generation (`$ resort create [prj-name]`)
- [ ] Test generation (`$ resort generate [--unittest]`)
- [ ] Application interface in python (`import resort`)