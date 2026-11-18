# Python Alarm Clock

A simple alarm clock that runs directly in the terminal. Its able to set multiple alarms, enable or disable them, delete alarms and snooze an alarm when it rings.

The application does not require a database, web server or any external service

## Requirements

* Python 3.8 or later
* Terminal / Command Prompt

No third-party Python packages are required.

## Project Structure

```text
alarm_clock/
├── alarm_clock.py
└── README.md
```

## Running the Application

Open a terminal in the project directory and run :

```bash
python alarm_clock.py
```

On some systems, it may need to use :

```bash
python3 alarm_clock.py
```

The main menu will be displayed :

```text
==================================================
             PYTHON ALARM CLOCK
==================================================
Current Time: 07:25:10 AM
==================================================
1. Set Alarm
2. List Alarms
3. Enable Alarm
4. Disable Alarm
5. Delete Alarm
6. Exit
==================================================

Select an option:
```

## Setting an Alarm

Select `1` and enter the required time.

For example :

```text
Select an option: 1

Enter alarm time (e.g. 07:30 AM or 19:30): 07:30 AM
Enter label (optional): Morning

Alarm created successfully.
ID: 1
Time: 07:30 AM
Label: Morning
```

The following time formats are accepted :

```text
07:30 AM
7:30 PM
07:30PM
19:30
```

## Viewing Alarms

Select `2` to see the alarms currently configured.

Example :

```text
=======================================================
ID    Time       Status     Label
-------------------------------------------------------
1     07:30 AM   Enabled    Morning
2     09:00 AM   Disabled   Meeting
=======================================================
```

Each alarm has its own ID, which is used when enabling, disabling, or deleting it.

## Disabling an Alarm

To temporarily stop an alarm from ringing :

```text
Select an option: 4
Enter alarm ID: 1

Alarm 1 disabled.
```

The alarm remains in the list and can be enabled again later.

## Enabling an Alarm

Select option `3` and provide the alarm ID :

```text
Select an option: 3
Enter alarm ID: 1

Alarm 1 enabled.
```

## Deleting an Alarm

To permanently remove an alarm :

```text
Select an option: 5
Enter alarm ID: 2

Alarm 2 deleted.
```

## When an Alarm Rings

When the configured time is reached, the application displays an alarm message and produces a terminal beep where the terminal supports it.

Example :

```text
==================================================
              ALARM RINGING!
==================================================

Time: 07:30:00 AM
Label: Morning

[S] Snooze for 5 minutes
[D] Dismiss

Choose an option:
```

Enter :

```text
S
```

to snooze the alarm for five minutes.

Or :

```text
D
```

to dismiss it.

## Multiple Alarms

Multiple alarms can be configured at the same time.

For example :

```text
ID    Time       Status     Label
-------------------------------------------------------
1     07:00 AM   Enabled    Wake Up
2     08:30 AM   Enabled    Meeting
3     01:00 PM   Enabled    Lunch
4     06:30 PM   Disabled   Gym
```

Each enabled alarm is checked while the application is running.

## Important Notes

Alarms are kept in memory while the application is running.

There is currently no persistent storage. If the application is closed, the configured alarms are lost.

The application also needs to remain running for alarms to trigger.

For example, if set an alarm for `08:00 AM` and close the terminal before 08:00 AM, the alarm will not run.

## Stopping the Application

Select :

```text
6. Exit
```

Its also stop the application using :

```text
Ctrl+C
```

The application handles the interruption and exits cleanly.

## Troubleshooting

### `python` command is not recognized

Make sure Python is installed and added in system PATH.

Try:

```bash
python3 --version
```

or:

```bash
python --version
```

### No sound when the alarm rings

The application uses the terminal bell (`\a`) for the audible notification. Whether this produces an actual sound depends on the operating system and terminal configuration.

The alarm message will still be displayed even if the terminal does not produce a sound.

## Limitations

This is intentionally a small command-line application. It currently does not provide :

* Persistent alarms
* Recurring weekly schedules
* Custom alarm sounds
* Desktop notifications
* Mobile notifications
* Web interface
* Database storage

These can be added later if required.
