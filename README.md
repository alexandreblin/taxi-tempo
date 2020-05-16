Tempo backend for Taxi
======================

This is the Tempo backend for [Taxi](https://github.com/sephii/taxi). It
exposes the `tempo` protocol to push entries to JIRA's [Tempo](https://www.tempo.io) app.

Installation
------------

```shell
taxi plugin install tempo
```

Usage
-----

In your `.taxirc` file, use the `tempo` protocol for your backend.

```ini
[backends]
my_tempo_backend = tempo://jira_user_account_id:tempo_api_token@api.tempo.io/core/3/
```

To auto-generate taxi aliases, you can specify your JIRA projects as follow:

```ini
[tempo_projects]
infra = 10000
ops = 1000
dev = 100
```

The numbers represent the range of JIRA tickets being aliased (DEV-1, DEV-2, DEV-3, ..., DEV-100).
