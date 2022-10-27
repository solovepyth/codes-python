""""""

import logging
from typing import Dict
from jinja2 import Template,Environment, PackageLoader
import detailtrans as dt 

from task_manager import rest_client
from config.config import Variables


LOG_FORMAT = '%(asctime)s %(message)s'


def execute(variables: Variables):
    """
    :param variables:
    :return:
    """
    logging.basicConfig(format=LOG_FORMAT)
    logger = logging.getLogger('connect')
    logger.setLevel(logging.INFO)
	template = Environment(loader=PackageLoader('application.json', ''), autoescape=True).get_template(variables.JSON_CONF_TEMPLATE_FILE)
	conf = json.loads(template.render(variables=variables))
	dt.job(conf)
