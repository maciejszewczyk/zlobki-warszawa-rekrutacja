#!/usr/bin/env python

import webapp2
import urllib2
import urllib
import re
from google.appengine.ext import ndb

from models import TestNote
from models import Note
import datetime
import os
import jinja2
import logging

url = 'https://www.zlobki.waw.pl/rekrutacja2012/index.php'
pesel = '00000000000'
pin = '0000'
imie = 'ANNA'
nazwisko = 'KOWALSKA'
userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
nursery_no1 = '1' #numer zlobka 1
nursery_no2 = '1'
nursery_no3 = '1'
start_value_nursery_no1 = 1 # poczatkowe miejsce z dnia zarejestrowania w systemie dla zlobka 1 
start_value_nursery_no2 = 1
start_value_nursery_no3 = 1
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        # https://stackoverflow.com/questions/40023743/google-charts-date-axis-labels-not-correct
        q = ndb.gql("SELECT * FROM Note ORDER BY date_created")
        results = q.fetch()
        ret = ''
        for el in results:
            # for Google Charts JS format: [new Date(2019, 5, 22),  37.8, 80.8, 41.8],
            ret += "[new Date({}, {}-1, {}), {}, {}, {}],".format(el.date_created.strftime("%Y"),
                                                                el.date_created.strftime("%-m"),
                                                                el.date_created.strftime("%-d"),
                                                                el.db_nursery_no1,
                                                                el.db_nursery_no2,
                                                                el.db_nursery_no3)
        q = ndb.gql("SELECT * FROM Note ORDER BY date_created DESC")
        results = q.fetch(1)
        last_value_no1, last_value_no2, last_value_no3, date_created = '', '', '', ''
        for el in results:
            last_value_no1 = el.db_nursery_no1
            last_value_no2 = el.db_nursery_no2
            last_value_no3 = el.db_nursery_no3
            date_created = el.date_created
        end_value_nursery_no1 = last_value_no1 - start_value_nursery_no1
        end_value_nursery_no2 = last_value_no2 - start_value_nursery_no2
        end_value_nursery_no3 = last_value_no3 - start_value_nursery_no3
        evno1 = "{0:+}".format(end_value_nursery_no1)
        evno2 = "{0:+}".format(end_value_nursery_no2)
        evno3 = "{0:+}".format(end_value_nursery_no3)
        yesterday = date_created - datetime.timedelta(days=1)
        id_date = yesterday.strftime("%Y-%m-%d")
        k = ndb.Key('Note', id_date)
        e = k.get()
        day2day_nursery_no1 = last_value_no1 - e.db_nursery_no1
        day2day_nursery_no2 = last_value_no2 - e.db_nursery_no2
        day2day_nursery_no3 = last_value_no3 - e.db_nursery_no3
        d2dno1 = "{0:+}".format(day2day_nursery_no1)
        d2dno2 = "{0:+}".format(day2day_nursery_no2)
        d2dno3 = "{0:+}".format(day2day_nursery_no3)
        template_context = {'body': ret,
                            'last_score_db_nursery_no1': last_value_no1,
                            'last_score_db_nursery_no2': last_value_no2,
                            'last_score_db_nursery_no3': last_value_no3,
                            'evno1': evno1,
                            'evno2': evno2,
                            'evno3': evno3,
                            'd2dno1': d2dno1,
                            'd2dno2': d2dno2,
                            'd2dno3': d2dno3
                            }
        template = jinja_env.get_template('templates/chart.html')
        self.response.out.write(template.render(template_context))


class RawView(webapp2.RequestHandler):
    def get(self):
        q = ndb.gql("SELECT * FROM Note ORDER BY date_created DESC")
        results = q.fetch()
        ret = ''
        for el in results:
            ret += "{};{};{};{}<br>".format(el.date_created, el.db_nursery_no1, el.db_nursery_no2, el.db_nursery_no3)

        template_context = {'body': ret}
        template = jinja_env.get_template('templates/main.html')
        self.response.out.write(template.render(template_context))


class TestRawView(webapp2.RequestHandler):
    def get(self):
        q = ndb.gql("SELECT * FROM Note ORDER BY date_created DESC")
        results = q.fetch(1)
        ret = ''
        for el in results:
            ret += "{};{};{};{}<br>".format(el.date_created, el.db_nursery_no1, el.db_nursery_no2, el.db_nursery_no3)

        template_context = {'body': ret}
        template = jinja_env.get_template('templates/main.html')
        self.response.out.write(template.render(template_context))


class TestGet(webapp2.RequestHandler):
    def get(self):
        id_date = datetime.datetime.now().strftime("%Y-%m-%d")
        k = ndb.Key('Note', id_date)
        e = k.get()
        ret = "{};{};{}<br>".format(e.db_nursery_no1, e.db_nursery_no2, e.db_nursery_no3)
        template_context = {'body': ret}
        template = jinja_env.get_template('templates/main.html')
        self.response.out.write(template.render(template_context))


