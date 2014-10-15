# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from apecoffee import app

app.run(debug=app.debug)