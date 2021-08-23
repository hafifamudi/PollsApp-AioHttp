from aiohttp import web

from settings import BASE_DIR, config
from routes import setup_routes
from db import pg_context

import aiohttp_jinja2
import jinja2

# create web instance
app = web.Application()

# create routes setup
setup_routes(app)

# db clean up context
app.cleanup_ctx.append(pg_context)

# load config .yaml
app['config'] = config

#load the templates
aiohttp_jinja2.setup(app,
                    loader = jinja2.FileSystemLoader(str(BASE_DIR / 'aiohttp_polls' / 'templates')))

# run the app with all configuration
web.run_app(app)