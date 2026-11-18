import time
import threading
from datetime import datetime, timedelta


class Alarm:
    def __init__(self, alarm_id, alarm_time, label=""):
        self.id = alarm_id
        self.time = alarm_time
        self.label = label
        self.enabled = True
        self.triggered_date = None

    def __str__(self):
        status = "Enabled" if self.enabled else "Disabled"
        label = self.label or "-"
        return f"{self.id:<5} {self.time.strftime('%I:%M %p'):<10} {status:<10} {label}"


class AlarmClock:
    def __init__(self):
        self.alarms = []
        self.next_id = 1
        self.running = True
        self.lock = threading.Lock()

    def add_alarm(self, alarm_time, label=""):
        with self.lock:
            alarm = Alarm(self.next_id, alarm_time, label)
            self.alarms.append(alarm)
            self.next_id += 1

        print(f"\nAlarm created successfully.")
        print(f"ID: {alarm.id}")
        print(f"Time: {alarm.time.strftime('%I:%M %p')}")
        if label:
            print(f"Label: {label}")

    def list_alarms(self):
        with self.lock:
            if not self.alarms:
                print("\nNo alarms configured.")
                return

            print("\n" + "=" * 55)
            print(f"{'ID':<5} {'Time':<10} {'Status':<10} Label")
            print("-" * 55)

            for alarm in self.alarms:
                print(alarm)

            print("=" * 55)

    def find_alarm(self, alarm_id):
        with self.lock:
            for alarm in self.alarms:
                if alarm.id == alarm_id:
                    return alarm
        return None

    def enable_alarm(self, alarm_id):
        alarm = self.find_alarm(alarm_id)

        if not alarm:
            print("\nAlarm not found.")
            return

        alarm.enabled = True
        print(f"\nAlarm {alarm_id} enabled.")

    def disable_alarm(self, alarm_id):
        alarm = self.find_alarm(alarm_id)

        if not alarm:
            print("\nAlarm not found.")
            return

        alarm.enabled = False
        print(f"\nAlarm {alarm_id} disabled.")

    def delete_alarm(self, alarm_id):
        with self.lock:
            for index, alarm in enumerate(self.alarms):
                if alarm.id == alarm_id:
                    self.alarms.pop(index)
                    print(f"\nAlarm {alarm_id} deleted.")
                    return

        print("\nAlarm not found.")

    def snooze_alarm(self, alarm):
        new_time = datetime.now() + timedelta(minutes=5)

        alarm.time = new_time
        alarm.triggered_date = None
        alarm.enabled = True

        print(
            f"\nAlarm snoozed until "
            f"{new_time.strftime('%I:%M:%S %p')}"
        )

    def dismiss_alarm(self, alarm):
        alarm.triggered_date = datetime.now().date()
        print("\nAlarm dismissed.")

    def ring_alarm(self, alarm):
        print("\n")
        print("=" * 50)
        print("              ALARM RINGING!")
        print("=" * 50)
        print(
            f"\nTime: {datetime.now().strftime('%I:%M:%S %p')}"
        )

        if alarm.label:
            print(f"Label: {alarm.label}")

        print("\n[S] Snooze for 5 minutes")
        print("[D] Dismiss")

        # Continue beeping until user responds
        while self.running:
            print("\a", end="", flush=True)

            choice = input("\nChoose an option: ").strip().lower()

            if choice == "s":
                self.snooze_alarm(alarm)
                break

            elif choice == "d":
                self.dismiss_alarm(alarm)
                break

            else:
                print("Invalid option. Enter S or D.")

    def monitor(self):
        while self.running:
            now = datetime.now()

            with self.lock:
                alarms_copy = list(self.alarms)

            for alarm in alarms_copy:
                if not alarm.enabled:
                    continue

                # Normal daily alarm
                if (
                    now.hour == alarm.time.hour
                    and now.minute == alarm.time.minute
                ):
                    if alarm.triggered_date != now.date():
                        alarm.triggered_date = now.date()

                        # Ring outside the monitor loop
                        threading.Thread(
                            target=self.ring_alarm,
                            args=(alarm,),
                            daemon=True
                        ).start()

            time.sleep(1)

    def stop(self):
        self.running = False


def parse_time(value):
    formats = [
        "%I:%M %p",
        "%I:%M%p",
        "%H:%M",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(value.upper(), fmt)

            now = datetime.now()

            return datetime(
                now.year,
                now.month,
                now.day,
                parsed.hour,
                parsed.minute
            )

        except ValueError:
            continue

    return None


def get_alarm_time():
    while True:
        value = input(
            "\nEnter alarm time "
            "(e.g. 07:30 AM or 19:30): "
        ).strip()

        alarm_time = parse_time(value)

        if alarm_time:
            return alarm_time

        print(
            "Invalid time format.\n"
            "Examples: 07:30 AM, 7:30 PM, 19:30"
        )


def get_alarm_id():
    value = input("Enter alarm ID: ").strip()

    try:
        return int(value)
    except ValueError:
        print("Invalid alarm ID.")
        return None


def show_menu(clock):
    print("\n")
    print("=" * 50)
    print("             PYTHON ALARM CLOCK")
    print("=" * 50)

    print(
        f"Current Time: "
        f"{datetime.now().strftime('%I:%M:%S %p')}"
    )

    print("=" * 50)
    print("1. Set Alarm")
    print("2. List Alarms")
    print("3. Enable Alarm")
    print("4. Disable Alarm")
    print("5. Delete Alarm")
    print("6. Exit")
    print("=" * 50)


def main():
    clock = AlarmClock()

    monitor_thread = threading.Thread(
        target=clock.monitor,
        daemon=True
    )

    monitor_thread.start()

    try:
        while clock.running:
            show_menu(clock)

            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                alarm_time = get_alarm_time()

                label = input(
                    "Enter label (optional): "
                ).strip()

                clock.add_alarm(
                    alarm_time,
                    label
                )

            elif choice == "2":
                clock.list_alarms()

            elif choice == "3":
                alarm_id = get_alarm_id()

                if alarm_id is not None:
                    clock.enable_alarm(alarm_id)

            elif choice == "4":
                alarm_id = get_alarm_id()

                if alarm_id is not None:
                    clock.disable_alarm(alarm_id)

            elif choice == "5":
                alarm_id = get_alarm_id()

                if alarm_id is not None:
                    clock.delete_alarm(alarm_id)

            elif choice == "6":
                clock.stop()
                print("\nGoodbye!")
                break

            else:
                print("\nInvalid option. Please choose 1-6.")

    except KeyboardInterrupt:
        clock.stop()
        print("\n\nAlarm clock stopped. Goodbye!")

    except EOFError:
        clock.stop()
        print("\n\nAlarm clock stopped. Goodbye!")


if __name__ == "__main__":
    main()