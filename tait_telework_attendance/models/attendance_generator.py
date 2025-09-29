import random
from datetime import datetime, timedelta


class AttendanceGenerator:
    """
    Helper class to separate attendance generation logic
    from the employee model.
    """

    def __init__(self, employee, calendar, start_date, end_date, attendance_rate):
        self.employee = employee
        self.calendar = calendar
        self.start_date = start_date
        self.end_date = end_date
        self.attendance_rate = attendance_rate

    def collect_work_days(self, public_holidays, leaves):
        """
        Collect all possible working days with their schedule (hour_from, hour_to).
        Excludes public holidays and validated leaves.
        """
        work_days = []
        current = self.start_date
        while current <= self.end_date:
            if any(ph.date_from.date() <= current <= ph.date_to.date() for ph in public_holidays):
                current += timedelta(days=1)
                continue

            if any(l.request_date_from <= current <= l.request_date_to for l in leaves):
                current += timedelta(days=1)
                continue

            day_attendances = self.calendar.attendance_ids.filtered(
                lambda a: int(a.dayofweek) == current.weekday()
            )
            if day_attendances:
                work_days.append((current, day_attendances))
            current += timedelta(days=1)
        return work_days

    def select_present_days(self, work_days):
        """
        Select the days the employee will attend based on attendance_rate.
        """
        total_work_days = len(work_days)
        required_days = int(total_work_days * self.attendance_rate)
        present_days = set(random.sample(work_days, required_days)) if required_days else set()
        return present_days, total_work_days, required_days

    def generate_day_attendance(self, day, att, late_multiplier, early_leave_multiplier):
        """
        Generate check_in/check_out for a single day with probabilities
        for late arrival, early leave, and partial shifts.
        """
        check_in_time = datetime.combine(day, datetime.min.time()) + timedelta(hours=att.hour_from)
        check_out_time = datetime.combine(day, datetime.min.time()) + timedelta(hours=att.hour_to)

        # Employee cannot arrive before official start → only late arrival
        if random.random() < (0.3 * late_multiplier):
            check_in_time += timedelta(minutes=random.randint(5, 60))

        # Employee cannot leave after official end → only early leave
        if random.random() < (0.3 * early_leave_multiplier):
            check_out_time -= timedelta(minutes=random.randint(5, 60))

        # Chance for partial working day
        if random.random() < 0.2:
            partial_hours = random.choice([3, 4, 5])
            check_out_time = check_in_time + timedelta(hours=partial_hours)
            official_end = datetime.combine(day, datetime.min.time()) + timedelta(hours=att.hour_to)
            if check_out_time > official_end:
                check_out_time = official_end

        return check_in_time, check_out_time if check_out_time > check_in_time else (None, None)
