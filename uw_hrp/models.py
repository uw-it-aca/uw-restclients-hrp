# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime, timezone
from dateutil.parser import parse
import json
from restclients_core import models


def get_now():
    # return time-zone-aware datetime
    return datetime.now(timezone.utc)


def is_future_end_date(end_date):
    return end_date is None or end_date > get_now()


def date_to_str(d_obj):
    if d_obj is not None:
        return str(d_obj)
    return None


def parse_date(date_str):
    if date_str is not None:
        return parse(date_str)
    return None


class EmploymentStatus(models.Model):
    status = models.CharField(max_length=32)
    is_active = models.BooleanField(default=False)
    is_retired = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)
    hire_date = models.DateTimeField(null=True, default=None)
    retirement_date = models.DateTimeField(null=True, default=None)
    termination_date = models.DateTimeField(null=True, default=None)

    def to_json(self):
        return {
                'hire_date': date_to_str(self.hire_date),
                'is_active': self.is_active,
                'is_retired': self.is_retired,
                'is_terminated': self.is_terminated,
                'retirement_date': date_to_str(self.retirement_date),
                'status': self.status,
                'termination_date': date_to_str(self.termination_date)}

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(EmploymentStatus, self).__init__(*args, **kwargs)

        self.status = data.get("EmployeeStatus")
        self.is_active = data.get("Active")
        self.is_retired = data.get("Retired")
        self.is_terminated = data.get("Terminated")
        self.hire_date = parse_date(data.get("HireDate"))
        self.retirement_date = parse_date(data.get("RetirementDate"))
        self.termination_date = parse_date(data.get("TerminationDate"))

    def __str__(self):
        return json.dumps(self.to_json())


class JobProfile(models.Model):
    job_code = models.CharField(max_length=16, null=True, default=None)
    description = models.CharField(max_length=96, null=True, default=None)

    def to_json(self):
        return {'job_code': self.job_code,
                'description': self.description}

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(JobProfile, self).__init__(*args, **kwargs)

        self.description = data.get("Name")
        ids = data.get("IDs")
        if ids  is not None and len(ids):
            for id_data in ids:
                if id_data.get("Type") == "Job_Profile_ID":
                    self.job_code = id_data.get("Value")

    def __str__(self):
        return json.dumps(self.to_json())


class SupervisoryOrganization(models.Model):
    # budget_code = models.CharField(max_length=16, null=True, default=None)
    org_code = models.CharField(max_length=16, null=True, default=None)
    org_name = models.CharField(max_length=128, null=True, default=None)

    def to_json(self):
        return {'budget_code': self.budget_code,
                'org_code': self.org_code,
                'org_name': self.org_name}

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(SupervisoryOrganization, self).__init__(*args,
                                                                 **kwargs)
        name_data = data.get("Name").strip()
        if ": " in name_data:
            name_data = name_data.split(": ", 1)
            self.org_code = name_data[0].strip()
            if " (" in name_data[1]:
                org_name = name_data[1].strip().split(" (", 1)
                self.org_name = org_name[0]

    def __str__(self):
        return json.dumps(self.to_json())


class EmploymentDetails(models.Model):
    start_date = models.DateTimeField(null=True, default=None)
    end_date = models.DateTimeField(null=True, default=None)
    job_class = models.CharField(max_length=96, null=True, default=None)
    fte_percent = models.FloatField(null=True, blank=True, default=None)
    is_primary = models.BooleanField(default=False)
    location = models.CharField(max_length=96, null=True, default=None)
    org_unit_code = models.CharField(max_length=8,
                                     null=True, default=None)
    pos_type = models.CharField(max_length=64, null=True, default=None)
    supervisor_eid = models.CharField(max_length=16,
                                      null=True, default=None)
    title = models.CharField(max_length=128, null=True, default=None)

    def is_active_position(self):
        return is_future_end_date(self.end_date)

    def to_json(self):
        data = {
                'start_date': date_to_str(self.start_date),
                'end_date': date_to_str(self.end_date),
                'job_class': self.job_class,
                'fte_percent': self.fte_percent,
                'is_primary': self.is_primary,
                'location': self.location,
                'org_unit_code': self.org_unit_code,
                'pos_type': self.pos_type,
                'supervisor_eid': self.supervisor_eid,
                'title': self.title,
                'job_profile': None,
                'supervisory_org': None
                }
        if self.job_profile is not None:
            data['job_profile'] = self.job_profile.to_json()
        if self.supervisory_org is not None:
            data['supervisory_org'] = self.supervisory_org.to_json()
        return data

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        self.job_profile = None
        self.supervisory_org = None
        if data is None:
            return super(EmploymentDetails, self).__init__(*args, **kwargs)

        self.job_profile = JobProfile(
            data=data.get("JobProfile"))

        self.supervisory_org = SupervisoryOrganization(
            data=data.get("SupervisoryOrganization"))

        if data.get("JobClassificationSummaries"):
            for jc_data in data["JobClassificationSummaries"]:
                if jc_data.get("JobClassification"):
                    jobc = jc_data["JobClassification"].get("Name")
                    if " - " in jobc:
                        name_data = jobc.split(" - ", 1)
                        if len(name_data[1]) > 0:
                            self.job_class = name_data[1].strip()
                            if " (" in self.job_class:
                                self.job_class = self.job_class.split(" (", 1)[0]

        self.title = data.get("BusinessTitle")
        self.fte_percent = float(data.get("FTEPercent"))
        self.is_primary = data.get("PrimaryPosition")

        if data.get("Location") is not None:
            self.location = data["Location"].get("Name")

        if data.get("OrganizationDetails") is not None:
            org = data["OrganizationDetails"].get("Organization")
            if org is not None:
                self.org_unit_code = org.get("Name")

        if data.get("PositionWorkerType") is not None:
            self.pos_type = data["PositionWorkerType"].get("Name")

        self.start_date = parse_date(data.get("StartDate"))
        self.end_date = parse_date(data.get("PositionVacateDate"))

        if data.get("Managers") is not None:
            ids = data["Managers"].get("IDs")
            for id_data in ids:
                if id_data.get("Type") == "Employee_ID":
                    self.supervisor_eid = id_data.get("Value")


