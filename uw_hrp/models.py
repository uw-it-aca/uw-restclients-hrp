from datetime import datetime, timezone
from dateutil.parser import parse
import json
from restclients_core import models


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
    status_code = models.CharField(max_length=8)
    is_active = models.BooleanField(default=False)
    is_retired = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)
    hire_date = models.DateTimeField(null=True, default=None)
    end_emp_date = models.DateTimeField(null=True, default=None)
    retirement_date = models.DateTimeField(null=True, default=None)
    termination_date = models.DateTimeField(null=True, default=None)

    def to_json(self):
        return {'end_emp_date': date_to_str(self.end_emp_date),
                'hire_date': date_to_str(self.hire_date),
                'is_active': self.is_active,
                'is_retired': self.is_retired,
                'is_terminated': self.is_terminated,
                'retirement_date': date_to_str(self.retirement_date),
                'status': self.status,
                'status_code': self.status_code,
                'termination_date': date_to_str(self.termination_date)}

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        self.status = data.get("EmployeeStatus")
        self.status_code = data.get("EmployeeStatusCode")
        if data.get("EndEmploymentDate") is not None:
            self.end_emp_date = parse_date(data["EndEmploymentDate"])
        self.is_active = data.get("IsActive")
        self.is_retired = data.get("IsRetired")
        self.is_terminated = data.get("IsTerminated")
        if data.get("HireDate") is not None:
            self.hire_date = parse_date(data["HireDate"])
        if data.get("RetirementDate") is not None:
            self.retirement_date = parse_date(data["RetirementDate"])
        if data.get("TerminationDate") is not None:
            self.termination_date = parse_date(data["TerminationDate"])

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
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        self.job_code = data.get("JobProfileID")
        self.description = data.get("JobProfileDescription")

    def __str__(self):
        return json.dumps(self.to_json())


class SupervisoryOrganization(models.Model):
    budget_code = models.CharField(max_length=16, null=True, default=None)
    org_code = models.CharField(max_length=16, null=True, default=None)
    org_name = models.CharField(max_length=128, null=True, default=None)

    def to_json(self):
        return {'budget_code': self.budget_code,
                'org_code': self.org_code,
                'org_name': self.org_name}

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        if data.get("CostCenter") is not None:
            self.budget_code = data["CostCenter"].get("OrganizationCode")
        self.org_code = data.get("Code")
        self.org_name = data.get("Name")

    def __str__(self):
        return json.dumps(self.to_json())


class WorkerPosition(models.Model):
    start_date = models.DateTimeField(null=True, default=None)
    end_date = models.DateTimeField(null=True, default=None)
    ecs_job_cla_code_desc = models.CharField(max_length=96,
                                             null=True, default=None)
    is_primary = models.BooleanField(default=False)
    location = models.CharField(max_length=96, null=True, default=None)
    pos_type = models.CharField(max_length=64, null=True, default=None)
    pos_time_type_id = models.CharField(max_length=64,
                                        null=True, default=None)
    fte_percent = models.FloatField(null=True, blank=True, default=None)
    supervisor_eid = models.CharField(max_length=16,
                                      null=True, default=None)
    title = models.CharField(max_length=128, null=True, default=None)

    def is_active_position(self):
        now = datetime.now(timezone.utc)
        return self.end_date is None or self.end_date > now

    def to_json(self):
        return {
            'start_date': date_to_str(self.start_date),
            'end_date': date_to_str(self.end_date),
            'ecs_job_cla_code_desc': self.ecs_job_cla_code_desc,
            'fte_percent': self.fte_percent,
            'is_primary': self.is_primary,
            'location': self.location,
            'pos_type': self.pos_type,
            'pos_time_type_id': self.pos_time_type_id,
            'title': self.title,
            'supervisor_eid': self.supervisor_eid,
            'job_profile': self.job_profile.to_json(),
            'supervisory_org': self.supervisory_org.to_json(),
            }

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        self.ecs_job_cla_code_desc = \
            data.get("EcsJobClassificationCodeDescription")
        self.is_primary = data.get("IsPrimaryPosition")
        if data.get("Location") is not None:
            self.location = data["Location"]["ID"]
        self.title = data.get("PositionBusinessTitle")
        self.pos_type = data.get("PositionType")
        self.pos_time_type_id = data.get("PositionTimeTypeID")
        self.fte_percent = float(data.get("PositionFTEPercent"))
        if data.get("PositionStartDate") is not None:
            self.start_date = parse_date(data["PositionStartDate"])

        if data.get("PositionEndDate") is not None:
            self.end_date = parse_date(data["PositionEndDate"])

        if data.get("PositionSupervisor") is not None:
            self.supervisor_eid = data["PositionSupervisor"]["EmployeeID"]

        if data.get("SupervisoryOrganization") is not None:
            self.supervisory_org = SupervisoryOrganization(
                data=data["SupervisoryOrganization"])
        else:
            self.supervisory_org = SupervisoryOrganization()

        if data.get("JobProfileSummary") is not None:
            self.job_profile = JobProfile(data=data["JobProfileSummary"])
        else:
            self.job_profile = JobProfile()


class Worker(models.Model):
    netid = models.CharField(max_length=32)
    regid = models.CharField(max_length=32)
    employee_id = models.CharField(max_length=16)
    primary_manager_id = models.CharField(max_length=16)

    def to_json(self):
        positions = []
        for pos in self.worker_active_positions:
            positions.append(pos.to_json())

        return {
            "netid": self.netid,
            'regid': self.regid,
            'employee_id': self.employee_id,
            'employee_status': self.employee_status.to_json(),
            'primary_manager_id': self.primary_manager_id,
            'worker_active_positions': positions
            }

    def __str__(self):
        return json.dumps(self.to_json())

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        self.netid = data.get("NetID")
        self.regid = data.get("RegID")
        self.employee_id = data.get("EmployeeID")

        self.employee_status = EmploymentStatus(
            data=data.get("WorkerEmploymentStatus"))

        self.worker_active_positions = []
        if (self.employee_status.is_active and
                data.get("WorkerPositions") is not None):
            for position in data["WorkerPositions"]:
                position = WorkerPosition(data=position)
                if position.is_active_position():
                    self.worker_active_positions.append(position)
                    if position.is_primary:
                        self.primary_manager_id = position.supervisor_eid
