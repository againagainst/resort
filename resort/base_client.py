import json


class BasicClient(object):

    def __init__(self, schema_info):
        '''
        schema_info = {
            'type' = 'file',
            'file' = './path/to/schema,
        }
        '''
        self._type = schema_info.get('type', 'file')
        self._file = schema_info.get('file', None)

    def prepare(self):
        if self._type == 'file':
            with open(self._file) as fp:
                self.parse_schema(fp)
        # Create a prepared client:
        # client = BasicClient().prepare()
        return self

    def parse_schema(self, in_file):
        body = json.load(in_file)
        self._schema_body = body['paths']

    @property
    def schema_body(self):
        return self._schema_body
