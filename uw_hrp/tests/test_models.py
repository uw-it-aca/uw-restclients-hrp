# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from datetime import datetime, timedelta, timezone
from uw_hrp.models import (
    EmploymentStatus, JobProfile, SupervisoryOrganization,
    EmploymentDetails, WorkerDetails, Person, parse_date)
from uw_hrp.util import fdao_hrp_override


@fdao_hrp_override
class ModelsTest(TestCase):

    def test_parse_date(self):
        self.assertIsNotNone(parse_date("2017-09-16T07:00:00.000Z"))

    def test_employment_status(self):
        emp_status0 = EmploymentStatus(status="Active", is_active=True)
        self.assertIsNotNone(emp_status0)
        self.assertEqual(
            emp_status0.to_json(),
            {
                'hire_date': None,
                'is_active': True,
                'is_retired': False,
                'is_terminated': False,
                'retirement_date': None,
                'status': 'Active',
                'termination_date': None
            })

        emp_status = EmploymentStatus(
            data={
                "HireDate": "2006-05-16T00:00:00-07:00",
                "OriginalHireDate": "2006-05-16T00:00:00-07:00",
                "ExpectedFixedTermEndDate": None,
                "FirstDayOfWork": "2006-05-16T00:00:00-07:00",
                "ActiveStatusDate": "2006-05-16T00:00:00-07:00",
                "Active": True,
                "EmployeeStatus": "Active",
                "Terminated": False,
                "TerminationDate": None,
                "TerminationInvoluntary": None,
                "TerminationReason": None,
                "Retired": False,
                "RetirementDate": None,
                "RetirementApplicationDate": None,
                "DisplayLeave": False,
                "LeaveStatusDetails": []
                })

        self.assertTrue(emp_status.is_active)
        self.assertEqual(
            emp_status.to_json(),
            {
                'hire_date': '2006-05-16 00:00:00-07:00',
                'is_active': True,
                'is_retired': False,
                'is_terminated': False,
                'retirement_date': None,
                'status': 'Active',
                'termination_date': None
            })
        self.assertIsNotNone(str(emp_status))

    def test_job_profile(self):
        job_prof = JobProfile(job_code="1", description="A")
        self.assertIsNotNone(job_prof)
        job_prof = JobProfile(
            data={
                "Name": "Unpaid Academic",
                "WID": "d957207a306801fc5c30a8906f5c6b57",
                "IDs": [
                    {
                        "Type": "WID",
                        "Value": "d957207a306801fc5c30a8906f5c6b57"
                    },
                    {
                        "Type": "Job_Profile_ID",
                        "Value": "21184"
                    }
                ]
            }
        )
        self.assertEqual(
            job_prof.to_json(),
            {
                'job_code': '21184', 'description': 'Unpaid Academic'
            }
        )
        self.assertIsNotNone(str(job_prof))

    def test_supervisory_organization(self):
        super_org = SupervisoryOrganization(
            org_code="HSA:",
            org_name="EHS: Occl Health - Acc Prevention")
        self.assertIsNotNone(super_org)
        super_org = SupervisoryOrganization(
            data={
                "Name": "SOM: Family Medicine: King Pierce JM Academic ( ())",
            }
        )
        self.assertEqual(
            super_org.to_json(),
            {
                'org_code': 'SOM',
                'org_name': 'Family Medicine: King Pierce JM Academic'
            }
        )
        self.assertIsNotNone(str(super_org))

    def test_employment_details(self):
        emp_details = EmploymentDetails()
        self.assertIsNotNone(emp_details)
        emp_details = EmploymentDetails(
            data={
                "PrimaryPosition": True,
                "BusinessTitle": "Clinical Associate Professor",
                "FTEPercent": 0.0,
                "StartDate": "2012-07-01T00:00:00-07:00",
                "PositionVacateDate": None,
                "JobProfile": {
                    "Name": "Unpaid Academic",
                },
                "PositionWorkerType": {
                    "Name": "Unpaid Academic",
                },
                "JobClassificationSummaries": [
                    {
                        "JobClassification": {
                            "Name": "F - Academic Personnel (Employment)",
                        },
                    }
                ],
                "Location": {
                    "Name": "Seattle Campus",
                },
                "OrganizationDetails": [
                    {
                        "Organization": {
                            "Name": "12",
                        }
                    }
                ],
                "Managers": [
                    {
                        "Name": "Joj, Pop",
                        "WID": "",
                        "IDs": [
                                    {
                                        "Type": "Employee_ID",
                                        "Value": "123456789",
                                    }
                                ],
                    }
                ],
                "SupervisoryOrganization": {
                    "Name": "SOM: Family Medicine (... (Inherited))",
                }
            }
        )
        self.assertEqual(
            emp_details.to_json(),
            {
                'end_date': None,
                'fte_percent': 0.0,
                'is_primary': True,
                'job_class': 'Academic Personnel',
                'job_profile': {
                    'description': 'Unpaid Academic',
                    'job_code': None
                },
                'location': 'Seattle Campus',
                'org_unit_code': '12',
                'pos_type': 'Unpaid Academic',
                'start_date': '2012-07-01 00:00:00-07:00',
                'supervisor_eid': '123456789',
                'supervisory_org': {
                    'org_code': 'SOM',
                    'org_name': 'Family Medicine'
                },
                'title': 'Clinical Associate Professor'
            }
        )
        self.assertIsNotNone(str(emp_details))

    def test_wwoker_details(self):
        pos = WorkerDetails(worker_wid="1b68136df25201c0710e3ddad462fa1d")
        self.assertIsNotNone(pos)
        self.assertEqual(
            pos.to_json(),
            {
                'active_positions': [],
                'employee_status': None,
                'primary_manager_id': None,
                'worker_wid': '1b68136df25201c0710e3ddad462fa1d'
            }
        )

        work_position = WorkerDetails(
            data={
                "WID": "1b68136df25201c0710e3ddad462fa1d",
                "EmploymentStatus": {
                    "HireDate": "2022-06-13T00:00:00-07:00",
                    "OriginalHireDate": "2022-06-13T00:00:00-07:00",
                    "ExpectedFixedTermEndDate": None,
                    "FirstDayOfWork": "2022-06-13T00:00:00-07:00",
                    "ActiveStatusDate": "2022-07-16T00:00:00-07:00",
                    "Active": False,
                    "EmployeeStatus": "Terminated",
                    "Terminated": True,
                    "TerminationDate": "2022-07-15T00:00:00-07:00",
                    "TerminationInvoluntary": None,
                    "TerminationReason": None,
                    "Retired": False,
                    "RetirementDate": None,
                    "RetirementApplicationDate": None,
                    "DisplayLeave": False,
                    "LeaveStatusDetails": []
                },
            }
        )
        self.assertEqual(
            work_position.to_json(),
            {
                'worker_wid': "1b68136df25201c0710e3ddad462fa1d",
                'primary_manager_id': None,
                'employee_status': {
                    'hire_date': '2022-06-13 00:00:00-07:00',
                    'is_active': False,
                    'is_retired': False,
                    'is_terminated': True,
                    'retirement_date': None,
                    'status': 'Terminated',
                    'termination_date': '2022-07-15 00:00:00-07:00',
                },
                'active_positions': [],
            }
        )
        self.assertIsNotNone(str(work_position))

    def test_worker(self):
        worker = Person(netid='none',
                        regid="10000000",
                        employee_id="100000115")
        self.assertIsNotNone(worker)

        data = {
            "Name": "Bill Faculty",
            "EmployeeID": "000000005",
            "RegID": "10000000000000000000000000000005",
            "IDs": [
                {
                    "Type": "NetID",
                    "Value": "bill"
                },
                {
                    "Type": "StudentID",
                    "Value": "1000005"
                },
                {
                    "Type": "PriorRegID",
                    "Value": "10000000000000000000000000000001"
                }
            ],
            "WorkerDetails": [
                {
                    "WID": "1b68136df25201c0710e3ddad462fa1d",
                    "EmploymentStatus": {
                        "HireDate": "2021-11-12T00:00:00-08:00",
                        "OriginalHireDate": "2021-11-12T00:00:00-08:00",
                        "ExpectedFixedTermEndDate": None,
                        "FirstDayOfWork": "2021-11-12T00:00:00-08:00",
                        "ActiveStatusDate": "2021-11-12T00:00:00-08:00",
                        "Active": True,
                        "EmployeeStatus": "Active",
                        "Terminated": False,
                        "TerminationDate": None,
                        "TerminationInvoluntary": None,
                        "TerminationReason": None,
                        "Retired": False,
                        "RetirementDate": None,
                        "RetirementApplicationDate": None,
                        "DisplayLeave": False,
                        "LeaveStatusDetails": []
                    },
                    "EmploymentDetails": [],
                    "OrganizationDetails": [],
                    "ActiveAppointment": True,
                }
            ]
        }
        worker = Person(data=data)
        self.maxDiff = None
        self.assertEqual(
            worker.to_json(),
            {
                'employee_id': '000000005',
                'is_active': True,
                'netid': 'bill',
                'primary_manager_id': None,
                'regid': '10000000000000000000000000000005',
                'student_id': '1000005',
                'worker_details': [
                    {
                        'active_positions': [],
                        'employee_status': {'hire_date': 
                                                '2021-11-12 00:00:00-08:00',
                                            'is_active': True,
                                            'is_retired': False,
                                            'is_terminated': False,
                                            'retirement_date': None,
                                            'status': 'Active',
                                            'termination_date': None},
                        'primary_manager_id': None,
                        'worker_wid': '1b68136df25201c0710e3ddad462fa1d'
                    }
                ]
            })
        self.assertIsNotNone(str(worker))
