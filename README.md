Tempo backend for Taxi
======================

This is the Tempo backend for [Taxi](https://github.com/sephii/taxi). It
exposes the `tempo` protocol to push entries to JIRA's [Tempo](https://www.tempo.io) app.

Installation
------------

```shell
taxi plugin install tempo
```

Known limitations
-----------------

### Duration as hours is not supported

As stated in [taxi's documentation](https://taxi-timesheets.readthedocs.io/en/master/userguide.html#timesheet-syntax) :

> duration can either be a time range or a duration in hours. If it’s a time range, it should be in the format start-end, where start can be left blank if the previous entry also used a time range and had a time defined, and end can be ? if the end time is not known yet, leading to the entry being ignored. Each part of the range should have the format HH:mm, or HHmm. If duration is a duration, it should just be a number, eg. 2 for 2 hours, or 1.75 for 1 hour and 45 minutes.

However, Tempo requires `startTime` in its API, so a proper error will be thrown if you do not provide a time range.

Usage
-----

In your `.taxirc` file, use the `tempo` protocol for your backend.

```ini
[backends]
my_tempo_backend = tempo://[jira_user_account_id]:[tempo_api_token]@api.tempo.io/core/3/
```

To auto-generate taxi aliases, you can specify your JIRA projects as follow:

```ini
[tempo_projects]
infra = 10000
ops = 1000
dev = 100
```

The numbers represent the range of JIRA tickets being aliased (DEV-1, DEV-2, DEV-3, ..., DEV-100).
