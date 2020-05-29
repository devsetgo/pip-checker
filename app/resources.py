# -*- coding: utf-8 -*-
from loguru import logger
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from com_lib import db_setup
from com_lib.db_setup import create_db
from com_lib.demo_data import make_a_lot_of_calls
import settings

# templates and static files
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="statics")


async def startup():

    logger.info("starting up services")
    await db_setup.connect_db()

    if settings.DEMO_DATA_CREATE == True:
        logger.info("Creating Demo Data")

    await make_a_lot_of_calls()


async def shutdown():

    logger.info("shutting down services")
    await db_setup.disconnect_db()


def init_app():

    # config_log()
    # logger.info("Initiating application")
    create_db()
    logger.info("Initiating database")
