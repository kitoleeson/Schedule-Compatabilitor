class Schedule:
    def __init__(self, name):
        self.name = name
        self.time_slots = []
        self.days = []

    def add_class(self, subject, start_time, end_time):
        self.time_slots.append(TimeSlot(start_time, end_time))

class TimeSlot:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def overlaps(self, other):
        return max(self.start, other.start) < min(self.end, other.end)

def main():
    db = ScheduleDatabase()

    # Load existing schedules or create new ones
    schedules = {}
    while True:
        print("1. Add new schedule")
        print("2. Load existing schedule")
        choice = input("Enter your choice (1/2): ")
        if choice == '1':
            name = input("Enter schedule name: ")
            schedule = Schedule(name)
            num_days = int(input("Enter number of days: "))
            for _ in range(num_days):
                num_classes = int(input(f"Enter number of classes for day {_:+d}: "))
                for _ in range(num_classes):
                    subject = input("Enter class subject: ")
                    start_time = int(input("Enter start time (minutes since midnight): "))
                    end_time = int(input("Enter end time (minutes since midnight): "))
                    schedule.add_class(subject, start_time, end_time)
            db.save(name, schedule)
        elif choice == '2':
            name = input("Enter schedule name: ")
            schedules[name] = Schedule(name)
            loaded_schedule = db.load(name)
            if loaded_schedule:
                schedules[name].time_slots = [
                    TimeSlot(slot['start'], slot['end'])
                    for slot in loaded_schedule['time_slots']
                ]
                schedules[name].days = [
                    Day(slot['start'], slot['end'])
                    for slot in loaded_schedule['days']
                ]
        else:
            break

    # Find overlapping schedules
    overlaps = {}
    for name1, schedule1 in schedules.items():
        for name2, schedule2 in schedules.items():
            if name1 != name2:
                overlaps[(name1, name2)] = find_overlapping_slots(schedule1, schedule2)

    # Calculate free time
    free_times = {name: calculate_free_time(schedule) for name, schedule in schedules.items()}

    # Visualize schedules
    visualize_schedules(schedules.values())

    print("Overlapping time slots:")
    for (name1, name2), overlaps_list in overlaps.items():
        print(f"{name1} and {name2}:")
        for slot1, slot2 in overlaps_list:
            print(f"  - {slot1.start}-{slot1.end} ({slot1.subject}) vs {slot2.start}-{slot2.end} ({slot2.subject})")

    # Display free time
    for name, times in free_times.items():
        print(f"\nFree time for {name}:")
        for time in times:
            print(f"  - {time // 60}:{time % 60:02d}")

if __name__ == "__main__":
    main()
