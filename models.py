from google.appengine.ext import ndb


class TestNote(ndb.Model):
    date_created = ndb.DateProperty(auto_now_add=True)
    db_nursery_no1 = ndb.IntegerProperty()
    db_nursery_no2 = ndb.IntegerProperty()
    db_nursery_no3 = ndb.IntegerProperty()


class Note(ndb.Model):
    date_created = ndb.DateProperty(auto_now_add=True)
    db_nursery_no1 = ndb.IntegerProperty()
    db_nursery_no2 = ndb.IntegerProperty()
    db_nursery_no3 = ndb.IntegerProperty()
