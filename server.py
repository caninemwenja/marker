from __future__ import division

import tornado.ioloop
import tornado.web
import sockjs.tornado
import logging
import os
import parser_tool
import json
import utils

logging.getLogger().setLevel(logging.DEBUG)

logging.debug("Loading grammar...")
grammar = parser_tool.load_grammar('grammars/declarative.fcfg', cache=True)

def relation_extraction(sentence):
    trees = parser_tool.parse(grammar, sentence)

    try:
        node = trees[0].node
        subject = node['SUBJECT']
        predicate = node['PREDICATE']
        obj = node['OBJECT']

        if type("") != type(subject):
            subject = None
        if type("") != type(predicate):
            predicate = None
        if type("") != type(obj):
            obj = None
            
        return subject, predicate, obj, trees[0]
    except IndexError:
        raise Exception("No parse trees found")

def similarity(sentence1, sentence2):
    s1_rel = relation_extraction(sentence1)
    s2_rel = relation_extraction(sentence2)

    sub_syns = tuple()
    pred_syns = tuple()
    obj_syns = tuple()

    sub_syns = utils.similar(s1_rel[0], s2_rel[0])
    pred_syns = utils.similar(s1_rel[1], s2_rel[1])
    if s1_rel[2] and s2_rel[2]:
        obj_syns = utils.similar(s1_rel[2], s2_rel[2])

    pred_score = pred_syns[2] * pred_syns[2]

    sm = sub_syns[2] + pred_score + (obj_syns[2] or 1)
    avg = sm / 3

    result = {}

    result['score'] = avg
    result['sub_score'] = sub_syns[2]
    result['pred_score'] = pred_score
    result['obj_score'] = obj_syns[2] or 1

    if s1_rel[2] and s2_rel[2]:
        result['objs'] = [{'name': s1_rel[2], 'def': obj_syns[0].definition},
            {'name': s2_rel[2], 'def': obj_syns[1].definition},]
    elif s1_rel[2]: 
        result['objs'] = [{'name': s1_rel[2], 'def': obj_syns[0].definition},
            {'name': None, 'def': None},]

    else:
        result['objs'] = [{'name': None, 'def': None}, 
            {'name': s2_rel[2], 'def': obj_syns[1].definition},]

    result.update({
        'subs': [{ 'name': s1_rel[0], 'def': sub_syns[0].definition },
            { 'name': s2_rel[0], 'def': sub_syns[1].definition },],
        'preds': [{ 'name': s1_rel[1], 'def': pred_syns[0].definition },
            { 'name': s2_rel[1], 'def': pred_syns[1].definition },],
    })

    result['s1_tree'] = str(s1_rel[3])
    result['s2_tree'] = str(s2_rel[3])

    return result

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class EchoServer(sockjs.tornado.SockJSConnection):

    def on_open(self, info):
        logging.debug("Joined: %s" % repr(info))

    def on_message(self, message):
        logging.debug("Message: %s" % repr(message))
        msg = json.loads(message)
        
        teacher = msg['teacher']
        student = msg['student']

        response = {}

        try:
            response = similarity(teacher, student)
        except Exception, e:
            response['error'] = "Server Error: %s" % str(e)

        try:
            self.send(json.dumps(response))
        except TypeError, e:
            response = {}
            response['error'] = "Error sending json: %s" % str(e)
            self.send(json.dumps(response))

    def on_close(self):
        logging.debug("Closed")

if __name__ == "__main__":
    logging.debug("Grammar loaded.")

    logging.debug("Starting Server...")

    EchoRouter = sockjs.tornado.SockJSRouter(EchoServer, "/message")

    settings = {
        'debug': True,
        'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
    }

    handlers = [
        (r"/", IndexHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler),
    ]

    handlers += EchoRouter.urls

    app = tornado.web.Application(handlers, **settings)

    app.listen(8080)

    logging.debug("Listening...")

    tornado.ioloop.IOLoop.instance().start()
