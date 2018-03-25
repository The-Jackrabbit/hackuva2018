from django.db import models
from django.db.models import Q
# Create your models here.

def convert_to_set(arr):
	a = []
	c = {}
	for i in range(len(arr)):
		if arr[i] not in c:
			a.append(arr[i])
	return a
'''
class Profile(models.Model):
	join_data = models.DateTimeField()
	username = models.CharField(max_length=250)
	first_name = models.CharField(max_length=250)
	last_name = models.CharField(max_length=250)
	email = models.CharField(max_length=250)
	password = models.CharField(max_length=250)
'''

class FileUpload(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	datafile = models.ImageField(upload_to='media/users/', blank=True, null=True)

class User(models.Model):
	real_name = models.CharField(max_length=250)
	tag = models.CharField(max_length=250)
	profile_picture = models.ImageField(upload_to='media/users/', blank=True, null=True)
	icon_url = models.CharField(max_length=250, blank=True, null=True)
	join_date = models.DateTimeField()
	bio = models.TextField(blank=True, null=True)
	
	def __str__(self):
		return self.real_name
	
	def get_sets(self):
		sets = Set.objects.filter(player_one=self)
		return sets

	def get_badges(self):
		badges = BadgesToUsers.objects.filter(user=self)
		return badges

	def get_all_tags(self):
		tag_data = {
			"current": self.tag,
			"past": []
		}

		tags = UserTags.objects.filter(user=self)
		past_tags = []
		for tag in tags:
			old_tag = {
				"tag": tag.tag,
				"tournament": tag.tournament
			}
			past_tags.append(old_tag)
		return tag_data

	def get_win_rate(self):
		won_sets = Set.objects.filter(victor=self)
		lost_sets = Set.objects.filter(loser=self)
		if len(won_sets) + len(lost_sets) == 0:
			rate = 0
		else:
			rate = 100*float(len(won_sets)/(len(won_sets) + len(lost_sets)))
		data = {
			"wins": len(won_sets),
			"loses": len(lost_sets),
			"total": len(won_sets) + len(lost_sets),
			"win_rate": round(rate,2)
		}
		return data

	def get_vs_info(self):
		users = User.objects.filter(~Q(self))
		for user in users:	
			Set.objects.filter((Q(player_one=self) & Q(player_two=user)) | (Q(player_two=self) & Q(player_one=user)))	

		return {}

	def get_seasons(self):
		t_2_us = TournamentToUsers.objects.filter(user=self)
		s = {}
		for t_2_u in t_2_us:
			
			t = t_2_u.tournament
			
			t_s = t.season
			
			s[t_s.pk] = t_s.__str__()

		return s

	def get_opponents(self, season=None):
		sets = Set.objects.filter( Q(player_one=self)| Q(player_two=self) )

		opponents = {}
		
		for s in sets:
			if season is None or s.tournament.season.pk == season.pk:
				opp = s.player_one
				if str(s.player_one.pk) == str(self.pk):
					opp = s.player_two

				try:
					iconUrl = opp.icon_url
				except ValueError:
					iconUrl = ""
				opp_data = {
					"name": opp.real_name,
					"icon": iconUrl
				}
				opponents[opp.pk] = opp_data
		
		return opponents

	def get_opponent_comparison(self, opponent, season=None):
		user_wins = Set.objects.filter(
			((Q(player_one=self) & Q(player_two=opponent)) | 
			(Q(player_two=self) & Q(player_one=opponent))) & 
			Q(victor=self)
		)
		opponent_wins = Set.objects.filter(
			((Q(player_one=self) & Q(player_two=opponent)) | 
			(Q(player_two=self) & Q(player_one=opponent))) & 
			Q(victor=opponent)
		)
		wins = 0
		loses = 0
		for uw in user_wins:
			if uw.tournament.season is None or uw.tournament.season == season:
				wins += 1

		
		for ow in opponent_wins:
			if ow.tournament.season is None or ow.tournament.season == season:
				loses += 1
		
		data = {
			"wins": wins,
			"loses": loses
		}

		return data

class Season(models.Model):
	name = models.CharField(max_length=250)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	
	def __str__(self):
		return self.name
	
	def get_tournaments(self):
		tournaments = Tournament.objects.filter(season=self)
		return tournaments

	def get_players(self):
		tournaments = self.get_tournaments()
		players = []

		for tournament in tournaments:
			tournaments_players = tournament.get_players()
			players.extend(tournaments_players)

		players = set(players)

		return players

class Tournament(models.Model):
	date = models.DateTimeField()
	name = models.CharField(max_length=250)
	season = models.ForeignKey(Season)

	def __str__(self):
		return self.name

	def get_sets(self):
		tournament_sets = Set.objects.filter(tournament=self)
		return tournament_sets

	def get_players(self):
		tournament_players = TournamentToUsers.objects.filter(tournament=self)
		return tournament_players

class UserTags(models.Model):
	user = models.ForeignKey(User)
	tournament = models.ForeignKey(Tournament)
	tag = models.CharField(max_length=250)

	def __str__(self):
		return self.tag

class TournamentToUsers(models.Model):
	tournament = models.ForeignKey(Tournament)
	user = models.ForeignKey(User)

class Set(models.Model):
	victor = models.ForeignKey(User, related_name='set_victor_id', blank=True, null=True)
	loser = models.ForeignKey(User, related_name='set_loser_id', blank=True, null=True)
	
	tournament = models.ForeignKey(Tournament)

	child_set = models.ForeignKey('self', blank=True, null=True)

	player_one = models.ForeignKey(User, related_name='set_player_one_id')
	player_two = models.ForeignKey(User, related_name='set_player_two_id')

	def __str__(self):
		set_name = self.player_one.real_name + " vs. " + self.player_two.real_name 
		return set_name

	def get_games(self):
		games = Game.objects.filter(set=self)
		return games

	def get_opponent(self, pk):
		if str(pk) == str(self.player_one.pk):
			return self.player_two.pk
		return self.player_one.pk
		
	def set_victor(self):
		games = self.get_games()
		wins = [0, 0]
		for game in games:
			wins[game.victor] += 1
		
		if wins[0] > wins[1]:
			self.victor = self.player_one
			self.loser = self.player_two
		elif wins[0] < wins[1]:
			self.victor = self.player_two
			self.loser = self.player_one

class Game(models.Model):
	
	VICTOR_CHOICES = (
		(0, 'Player 1'),
		(1, 'Player 2')
	)
	
	victor = models.IntegerField(
		choices=VICTOR_CHOICES
	)
	set = models.ForeignKey(Set)
	round_number = models.IntegerField(default=1, blank=True)
	
	def __str__(self):
		game_name = self.set.__str__() + " - Round " + str(self.round_number)
		return game_name

	def get_players(self):
		return {
			'player_one': self.set.player_one, 
			'player_two': self.set.player_two
		}

class PowerRank(models.Model):
	season = models.ForeignKey(Season)
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name

class PowerRankToUsers(models.Model):
	powerrank = models.ForeignKey(PowerRank)
	user = models.ForeignKey(User)
	rank = models.IntegerField()

	def __str__(self):
		return self.powerrank.__str__() + " - " + self.user.__str__() + " - " + str(self.rank)

class Badge(models.Model):
	name = models.CharField(max_length=250)
	badge_image = models.ImageField(upload_to='media/badges/', blank=True)
	points = models.IntegerField()

	def __str__(self):
		return self.name

class BadgesToUsers(models.Model):
	badge = models.ForeignKey(Badge)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.user.__str__() + " - " + self.badge.name

