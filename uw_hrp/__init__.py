"""
This is the interface for interacting with
the hrp web service.
"""

import logging
from uw_hrp.dao import HRP_DAO
from restclients_core.exceptions import DataFailureException


logger = logging.getLogger(__name__)
hrp_dao = HRP_DAO()


def get_resource(url):
    response = hrp_dao.getURL(url, {'Accept': 'application/json'})

    logger.debug("{0} ==status==> {1}".format(url, response.status))
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    logger.debug("{0} ==data==> {1}".format(url, response.data))
    return response.data
