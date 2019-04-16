import json
from uw_hrp import parse_date
from restclients_core import models


def date_to_str(d_obj):
    if d_obj is not None:
        return str(d_obj)
    return None


class WorkerPosition(models.Model):
    effective_date = models.DateTimeField(null=True, default=None)
    end_date = models.DateTimeField(null=True, default=None)
    ecs_job_cla_code_desc = models.CharField(max_length=64,
                                             null=True, default=None)
    location = models.CharField(max_length=96, null=True, default=None)
    is_primary = models.BooleanField(default=False)
    org_code = models.CharField(max_length=16, null=True, default=None)
    org_desc = models.CharField(max_length=128, null=True, default=None)
    busi_title = models.CharField(max_length=128, null=True, default=None)
    pos_type = models.CharField(max_length=64, null=True, default=None)
    supervisor_eid = models.CharField(max_length=16,
                                      null=True, default=None)
    pos_time_type_id = models.CharField(max_length=64,
                                        null=True, default=None)
    supervisory_org_code = models.CharField(max_length=32,
                                            null=True, default=None)
    supervisory_org_id = models.CharField(max_length=96,
                                          null=True, default=None)
    supervisory_org_desc = models.CharField(max_length=256,
                                            null=True, default=None)

    def json_data(self):
        return {
            'effective_date': date_to_str(self.effective_date),
            'end_date': date_to_str(self.end_date),
            'is_primary': self.is_primary,
            'busi_title': self.busi_title,
            'pos_type': self.pos_type,
            'ecs_job_cla_code_desc': self.ecs_job_cla_code_desc,
            'location': self.location,
            'org_code': self.org_code,
            'org_desc': self.org_desc,
            'pos_time_type_id': self.pos_time_type_id,
            'supervisor_eid': self.supervisor_eid,
            'supervisory_org_code': self.supervisory_org_code,
            'supervisory_org_id': self.supervisory_org_id,
            'supervisory_org_desc': self.supervisory_org_desc,
            }

    def __str__(self):
        return json.dumps(self.json_data())

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        if data.get("CostCenter") is not None:
            self.org_code = data["CostCenter"]["OrganizationCode"]
            self.org_desc = data["CostCenter"]["OrganizationDescription"]

        self.ecs_job_cla_code_desc = \
            data["EcsJobClassificationCodeDescription"]
        self.is_primary = data["IsPrimaryPosition"]

        if data.get("Location") is not None:
            self.location = data["Location"]["ID"]

        self.busi_title = data["PositionBusinessTitle"]

        if data.get("PositionType") is not None:
            self.pos_type = data["PositionType"]

        if data.get("PositionTimeTypeID") is not None:
            self.pos_time_type_id = data["PositionTimeTypeID"]

        self.effective_date = parse_date(data["PositionEffectiveDate"])
        self.end_date = parse_date(data["PositionEndDate"])

        self.supervisor_eid = data["PositionSupervisor"]["EmployeeID"]

        if data.get("SupervisoryOrganization") is not None:
            self.supervisory_org_code = \
                data["SupervisoryOrganization"]["Code"]
            self.supervisory_org_id = \
                data["SupervisoryOrganization"]["ID"]
            self.supervisory_org_desc = \
                data["SupervisoryOrganization"]["Description"]

    class Meta:
        db_table = 'restclients_hrp_worker_position'


class Worker(models.Model):
    netid = models.CharField(max_length=32,
                             db_index=True,
                             unique=True)
    regid = models.CharField(max_length=32,
                             db_index=True,
                             unique=True)
    employee_id = models.CharField(max_length=16,
                                   db_index=True,
                                   unique=True)
    employee_status = models.CharField(max_length=32)
    is_active = models.BooleanField(default=False)
    is_retired = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)

    def json_data(self):
        positions = []
        for pos in self.worker_positions:
            positions.append(pos.json_data())

        return {
            "netid": self.netid,
            'regid': self.regid,
            'employee_id': self.employee_id,
            'employee_status': self.employee_status,
            'is_active': self.is_active,
            'is_retired': self.is_retired,
            'is_terminated': self.is_terminated,
            'worker_positions': positions
            }

    def __str__(self):
        json_data = self.json_data()
        json_data['worker_positions'] = "[{0}]".format(','.join(
            map(str, self.worker_positions)))
        return json.dumps(json_data)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(WorkerPosition, self).__init__(*args, **kwargs)

        self.netid = data["NetID"]
        self.regid = data["RegID"]
        self.employee_id = data["EmployeeID"]

        if data.get("WorkerEmploymentStatus") is not None:
            self.employee_status = \
                data["WorkerEmploymentStatus"]["EmployeeStatus"]
            self.is_active = data["WorkerEmploymentStatus"]["IsActive"]
            self.is_retired = data["WorkerEmploymentStatus"]["IsRetired"]
            self.is_terminated = data["WorkerEmploymentStatus"]["IsTerminated"]

        self.worker_positions = []
        if data.get("WorkerPositions") is not None:
            for position in data["WorkerPositions"]:
                self.worker_positions.append(WorkerPosition(data=position))

    class Meta:
        db_table = 'restclients_hrp_worker'
