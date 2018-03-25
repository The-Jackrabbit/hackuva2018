from django.contrib import admin

# Register your models here.
''' 
superuser
username: root
password: hackuva2018
'''
from .models import User, UserTags, Season, Tournament, TournamentToUsers, Set, Game, PowerRank, PowerRankToUsers, Badge, BadgesToUsers, FileUpload

# Register your models here.
admin.site.register(User)
admin.site.register(FileUpload)
admin.site.register(UserTags)
admin.site.register(Season)
admin.site.register(Tournament)
admin.site.register(TournamentToUsers)
admin.site.register(Set)
admin.site.register(Game)
admin.site.register(PowerRank)
admin.site.register(PowerRankToUsers)
admin.site.register(Badge)
admin.site.register(BadgesToUsers)

