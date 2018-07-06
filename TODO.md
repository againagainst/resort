
### First steps
- [x] Setup environment 
- [x] Create a basic method for API definition
- [x] Fetch an etalon
- [x] Provide options support
- [x] Create a basic etalon definition (`--store` mode)
- [x] Create an etalon-reader (`--check` mode)

### Basic test generator
- [ ] Module and application modes `$ python3 -m resort --help` and `$ resort --help`
- [x] CLI storing (`$ resort --store`)
- [x] CLI checking (`$ resort --check`)
- [x] Boilerplate generation (`$ resort --create [prj-name]`)
- [ ] Test generation (`$ resort generate [--unittest]`)
- [ ] Application interface in python (`import resort`)
- [ ] An ability to update etalons (`--update` options to generate diff)

### Features to do:
- [ ] MIME Type based etalon
- [x] A tool for comparing etalon and snapshot
- [ ] Test scenario feature: call checks in specified order
- [ ] Rename entity to URI (Uniform Resource Identifier)
- [ ] Implement test system based on `tavern` format

### Project organization tasks
- [ ] Add tests and use TDD
- [x] Docstring all classes and methods
- [x] Setup logging (daiquiri)
- [x] Create the app
- [ ] Add versioning for the frameworks and track version of the server
- [x] Add error (exception) handling 
- [ ] Write exhaustive help system (`--help`)
- [x] Replace arguments with commands (`--store`->`store`)
- [ ] Add installation procedures (setup.py)
- [ ] Describe the application API ()
