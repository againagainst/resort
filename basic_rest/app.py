'''
Created on May 2, 2018

@author: againagainst
'''
import logging
from http import HTTPStatus

import tornado.ioloop
import tornado.web


class BasicHander(tornado.web.RequestHandler):

    def get(self):
        '''Get a ping endpoint.
        ---
        description: Get a response for ping (pong)
        responses:
            200:
                description: A response to the client
                schema:
                    $ref: '#/definitions/pong'
        '''
        self.set_status(HTTPStatus.OK)
        self.write("pong")


class EchoHander(tornado.web.RequestHandler):

    def get(self, entity=None):
        '''Get an echo endpoint.
        ---
        description: Get an echo response
        responses:
            200:
                description: A response with sent body or url_entry
                schema:
                    $ref: '#/definitions/echo'
            204:
                description: An empty response
                schema:
                    $ref: '#/definitions/echo_empty'

        '''
        self.set_status(HTTPStatus.OK)
        if self.request.body:
            self.write(self.request.body)
        else:
            if entity:
                self.write(entity)
            else:
                self.set_status(HTTPStatus.NO_CONTENT)
        self.finish()

    def post(self, entity=None):
        self.write(self.request.body)


class AuthHander(tornado.web.RequestHandler):

    def get(self):
        tok = self.get_cookie('token')
        if tok == 'authorized':
            self.set_status(HTTPStatus.NO_CONTENT)
        else:
            self.set_status(HTTPStatus.UNAUTHORIZED)

    def post(self):
        self.set_cookie('token', 'authorized')

    def delete(self):
        self.clear_cookie('token')


def serve_basic_rest_server():
    logging.basicConfig(level=logging.DEBUG)
    handlers = ((r'/ping', BasicHander),
                (r'/echo/?([\w?&=]*)', EchoHander),
                (r'/session', AuthHander),
                )
    application = tornado.web.Application(handlers=handlers, debug=__debug__)
    # make_apispec(handlers)
    host = 'localhost'
    port = 8888
    logging.info(' - Serving at http://{host}:{port}'.format(host=host,
                                                             port=port))
    application.listen(port=port, address=host)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logging.info(' - Stop serving...')


if __name__ == "__main__":
    serve_basic_rest_server()
