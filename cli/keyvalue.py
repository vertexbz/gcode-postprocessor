import argparse


class KeyValue(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())

        # split it into key and value
        key, value = values.split('=')
        # assign into dictionary
        getattr(namespace, self.dest)[key] = value
