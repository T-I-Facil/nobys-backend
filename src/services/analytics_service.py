from repositories import ScheduleRepository

class AnalyticsService:
    def __init__(self):
        self.schedule_repository = ScheduleRepository()

    def get_analytics(self, user_id: str, start_date: str, end_date: str):
        total_to_invoice = 0
        total_invoiced = 0

        invoiced_schedules = []

        schedules = self.schedule_repository.get_schedules(user_id, start_date, end_date) 
        print(schedules)
        for schedule in schedules:
            if not schedule.invoiced:
                total_to_invoice += schedule.value * schedule.schedule_time
            else:
                value_invoiced = schedule.value * schedule.schedule_time
                total_invoiced += value_invoiced

                invoiced_schedules.append({
                    "start_date": schedule.start_date,
                    "value_invoiced": value_invoiced
                })

        return {
            "total_to_invoice": total_to_invoice,
            "total_invoiced": total_invoiced,
            "invoiced_schedules": invoiced_schedules
        }