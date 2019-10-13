from views.auth import auth
from views.calendars import calendars
from views.databases import databases
from views.settings import settings
from views.syncs import syncs
from views.user import user

blueprints = [auth, user, calendars, settings, syncs, databases]
