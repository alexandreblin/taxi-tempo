from collections import defaultdict

from taxi.aliases import aliases_database
from taxi.backends import BaseBackend, PushEntryFailed
from taxi.projects import Activity, Project

import requests

class TempoBackend(BaseBackend):
    HASH_N=3
    
    def __init__(self, **kwargs):
        super(TempoBackend, self).__init__(**kwargs)
        self.path = self.path.lstrip('/')
        self.settings = self.context['settings']

        self.worker_id = kwargs['username']
        self.api_key = kwargs['password']
        self.hostname = kwargs['hostname']

    def push_entry(self, date, entry):
        if not isinstance(entry.duration, tuple):
            raise PushEntryFailed('This backend does not support durations as hours. Please use a time range.')

        seconds = int(entry.hours * 3600)
        mapping = aliases_database[entry.alias]

        r = requests.post(f'https://{self.hostname}/{self.path}/worklogs', json={
            'issueKey': "%s-%d" % (self.get_project_name(mapping.mapping[0]), mapping.mapping[1]),
            'timeSpentSeconds': seconds,
            'startDate': date.strftime('%Y-%m-%d'),
            'startTime': entry.get_start_time().strftime('%H:%M:%S'),
            'description': entry.description,
            'authorAccountId': self.worker_id,
        }, headers={
            'Authorization': f'Bearer {self.api_key}'
        })

        if r.status_code != 200:
            raise PushEntryFailed(', '.join(e['message'] for e in r.json()['errors']))

    def get_project_hash(self, project_name):
        hash = 0
        for i, c in enumerate(project_name.upper()):
            hash += ord(c) * pow(10, i * self.HASH_N)

        return hash

    def get_project_name(self, hash):
        hash = str("0%d" % hash)

        ords = [hash[i:i+self.HASH_N] for i in range(0, len(hash), self.HASH_N)]
        ords.reverse()
        letters = list(map(lambda ord: chr(int(ord)), ords))

        return "".join(letters)

    def get_projects(self):
        projects_list = []

        for project_name, count in self.settings.config.items('jira_projects'):
            project_name = project_name.upper()
            p = Project(self.get_project_hash(project_name), project_name, Project.STATUS_ACTIVE)
            for i in range(1, int(count) + 1):
                name = f'{project_name}-{i}'
                a = Activity(i, name, 0)
                p.add_activity(a)
                p.aliases[name] = a.id

            projects_list.append(p)

        return projects_list
