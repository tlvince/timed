#!/usr/bin/env python3

"""A command-line time tracker."""

__author__ = 'Adeel Ahmad Khan\nTom Vincent'

import sys
import time
import datetime

class Timed:
    """Timed represents a stopwatch.

    It tracks time spent on projects by writing a timestamp the given log file,
    in the given (human-readable) format.
    """

    def __init__(self, log_file, time_format):
        """Construct an object of type Timed."""
        self.log_file = log_file
        self.time_format = time_format

    def status(self, quiet=False):
        """Print current status."""
        logs = self.read()
        if logs:
            last = logs[-1]
            if not last.get('end'):
                project = last['project']
                start = last.get('start')
                end = datetime.datetime.now()
                
                if not quiet:
                    print("working on %s:" % project)
                    print("  from    %s" % start.strftime(time_format))
                    print("  to now, %s" % end.strftime(time_format))
                    print("       => %s have elapsed" % elapsed_time(start, end))
                else:
                    print(project)
            else:
                if not quiet:
                    self.summary()
        else:
            if not quiet:
                print("Log empty")

    def summary(self):
        """Print a summary of hours for all projects."""
        
        logs = self.read()
        summary = {}
        for log in logs:
            if log['project'] not in summary:
                summary[log['project']] = 0
            end = log.get('end', datetime.datetime.now())
            start = log.get('start')
            summary[log['project']] += (end - start).seconds / 60
        
        for project, min in list(summary.items()):
            print("  - %s: %sh%sm" % (project, min/60, min - 60 * (min/60)))

    def start(self, project):
        """Start tracking for <project>."""
        
        logs = self.read()
        start = datetime.datetime.now()
        logs.append({'project': project, 'start': start})
        save(logs)
        print("starting work on %s" % project)
        print("  at %s" % start.strftime(time_format))

    def stop(self):
        """Stop tracking for the current project."""
        
        logs = self.read()
        if not logs:
            print("error: no active project")
        else:
            last = logs[-1]
            project = last['project']
            start = last.get('start')
            end = datetime.datetime.now()
            print("worked on %s" % project)
            print("  from    %s" % start.strftime(time_format))
            print("  to now, %s" % end.strftime(time_format))
            print("       => %s elapsed" % elapsed_time(start))
            
            logs[-1]['end'] = end
            self.save(logs)

    def elapsed_time(self, start, end=None):
        """Return the elapsed time spent working on the current project."""
        if not end:
            end = datetime.datetime.now()
        delta = (end - start).seconds
        hour = delta / 3600
        min = (delta - 3600 * hour) / 60
        return '%sh%sm' % (hour, min)

    def read(self):
        """Read log file."""
        logs = []
        with open(self.log_file) as data:
            try:
                for line in data:
                    project, line = line.split(':', 1)
                    project = project.strip()
                    
                    start, end = line.split(' - ')
                    start, end = start.strip(), end.strip()
                    
                    if not project or not start:
                        raise SyntaxError()
                    
                    start = datetime.datetime.strptime(start, self.time_format)
                    if end:
                        end = datetime.datetime.strptime(end, self.time_format)
                    
                    if end:
                        logs.append({'project': project, 'start': start, 'end': end})
                    else:
                        logs.append({'project': project, 'start': start})
                    
            except ValueError:
                raise SyntaxError()
        
        return logs

    def save(self, logs):
        """Save log file."""
        file = open(log_file, 'w')

class SyntaxError(Exception):
    """An error thrown if there's an unexpected line in the log."""
    args = 'Syntax error in ~/.timed'
