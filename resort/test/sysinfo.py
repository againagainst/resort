import sys
import pkgutil
from pprint import pprint

print('paths:')
pprint(sys.path)
print('modules')
search_path = '.'  # set to None to see all modules importable from sys.path
all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
pprint(all_modules)
