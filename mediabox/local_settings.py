from mediabox.settings import *

from whitelist_auth.auth import require_whitelisted_wrapper
require_whitelisted_wrapper()
