
### First steps
- [x] Setup environment 
- [x] Create a basic method for API definition
- [x] Fetch an etalon
- [x] Provide options support
- [x] Create a basic etalon definition (`--store` mode)
- [x] Create an etalon-reader (`--check` mode)

### Basic test generator
- [ ] Support --verbose mode, and run application quietly by default
- [ ] Require -f with the `store` if etalons directory is not empty
- [ ] Module and application modes `$ python3 -m resort --help` and `$ resort --help`
- [ ] Test generation (`$ resort generate [--unittest]`)
- [x] CLI storing (`$ resort --store`)
- [x] CLI checking (`$ resort --check`)
- [x] Boilerplate generation (`$ resort --create [prj-name]`)
- [x] Application interface in python (`import resort`)
- [x] REMOVED: -- An ability to update etalons (`--update` options to generate diff)
- [x] Support authentication and sessions

### Features to do:
- [ ] Handle "Connection refused" error
- [ ] Handle pretty-printing of the snapshot-etalon difference
- [ ] Support ResortProject.ignore through config
- [ ] Rename entity to URI (Uniform Resource Identifier)
- [ ] Support situation when test files were changed after the `store` action. (warning on check)
- [ ] MIME Type based etalon
- [ ] Implement test system based on `tavern` format
- [ ] Make `etalon-id` structure that combines `entry: str` and `name: str`
- [ ] Control exports with `__all__` field in every module/package
- [x] A tool for comparing etalon and snapshot
- [x] Test scenario feature: call checks in specified order
- [x] Support names for tests' etalons (test_*.json['info']['title'])

### Project organization tasks
- [ ] Add tests and use TDD
- [x] Docstring all classes and methods
- [x] Setup logging (daiquiri)
- [x] Create the app
- [ ] Add versioning for the framework and track version of the server
- [x] Add error (exception) handling 
- [ ] Write exhaustive help system (`--help`)
- [x] Replace arguments with commands (`--store`->`store`)
- [ ] Add installation procedures (setup.py)
- [ ] Describe the application API
