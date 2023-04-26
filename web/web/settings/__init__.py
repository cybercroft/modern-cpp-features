from .base import *

if DEBUG:
    from .local import *
else:
    from .prod import *