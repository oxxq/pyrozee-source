from pyrogram import raw
from .auto_name import AutoName


class BusinessSchedule(AutoName):

    ALWAYS = raw.types.BusinessAwayMessageScheduleAlways
    OUTSIDE_WORK_HOURS = raw.types.BusinessAwayMessageScheduleOutsideWorkHours
    CUSTOM = raw.types.BusinessAwayMessageScheduleCustom
