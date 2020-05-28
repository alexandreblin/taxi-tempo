from collections import defaultdict

from taxi.aliases import aliases_database
from taxi.backends import BaseBackend, PushEntryFailed
from taxi.projects import Activity, Project

import requests

class TempoBackend(BaseBackend):
    def __init__(self, **kwargs):
        super(TempoBackend, self).__init__(**kwargs)

        self.name = 'tempo'
        self.path = self.path.lstrip('/')
        self.settings = self.context['settings']

        self.worker_id = kwargs['username']
        self.api_key = kwargs['password']
        self.hostname = kwargs['hostname']

    def push_entry(self, date, entry):
        if not isinstance(entry.duration, tuple):
            raise PushEntryFailed(
                f"[{self.name}] does not support durations as hours. Please use a time range instead."
            )

        seconds = int(entry.hours * 3600)
        mapping = aliases_database[entry.alias]

        r = requests.post(
            f"https://{self.hostname}/{self.path}/worklogs",
            json={
                'issueKey': f"{str(mapping.mapping[0]).upper()}-{int(mapping.mapping[1])}",
                'timeSpentSeconds': seconds,
                'startDate': date.strftime('%Y-%m-%d'),
                'startTime': entry.get_start_time().strftime('%H:%M:%S'),
                'description': entry.description,
                'authorAccountId': self.worker_id,
            },
            headers={'Authorization': f"Bearer {self.api_key}"}
        )

        if r.status_code != 200:
            raise PushEntryFailed(f"[{self.name}] {', '.join(e['message'] for e in r.json()['errors'])}")

    def get_projects(self):
        projects_list = []

        for project_name, count in self.settings.config.items('jira_projects'):
            project_name = project_name.upper()
            p = Project(project_name, f"[JIRA] {project_name}", Project.STATUS_ACTIVE,
                    description=f"JIRA Project {project_name} (created by backend {self.name})"
            )
            for i in range(1, int(count) + 1):
                name = f"{project_name}-{i}"
                a = Activity(i, name)
                p.add_activity(a)
                p.aliases[name] = a.id

            projects_list.append(p)

        return projects_list
