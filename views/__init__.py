from . import inappoauth2
from . import choosegamebtns
from . import updatedata

from __main__ import bot


async def setup_hook():
    bot.add_view(inappoauth2.OAuthInApp_view())
    bot.add_view(choosegamebtns.ChooseGameButtons_view())
    bot.add_view(inappoauth2.OAuthInAppFailed_view())
    bot.add_view(updatedata.UpdateMemberData_view())
