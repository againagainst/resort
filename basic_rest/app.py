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
        self.set_status(HTTPStatus.OK)
        self.write("pong")

application = tornado.web.Application([
    (r'/ping', BasicHander),

], debug=__debug__)

if __name__ == "__main__":
    # host = 'http://127.0.0.1'
    logging.basicConfig(level=logging.DEBUG)
    host = 'localhost'
    port = 8888
    logging.info(' - Serving at http://{host}:{port}'.format(host=host,
                                                             port=port))
    application.listen(port=port, address=host)
    tornado.ioloop.IOLoop.current().start()
