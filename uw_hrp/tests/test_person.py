# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from restclients_core.exceptions import (
    DataFailureException, InvalidEmployeeID, InvalidRegID, InvalidNetID)
from uw_hrp.person import (
    get_person_by_netid, get_person_by_employee_id, get_person_by_regid,
    person_search)
from uw_hrp.util import fdao_hrp_override


@fdao_hrp_override
class PersonTest(TestCase):

    def test_get_person_by_netid(self):
        self.assertRaises(DataFailureException,
                          get_person_by_netid,
                          "None")
        self.assertRaises(InvalidNetID,
                          get_person_by_netid,
                          "")

        person = get_person_by_netid("faculty")
        self.assertIsNotNone(person)
        self.assertEqual(person.regid, "10000000000000000000000000000005")
        self.assertEqual(person.employee_id, "000000005")
        self.assertEqual(person.student_id, "1000005")
        self.assertTrue(person.is_active)
        self.assertEqual(person.primary_manager_id, "845007271")
        self.assertEqual(len(person.worker_details), 1)
        position = person.worker_details[0]
        self.assertEqual(len(position.other_active_positions), 0)
        self.maxDiff = None
        self.assertEqual(
            position.employee_status.to_json(),
            {
                'hire_date': '2006-05-16 00:00:00-07:00',
                'is_active': True,
                'is_retired': False,
                'is_terminated': False,
                'retirement_date': None,
                'status': 'Active',
                'termination_date': None
            })
        self.assertEqual(
            position.primary_position.to_json(),
            {
                'end_date': None,
                'is_primary': True,
                'job_class': 'Academic Personnel',
                'job_profile': {
                    'description': 'Unpaid Academic',
                    'job_code': '21184'
                },
                'job_title': 'Clinical Associate Professor',
                'location': 'Seattle Campus',
                'org_unit_code': '',
                'pos_type': 'Unpaid Academic',
                'start_date': '2012-07-01 00:00:00-07:00',
                'supervisor_eid': '845007271',
                'supervisory_org': {
                    'budget_code': '',
                    'org_code': 'SOM',
                    'org_name': 'Family Medicine: King Pierce JM Academic'}
            })

        person = get_person_by_netid("faculty", include_future=True)
        self.assertIsNotNone(person)

    def test_get_person_by_employee_id(self):
        person = get_person_by_employee_id("000000005")
        self.assertTrue(person.netid, 'faculty')

        self.assertRaises(InvalidEmployeeID,
                          get_person_by_employee_id,
                          "")

    def test_get_person_by_regid(self):
        person = get_person_by_regid("9136CCB8F66711D5BE060004AC494FFE")
        self.assertTrue(person.netid, 'javerage')

        self.assertRaises(InvalidRegID,
                          get_person_by_regid, "000")

    def test_person_search(self):
        pass
        # persons = person_search(changed_since_date="2022-12-12")
        # self.assertEqual(len(persons), 0)
