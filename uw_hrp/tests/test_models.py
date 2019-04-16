from unittest import TestCase
from uw_hrp import parse_date
from uw_hrp.models import Worker, WorkerPosition
from uw_hrp.util import fdao_hrp_override


@fdao_hrp_override
class WorkerTest(TestCase):

    def test_parse_date(self):
        self.assertIsNotNone(parse_date("2017-09-16T07:00:00.000Z"))

    def test_workerposition(self):
        data = {
            "CostCenter":
                {"Description": "INFORMATION SCHOOL",
                 "ID": "061630",
                 "OrganizationCode": "2670001000",
                 "OrganizationDescription": "THE INFORMATION SCHOOL"},
            "EcsJobClassificationCodeDescription": "Undergraduate Student",
            "IsPrimaryPosition": True,
            "Location":
                {"ID": "Seattle Campus",
                 "Name": "Seattle Campus"},
            "PositionBusinessTitle": "Reader/Grader",
            "PositionEffectiveDate": "2017-09-16T07:00:00.000Z",
            "PositionEndDate": "2018-06-15T00:00:00.000Z",
            "PositionSupervisor":
                {"EmployeeID": "000000005",
                 "Href": "/hrp/v2/worker/000000005.json"},
            "PositionTimeTypeID": "Part_time",
            "PositionTitle": "Reader/Grader",
            "PositionType": "Temporary",
            "SupervisoryOrganization": None,
            "WorkShift": "First Shift"
            }
        work_position = WorkerPosition(data=data)
        self.assertEqual(
            work_position.json_data(),
            {'busi_title': 'Reader/Grader',
             'ecs_job_cla_code_desc': 'Undergraduate Student',
             'effective_date': '2017-09-16 07:00:00+00:00',
             'end_date': '2018-06-15 00:00:00+00:00',
             'is_primary': True,
             'location': 'Seattle Campus',
             'org_code': '2670001000',
             'org_desc': 'THE INFORMATION SCHOOL',
             'pos_time_type_id': 'Part_time',
             'pos_type': 'Temporary',
             'supervisor_eid': '000000005',
             'supervisory_org_code': None,
             'supervisory_org_desc': None,
             'supervisory_org_id': None})
        self.assertIsNotNone(str(work_position))

    def test_worker(self):
        data = {
            "NetID": "dean",
            "RegID": "10000000000000000000000000000115",
            "EmployeeID": "100000115",
            "WorkerEmploymentStatus":
                {"ActiveStatusDate": "1980-07-01T07:00:00.000Z",
                 "EmployeeStatus": "Active",
                 "EmployeeStatusCode": "A",
                 "EndEmploymentDate": None,
                 "EstimatedLastDayOfLeave": None,
                 "FirstDayOfLeave": None,
                 "FirstDayOfWork": "1980-07-01T07:00:00.000Z",
                 "HireDate": "1980-07-01T07:00:00.000Z",
                 "IsActive": True,
                 "IsRetired": False,
                 "IsTerminated": False,
                 "LastDayOfWorkForLeave": None,
                 "OriginalHireDate": "1980-07-01T07:00:00.000Z",
                 "RetirementDate": None,
                 "TerminationDate": None},
            "WorkerPositions": [
                {"CostCenter":
                 {"Description": "SOM ADMINISTRATION",
                  "ID": "652791",
                  "OrganizationCode": "3040501060",
                  "OrganizationDescription": "EXEC MGMT OEVP ADMIN"},
                 "EcsJobClassificationCode": "F",
                 "EcsJobClassificationCodeDescription": "Academic Personnel",
                 "IsPrimaryPosition": True,
                 "Location":
                     {"ID": "Seattle Campus",
                      "Name": "Seattle Campus"},
                 "PositionBusinessTitle":
                     "CEO, UW Medicine and Dean of the School of Medicine",
                 "PositionEffectiveDate": "1999-06-13T07:00:00.000Z",
                 "PositionEndDate": None,
                 "PositionSupervisor":
                     {"EmployeeID": "100001115"},
                 "WorkShift": "First Shift"}]}
        worker = Worker(data=data)
        self.assertEqual(
            worker.json_data(),
            {'netid': 'dean',
             'regid': "10000000000000000000000000000115",
             'employee_id': '100000115',
             'employee_status': 'Active',
             'is_active': True,
             'is_retired': False,
             'is_terminated': False,
             'worker_positions': [
                 {'effective_date': '1999-06-13 07:00:00+00:00',
                  'end_date': None,
                  'is_primary': True,
                  'busi_title':
                      'CEO, UW Medicine and Dean of the School of Medicine',
                  'pos_type': None,
                  'ecs_job_cla_code_desc': 'Academic Personnel',
                  'location': 'Seattle Campus',
                  'org_code': '3040501060',
                  'org_desc': 'EXEC MGMT OEVP ADMIN',
                  'pos_time_type_id': None,
                  'supervisor_eid': '100001115',
                  'supervisory_org_code': None,
                  'supervisory_org_id': None,
                  'supervisory_org_desc': None}
                 ]})
        self.assertIsNotNone(str(worker))
