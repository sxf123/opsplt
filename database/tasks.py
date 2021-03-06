from __future__ import absolute_import
from celery import shared_task
import subprocess
from opsplt.settings import FLYWAY_BASEDIR
import os
import jinja2
import logging
from database.models import Result

logger = logging.getLogger("default")

@shared_task
def database_init(schema_name,schema_url,schema_username,schema_password):
    conf_dir = os.path.join(FLYWAY_BASEDIR,"conf")
    flyway_dir = os.path.join(FLYWAY_BASEDIR,"flyway")
    loader = jinja2.FileSystemLoader(searchpath="flyway/")
    env = jinja2.Environment(loader=loader)
    template = env.get_template("flyway.conf","utf-8")
    content = template.render(schema_name=schema_name,schema_url=schema_url,schema_username=schema_username,schema_password=schema_password)
    f = os.path.join(conf_dir,"{}-{}.conf".format(schema_name,schema_url))
    with open(f,"w") as fp:
        fp.write(content)
        fp.close()
    res = subprocess.getstatusoutput("{0} -configFiles={1} baseline".format(flyway_dir,f))
    logger.info('[INFO] output: ' + res[1])
    return res

@shared_task
def db_migrate(configFile):
    flyway_dir = os.path.join(FLYWAY_BASEDIR,'flyway')
    config_dir = os.path.join(FLYWAY_BASEDIR,'conf')
    config_file = os.path.join(config_dir,configFile)
    res = subprocess.getstatusoutput("{0} -configFiles={1} migrate".format(flyway_dir,config_file))
    result = Result(
        migrate_id=db_migrate.request.id,
        migrate_status=res[0],
        migrate_result=res[1]
    )
    result.save()
    return res
