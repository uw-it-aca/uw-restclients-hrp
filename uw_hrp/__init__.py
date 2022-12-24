# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the hrp web service.
"""

import logging
from uw_hrp.dao import HRP_DAO
from restclients_core.exceptions import DataFailureException


logger = logging.getLogger(__name__)


def get_resource(url):
    response = HRP_DAO().getURL(url, {'Accept': 'application/json'})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)
    return response.data