class CurrentTime(webapp2.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        utc_now = datetime.datetime.utcnow()
        td = datetime.datetime.today()
        bd = "{}<br>{}<br>{}<br>".format(now, utc_now, td)
        template_context = {'body': bd}
        template = jinja_env.get_template('templates/main.html')
        self.response.out.write(template.render(template_context))


class TestView(webapp2.RequestHandler):
    def get(self):
        q = ndb.gql("SELECT * FROM TestNote ORDER BY date_created")
        results = q.fetch()
        ret = ''
        for el in results:
            ##      [new Date(2019, 5, 22),  37.8, 80.8, 41.8],
            ret += "[new Date({}, {}, {}), {}, {}, {}],".format(el.date_created.strftime("%Y"),
                                                                el.date_created.strftime("%-m"),
                                                                el.date_created.strftime("%-d"),
                                                                el.db_nursery_no1,
                                                                el.db_nursery_no2,
                                                                el.db_nursery_no3)

        template_context = {'body': ret}
        template = jinja_env.get_template('templates/test_chart.html')
        self.response.out.write(template.render(template_context))

'''
class TestMultiInsert(webapp2.RequestHandler):
    def get(self):
        TestNote.date_created._auto_now_add = False
        entities = []
        for i in range(469):
            test_note = TestNote(db_nursery_no1=1*i,
                                 db_nursery_no2=1*i,
                                 db_nursery_no3=1*i,
                                 date_created=datetime.date(2019, 5, 28) + datetime.timedelta(days=i))
            entities.append(test_note)
        ndb.put_multi(entities)
        self.response.out.write('Test Multi Insert Done!')


class Insert(webapp2.RequestHandler):
    def get(self):
        Note.date_created._auto_now_add = False
        note = Note(id=datetime.date(2019, 5, 26).strftime("%Y-%m-%d"),
                    db_nursery_no1=52,
                    db_nursery_no2=69,
                    db_nursery_no3=98,
                    date_created=datetime.date(2019, 5, 26))
        note.put()
        self.response.out.write('Production Note Inserted')


class TestInsert(webapp2.RequestHandler):
    def get(self):
        TestNote.date_created._auto_now_add = False
        test_note = TestNote(id=datetime.date(2019, 5, 22).strftime("%Y-%m-%d"),
                             db_nursery_no1=3,
                             db_nursery_no2=3,
                             db_nursery_no3=3,
                             date_created=datetime.date(2019, 5, 22))
        test_note.put()
        self.response.out.write('Test Note Inserted')
'''


class CronUpdate(webapp2.RequestHandler):
    def post(self):
        self.abort(405, headers=[('Allow', 'GET')])

    def get(self):
        if 'X-AppEngine-Cron' not in self.request.headers:
            self.error(403)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.HTTPHandler(debuglevel=1))
        req = urllib2.Request(url)
        req.add_header('User-Agent', userAgent)
        opener.open(req)

        data_stage1 = {
            'pesel': pesel,
            'akcja': 'sprawdzpesel'
        }

        encoded_data_stage1 = urllib.urlencode(data_stage1)
        req = urllib2.Request(url)
        req.add_data(encoded_data_stage1)
        req.add_header('User-Agent', userAgent)
        opener.open(req)

        data_stage2 = {
            'imie': imie,
            'nazwisko': nazwisko,
            'pesel': pesel,
            'akcja': 'login',
            'pin': pin
        }

        encoded_data_stage2 = urllib.urlencode(data_stage2)
        req = urllib2.Request(url)
        req.add_data(encoded_data_stage2)
        req.add_header('User-Agent', userAgent)
        result = opener.open(req).read().decode('iso-8859-2')
        zlobek1 = re.search(r"<li>I  wybor ZLOBEK nr <strong>%s</strong>  --> MIEJSCE: <strong> (\d+)</strong>"
                            % nursery_no1, result)
        zlobek1 = zlobek1.group(1)
        zlobek2 = re.search(r"<li>II wybor ZLOBEK nr <strong>%s</strong> --> MIEJSCE: <strong> (\d+)</strong>"
                            % nursery_no2, result)
        zlobek2 = zlobek2.group(1)
        zlobek3 = re.search(r"<li>III wybor ZLOBEK nr <strong>{}</strong> --> MIEJSCE: <strong> (\d+)</strong>"
                            .format(nursery_no3), result)
        zlobek3 = zlobek3.group(1)

        id_date = datetime.datetime.now().strftime("%Y-%m-%d")
        note = Note(id=id_date,
                    db_nursery_no1=int(zlobek1),
                    db_nursery_no2=int(zlobek2),
                    db_nursery_no3=int(zlobek3))
        note.put()
        logging.info("!! INFO !! CRON on {} Z1:{} Z2:{} Z3:{}".format(id_date, zlobek1, zlobek2, zlobek3))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/raw_view', RawView),
    ('/test_raw_view', TestRawView),
    ('/test_get', TestGet),
    ('/test_view', TestView),
    ('/cron', CronUpdate),
    #   ('/insert', Insert),
    #   ('/test_insert', TestInsert),
    #   ('/test_multi_insert', TestMultiInsert),
    ('/time', CurrentTime)
], debug=False)
