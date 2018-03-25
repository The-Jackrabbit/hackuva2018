from django.test import TestCase, Client
from .models import *
from django.core.urlresolvers import reverse
import datetime

class UserTests(TestCase):
    def setUp(self):
        self.entry = User(real_name="Luke Masters",
                     tag = {"current" : "champion", "past":[]})
    def test_string_representation(self):
        self.assertEqual(str(self.entry), self.entry.real_name)

    def test_tags(self):
        self.assertEqual(self.entry.tag, {"current" : "champion", "past":[]} )

class SeasonTests(TestCase):
    def setUp(self):
        self.season = Season(name="First",
                     start_date = datetime.datetime(2003, 8, 4, 12, 30, 45),
                     end_date = datetime.datetime(2003, 8, 4, 12, 30, 45))
    def test_string_representation(self):
        self.assertEqual(str(self.season), "First")

    def test_start_date(self):
        self.assertEqual(self.season.start_date, datetime.datetime(2003, 8, 4, 12, 30, 45))
    def test_end_date(self):
        self.assertEqual(self.season.end_date, datetime.datetime(2003, 8, 4, 12, 30, 45))

class TorunamentTests(TestCase):
    def setUp(self):
        self.tournament = Tournament(name="This Tournament",
                     date = datetime.datetime(2003, 8, 4, 12, 30, 45))
    def test_string_representation(self):
        self.assertEqual(str(self.tournament), "This Tournament")

    def test_date(self):
        self.assertEqual(self.tournament.date, datetime.datetime(2003, 8, 4, 12, 30, 45))
class SetTests(TestCase):
     # <--- gets the first tournament cause we just need one and I’m too lazy to properly instantiate ones = Set(

    def setUp(self):
        self.set = Set(player_one=User(real_name="John", tag="sss"),
                    player_two=User(real_name="Jack", tag="f0x"),
                    tournament= Tournament(date = datetime.datetime(2003, 8, 4, 12, 30, 45),
                                            name= "This Tournament",
                                            season=  Season(name="First",
                                                         start_date = datetime.datetime(2003, 8, 4, 12, 30, 45),
                                                         end_date = datetime.datetime(2003, 8, 4, 12, 30, 45)))
                     )
    def test_string_player_one(self):
        self.assertEqual(str(self.set.player_one), "John")
    def test_string_player_two(self):
        self.assertEqual(str(self.set.player_two), "Jack")
    def test_string_season(self):
        self.assertEqual(str(self.set.tournament.season.name), "First")
    # def test_date(self):
    #     self.assertEqual(self.tournament.date, datetime.datetime(2003, 8, 4, 12, 30, 45))

    # def get_sets_test(self):

# Create your tests here.
