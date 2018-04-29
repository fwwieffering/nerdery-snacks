from json import JSONEncoder


class SnackEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__()
