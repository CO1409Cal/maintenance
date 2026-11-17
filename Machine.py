from pydantic import BaseModel
import datetime


class Machine(BaseModel):
   name: str
   online: bool
   uptime: float
   maintenanceAlerts: str
   maintenanceLog: dict[str,dict[str,datetime.datetime]]
