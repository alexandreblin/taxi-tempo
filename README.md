Tempo backend for Taxi
======================

This is the Tempo backend for [Taxi](https://github.com/sephii/taxi). It
exposes the `tempo` protocol to push entries to JIRA's [Tempo](https://www.tempo.io) app.

Installation
------------

```shell
taxi plugin install tempo
```

Configuration
-------------

Run `taxi config` and use the `tempo` protocol for your backend :

```ini
[backends]
my_tempo_backend = tempo://[jira_user_account_id]:[tempo_api_token]@api.tempo.io/core/3/
```

* `[jira_user_account_id]` can be found at the end of the URL of your JIRA profile page, like `https://[instance].atlassian.net/jira/people/5daee3299703bc0c2d27a5cc` (to open this page, click on your avatar in the top right corner, then click the `Profile` link in the section with your name)
* `[tempo_api_token]` is a token you need to create by going to the `Apps > Tempo > Settings > API Integration > [+ New Token]` page in Jira :
    * give it a name (like `taxi`)
    * set the expiration to 5000 days (so you don't need to worry about that
    * set a custom access and check `Manage Worklogs` (it will automatically check `View Worklogs` too)

To generate taxi aliases, specify your JIRA projects as follows and run `taxi update`:

```ini
[jira_projects]
dev = 10000
ops = 1000
infra = 100
```

> The numbers represent the range of JIRA tickets that will be statically generated as taxi aliases (DEV-1, DEV-2, DEV-3, ..., DEV-100). Whenever your JIRA project reaches a ticket above that range, taxi will display a warning `inexistent alias` and ignore your entry. To fix it, run `taxi config`, raise the number and run `taxi update`.

Usage
-----

You can now add timesheet entries like :

```
19/05/2020 # Tuesday
INFRA-38      08:00-09:00    Monitoring server
DEV-2087           -10:30    Fixing bug
OPS-952            -?        Work in progress...
```

> You can use lowercase aliases too.

Things you should know
----------------------

### Duration as hours is not supported

As stated in [taxi's documentation](https://taxi-timesheets.readthedocs.io/en/master/userguide.html#timesheet-syntax) :

> duration can either be a time range or a duration in hours. If it’s a time range, it should be in the format start-end, where start can be left blank if the previous entry also used a time range and had a time defined, and end can be ? if the end time is not known yet, leading to the entry being ignored. Each part of the range should have the format HH:mm, or HHmm. If duration is a duration, it should just be a number, eg. 2 for 2 hours, or 1.75 for 1 hour and 45 minutes.

However, Tempo requires `startTime` in its API, so a proper error will be thrown if you do not provide a time range.

### Taxi regroups entries by default

By default, [taxi](https://taxi-timesheets.readthedocs.io/en/master/userguide.html#regroup-entries) regroups entries to commit them. So if you have 3 different entries on a day with the same alias and description, it will push only one entry with the cumulated times. In Tempo, this leads to worklogs overlapping each others, which you might not want. To fix it, add this configuration :

```
[taxi]
regroup_entries = false
```
