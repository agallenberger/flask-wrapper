'''
Example usage of the Flask wrapper.
'''
import flask
import requests

import flask_wrapper


def main():
    app = MyFlaskApp()

    ## If host or port are None, the flask server will use default values of '127.0.0.1' and 5000
    host = flask_wrapper.get_ip()
    port = 5000
    app.flask.run(host=host, port=port)

    url = f'http://{host}:{port}/'
    res = requests.get(url + 'example-get')
    print(res.text)
    res = requests.post(url + 'example-post', json={'message': 'Hello world!'})
    print(res.text)


class MyFlaskApp():
    def __init__(self):
        self.flask = flask_wrapper.FlaskWrapper('Example')
        self.flask.add_endpoint(
            endpoint='/example-get',
            name='example-get',
            handler=self.example_get,
            methods=['GET']
        )
        self.flask.add_endpoint(
            endpoint='/example-post',
            name='example-post',
            handler=self.example_post,
            methods=['POST']
        )

    def example_get(self):
        return {
            'status': 'success',
            'message': 'This is an example GET',
        }

    def example_post(self):
        post = flask.request.json.get('message')
        return {
            'status': 'success',
            'message': f'This is an example POST. You sent: \'{post}\'',
        }


if __name__ == '__main__':
    main()