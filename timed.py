#!/usr/bin/env python3
"""timed: a command-line time tracker. Python3 port."""

import sys
import os.path
import time, datetime

import argparse

__author__ = 'Adeel Ahmad Khan, Tom Vincent'

log_file = os.path.expanduser('~/.timed')
time_format = '%H:%M on %d %b %Y'

def status(quiet=False):
  "print current status"

  logs = read()
  if logs:
    last = logs[-1]
    if not last.get('end'):
      project = last['project']
      start = last.get('start')
      end = datetime.datetime.now()

      if not quiet:
        print(("working on %s:" % project))
        print(("  from    %s" % start.strftime(time_format)))
        print(("  to now, %s" % end.strftime(time_format)))
        print(("       => %s have elapsed" % elapsed_time(start, end)))
      else:
        print(project)
    else:
      if not quiet:
        summary()
  else:
    if not quiet:
      help()


def summary():
  "print a summary of hours for all projects"

  logs = read()
  summary = {}
  for log in logs:
    if log['project'] not in summary:
      summary[log['project']] = 0
    end = log.get('end', datetime.datetime.now())
    start = log.get('start')
    summary[log['project']] += (end - start).seconds / 60

  for project, min in list(summary.items()):
    print(("  - %s: %sh%sm" % (project, min/60, min - 60 * (min/60))))

def get_week(dt=None):
    if dt == None:
        dt = datetime.datetime.today()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    offset = datetime.timedelta(days=dt.isoweekday())

    startOfWeek = dt - offset

    offset = datetime.timedelta(days=6)

    endOfWeek = startOfWeek + offset

    key = "%s to %s" % (startOfWeek.strftime("%Y-%m-%d"),
        endOfWeek.strftime("%Y-%m-%d"))

    return key

def get_day(dt=None):
    if dt == None:
        dt = datetime.datetime.today()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    return dt.strftime("%Y-%m-%d")

def get_month(dt=None):
    if dt == None:
        dt = datetime.datetime.today()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    return dt.strftime("%Y-%m")

def get_year(dt=None):
    if dt == None:
        dt = datetime.datetime.today()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    return dt.strftime("%Y")


def report(d=None, day=None, w=None, week=None, m=None, month=None, y=None,
    year=None):
  "print a summary of hours by day, week, month, year"

  # handle short or long options with - or --
  if isinstance(d, str):
    if d == '-d':
      day = True
    elif d == '-w':
      week = True
    elif d == '-m':
      month = True
    elif d == '-y':
      year = True

    d = None

  get_key = None

  if d or day:
    get_key = get_day
  elif w or week:
    get_key = get_week
  elif m or month:
    get_key = get_month
  elif y or year:
    get_key = get_year
  else:
    global summary
    summary()
    return

  logs = read()
  periods = {}
  for log in logs:
    end = log.get('end', datetime.datetime.now())
    start = log.get('start')

    key = get_key(start)

    summary = periods.setdefault(key, {})

    if log['project'] not in summary:
      summary[log['project']] = 0
    summary[log['project']] += (end - start).seconds / 60

  first = False

  for key, summary in sorted(periods.items()):
    if not first:
      print()
    else:
      first = True

    total = sum(summary.values())
    hours = total/60
    minutes = total - 60*(total/60)

    print(("%s - %sh%sm" % (key, hours, minutes)))

    for project, min in sorted(summary.items()):
      print(("    - %s: %sh%sm" % (project, min/60, min - 60 * (min/60))))


def start(project):
  "start tracking for <project>"

  logs = read()
  start = datetime.datetime.now()
  logs.append({'project': project, 'start': start})
  save(logs)
  print(("starting work on %s" % project))
  print(("  at %s" % start.strftime(time_format)))


def stop():
  "stop tracking for the current project"

  logs = read()
  if not logs:
    print("error: no active project")
  else:
    last = logs[-1]
    project = last['project']
    start = last.get('start')
    end = datetime.datetime.now()
    print(("worked on %s" % project))
    print(("  from    %s" % start.strftime(time_format)))
    print(("  to now, %s" % end.strftime(time_format)))
    print(("       => %s elapsed" % elapsed_time(start)))

    logs[-1]['end'] = end
    save(logs)


def restart():
  "restart tracking for the last project"

  logs = read()
  if not logs:
    print("error: no active project")
  else:
    last = logs[-1]
    project = last['project']
    start = datetime.datetime.now()
    logs.append({'project': project, 'start': start})
    save(logs)
    print(("starting work on %s" % project))
    print(("  at %s" % start.strftime(time_format)))

def elapsed_time(start, end=None):
  if not end:
    end = datetime.datetime.now()
  delta = (end - start).seconds
  hour = delta / 3600
  min = (delta - 3600 * hour) / 60
  return '%sh%sm' % (hour, min)

def read():
  logs = []
  with open(log_file) as data:
    try:
      for line in data:
        project, line = line.split(':', 1)
        project = project.strip()

        start, end = line.split(' - ')
        start, end = start.strip(), end.strip()

        if not project or not start:
          raise SyntaxError()

        start = datetime.datetime.strptime(start, time_format)
        if end:
          end = datetime.datetime.strptime(end, time_format)

        if end:
          logs.append({'project': project, 'start': start, 'end': end})
        else:
          logs.append({'project': project, 'start': start})

    except ValueError:
      raise SyntaxError()

  return logs

def save(logs):
  file = open(log_file, 'w')

  def format(log):
    if log.get('end'):
      return '%s: %s - %s' % (log['project'],
        log['start'].strftime(time_format),
        log['end'].strftime(time_format))
    else:
      return '%s: %s - ' % (log['project'],
        log['start'].strftime(time_format))

  dump = '\n'.join((format(log) for log in logs))

  file.write(dump)
  file.close()

class SyntaxError(Exception):
  args = 'Syntax error in ~/.timed'

def parseArgs():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="sub-commands")

    status = subparsers.add_parser("status",
        help="print current status")
    status.set_defaults(func=status)

    stop = subparsers.add_parser("stop",
        help="stop tracking for the current project")
    stop.set_defaults(func=stop)

    summary = subparsers.add_parser("summary",
        help="print a summary of hours for all projects")
    summary.set_defaults(func=summary)

    start = subparsers.add_parser("start",
        help="start tracking for <project>")
    start.add_argument("project", help="the project name")
    start.set_defaults(func=start)

    report = subparsers.add_parser("report",
        help="print a summary of hours by day, week, month, year",)
    report.add_argument("-d", "--day", help="summary of hours by day")
    report.add_argument("-w", "--week", help="summary of hours by week")
    report.add_argument("-m", "--month", help="summary of hours by month")
    report.add_argument("-y", "--year", help="summary of hours by year")
    report.set_defaults(func=report)

    restart = subparsers.add_parser("restart",
        help="restart tracking for the last project")
    restart.set_defaults(func=restart)

    args = parser.parse_args()
    args.func(args)

def main():
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    parseArgs()

if __name__ == '__main__':
  main()