class WorkerDetails(models.Model):
    worker_wid = models.CharField(max_length=32)
    is_active = models.BooleanField(default=False)
    primary_manager_id = models.CharField(
        max_length=16, null=True, default=None)

    def to_json(self):
        data = {'worker_wid': self.worker_wid,
                'employee_status': None,
                'primary_manager_id': self.primary_manager_id}

        if self.employee_status is not None:
            data['employee_status'] = self.employee_status.to_json()

        positions = []
        if self.primary_position is not None:
            positions.append(self.primary_position.to_json())
        for pos in self.other_active_positions:
            positions.append(pos.to_json())
        data['active_positions'] = positions
        return data

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        self.employee_status = None
        self.primary_position = None  # only 1 primary position
        self.other_active_positions = []  # include the future position

        if data is None:
            return super(WorkerDetails, self).__init__(*args, **kwargs)

        self.worker_wid = data.get("WID")

        self.employee_status = EmploymentStatus(
            data=data.get("EmploymentStatus"))

        if not (self.employee_status and self.employee_status.is_active):
            return

        emp_details = data.get("EmploymentDetails")
        if emp_details is not None and len(emp_details) > 0:
            for emp_detail in emp_details:
                position = EmploymentDetails(data=emp_detail)
                if position and position.is_primary:
                    self.primary_manager_id = position.supervisor_eid
                    self.primary_position = position
                else:
                    self.other_active_positions.append(position)


class Person(models.Model):
    netid = models.CharField(max_length=32)
    regid = models.CharField(max_length=32)
    employee_id = models.CharField(max_length=16)
    student_id = models.CharField(
        max_length=16, null=True, default=None)
    is_active = models.BooleanField(default=False)
    primary_manager_id = models.CharField(
        max_length=16, null=True, default=None)

    def to_json(self):
        data = {
                "netid": self.netid,
                'regid': self.regid,
                'employee_id': self.employee_id,
                'student_id': self.student_id,
                'is_active': self.is_active,
                'primary_manager_id': self.primary_manager_id
                }
        workers = []
        for worker_detail in self.worker_details:
            workers.append(worker_detail.to_json())
        data['worker_details'] = workers
        return data

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        self.worker_details = []
        if data is None:
            return super(Person, self).__init__(*args, **kwargs)

        self.employee_id = data.get("EmployeeID")
        self.regid = id.get("RegID")

        for id in data.get("IDs"):
            if id.get("Type") == "NetID":
                self.netid = id.get("Value")
            if id.get("Type") == "StudentID":
                self.student_id = id.get("Value")

        if "WorkerDetails" in data:
            wk_detail_list = data["WorkerDetails"]
            for wk_detail in wk_detail_list:
                if wk_detail.get("ActiveAppointment") is False:
                    continue

                worker_obj = WorkerDetails(data=wk_detail)
                if (worker_obj and worker_obj.employee_status and
                        worker_obj.employee_status.is_active):
                    self.is_active = True
                    self.worker_details.append(worker_obj)
                if worker_obj.primary_manager_id is not None:
                    self.primary_manager_id = worker_obj.primary_manager_id
