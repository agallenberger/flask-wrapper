'''
Wraps a Flask server into a class so that it can be imported and ran in a separate program.
'''
import socket
import threading

import flask


def get_ip():
    '''
    Gets the internal IP address of the current device. OS independent.

    :return: IP
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception as e:
        print(f'{e}!r')
        ip = '127.0.0.1'
    finally:
        s.close()

    return ip


class EndpointAction():
    def __init__(self, function):
        self.function = function


    def __call__(self, *args):
        return self.function()


class FlaskWrapper():
    def __init__(self, name):
        '''
        :param name: Flask app name
        '''
        self.flask_server  = flask.Flask(name)
        self.server_thread = None
        self.host          = None
        self.port          = None


    def run(self, host=get_ip(), port=5000):
        '''
        Runs the flask app in a separate thread. By defualt, the app runs on the device's
        internal IP.

        :param host: hostname on which to run flask server (string)
        :param port: port to run flask server (int)
        :return: None
        '''
        self.host = host
        self.port = port
        self.server_thread = threading.Thread(
            target=self.flask_server.run,
            kwargs={
                'host': self.host,
                'port': self.port,
            }
        )
        self.server_thread.start()


    def add_endpoint(self, endpoint, name, handler, methods):
        '''
        Add an endpoint to the flask app

        :param endpoint: url route (ex: /example)
        :param name: route name
        :param handler: function to call when endpoint is hit
        :param methods: list of methods (POST, GET, etc)
        :return: None
        '''
        self.flask_server.add_url_rule(endpoint, name, EndpointAction(handler), methods=methods)