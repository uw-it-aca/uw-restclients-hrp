# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the HRP Web Service.
"""

from datetime import datetime
import logging
import json
import re
from urllib.parse import urlencode
from restclients_core.exceptions import (
    InvalidRegID, InvalidNetID, InvalidEmployeeID)
from uw_hrp import get_resource
from uw_hrp.models import Person


logger = logging.getLogger(__name__)
re_netid = re.compile(r'^[a-z][a-z0-9\-\_\.]{,127}$', re.I)
re_regid = re.compile(r'^[A-F0-9]{32}$', re.I)
re_employee_id = re.compile(r'^\d{9}$')
URL_PREFIX = "/hrp/v3/person"
SUFFIX = "future_worker=true"


def get_person_by_employee_id(employee_id, include_future=False):
    if not valid_employee_id(employee_id):
        raise InvalidEmployeeID(employee_id)
    return _get_person(employee_id, include_future)


def get_person_by_netid(netid, include_future=False):
    if not valid_uwnetid(netid):
        raise InvalidNetID(netid)
    return _get_person(netid, include_future)


def get_person_by_regid(regid, include_future=False):
    if not valid_uwregid(regid):
        raise InvalidRegID(regid)
    return _get_person(regid, include_future)


def _get_person(id, include_future):
    """
    Return a restclients.models.hrp.WorkerDetails object
    """
    url = "{0}/{1}.json".format(URL_PREFIX, id)
    if include_future:
        url = "{0}?{1}".format(url, SUFFIX)
    return Person(data=json.loads(get_resource(url)))


def person_search(**kwargs):
    """
    Returns a list of Person objects
    Parameters can be:
        active_appointment: true|false
        changed_since_date: string
        cost_center: string
        current_faculty: true|false
        future_worker: string
        location: string
        supervisory_organization: string
        worker_wid: string
    """
    url = "{0}.json?{1}&page_size=200".format(URL_PREFIX, urlencode(kwargs))
    persons = []
    while True:
        data = json.loads(get_resource(url))
        if "Persons" in data:
            for person_record in data.get("Persons"):
                persons.append(Person(data=person_record))
        if (data.get("Next") and data["Next"].get("Href") and
                len(data["Next"]["Href"]) > 0):
            url = data["Next"]["Href"]
        else:
            break
    return persons


def valid_uwnetid(netid):
    return (netid is not None and
            re_netid.match(str(netid)) is not None)


def valid_uwregid(regid):
    return (regid is not None and
            re_regid.match(str(regid)) is not None)


def valid_employee_id(employee_id):
    return (employee_id is not None and
            re_employee_id.match(str(employee_id)) is not None)
