from unittest import TestCase
from uw_hrp.worker import (
    get_worker_by_netid, get_worker_by_employee_id, get_worker_by_regid)
from restclients_core.exceptions import DataFailureException
from uw_hrp.util import fdao_hrp_override


@fdao_hrp_override
class WorkerTest(TestCase):

    def test_get_worker_by_netid(self):
        worker = get_worker_by_netid("faculty")
        self.assertEqual(worker.netid, "faculty")
        self.assertEqual(worker.regid,
                         "10000000000000000000000000000005")
        self.assertEqual(worker.employee_id, "000000005")
        self.assertEqual(worker.employee_status, "Active")
        self.assertTrue(worker.is_active)
        self.assertFalse(worker.is_retired)
        self.assertFalse(worker.is_terminated)

        self.assertEqual(len(worker.worker_active_positions), 1)
        work_position = worker.worker_active_positions[0]
        self.assertEqual(work_position.org_code, '3040111000')
        self.assertEqual(work_position.org_desc, "FAMILY MEDICINE")
        self.assertEqual(work_position.ecs_job_cla_code_desc,
                         "Academic Personnel")
        self.assertEqual(str(work_position.effective_date),
                         "2012-07-01 07:00:00+00:00")
        self.assertIsNone(work_position.end_date)
        self.assertEqual(work_position.busi_title,
                         "Clinical Associate Professor")
        self.assertEqual(work_position.pos_type, "Unpaid_Academic")
        self.assertEqual(work_position.supervisor_eid, "100000015")
        self.assertEqual(work_position.pos_time_type_id, "Part_time")
        self.assertEqual(work_position.supervisory_org_code, "SOM")
        self.assertEqual(work_position.supervisory_org_id, "SOM_000420")
        self.assertEqual(work_position.supervisory_org_desc,
                         "SOM: Family Medicine: Volunteer (Visor, Super1)")
        self.assertEqual(work_position.location, "Seattle Campus")
        self.assertTrue(work_position.is_primary)

    def test_get_worker_by_employee_id(self):
        worker = get_worker_by_employee_id("100000015")
        self.assertTrue(worker.netid, 'chair')

    def test_get_worker_by_regid(self):
        worker = get_worker_by_regid("10000000000000000000000000000015")
        self.assertTrue(worker.netid, 'chair')

    def test_invalid_user(self):
        self.assertRaises(DataFailureException,
                          get_worker_by_regid,
                          "00000000000000000000000000000001")

        self.assertRaises(DataFailureException,
                          get_worker_by_employee_id, "100000000")
