# WIS2Box ADL ADCON Plugin

[WIS2Box ADL](https://github.com/wmo-raf/wis2box-adl) Plugin for automated observation data loading from ADCON AWS
Network into the WIS2Box

## Introduction

[WIS2Box Automated Data Loader](https://github.com/wmo-raf/wis2box-adl) is a Wagtail based web application that provides
functionality for automating periodic Observation data ingestion into WIS2Box node, from Automatic and or Manual
Weather Stations. ADL is a plugin based system that defines an architecture for implementing wis2box data loaders for
different AWS vendors.

This plugin is an implementation of the ADL plugin for the ADCON AWS Network. The goal is to provide
functionality to ingest data from ADCON AWS Network into the WIS2Box.

## Installation

This plugin contains Django/Wagtail app that should be installed in the WIS2Box ADL project. This means that you need to
have the WIS2Box ADL project installed and running before you can install this plugin.

For installation of the WIS2Box ADL project, please refer to the [WIS2Box ADL](https://github.com/wmo-raf/wis2box-adl)
documentation.

### 1. Add the plugin to the WIS2Box ADL project

At the root of the `wis2box-adl`, edit the `.env` file and add the following line:

```sh
WIS2BOX_ADL_PLUGIN_GIT_REPOS="https://github.com/wmo-raf/wis2box-adl-adcon-plugin.git"
```

The `WIS2BOX_ADL_PLUGIN_GIT_REPOS` is a comma separated list of git repositories that contain the ADL plugins. If there
is an existing plugin url, add the new plugin repository to the list separated by a comma.

### 2. Add custom environment variables

`wis2box-adl-adcon-plugin` requires the following environment variables to be set:

```sh
WIS2BOX_ADL_ADCON_DATABASE_URL=
WIS2BOX_ADL_ADCON_INIT_DATETIME=
```

These should be added to the `.env` file in the root of the `wis2box-adl` project.

| Variable                        | Description                                                                                                                                         | Example                                             | Required |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|----------|
| WIS2BOX_ADL_ADCON_DATABASE_URL  | Full ADCON addVANTAGE PostgreSQL database connection string                                                                                         | postgres://postgres:postgres@<ip>:<port>/addvantage | YES      |
| WIS2BOX_ADL_ADCON_INIT_DATETIME | The initial date-time to start from, when querying data from ADCON database. Leave blank to use the current system time when the plugin initializes | 2024-10-29 00:00                                    | NO       |

After adding, we need to update our `docker compose` configuration to include these new environment variables. We do not
want to edit the core `docker-compose.yml` file, instead we will create a new file called `docker-compose.override.yml`
in the root of the `wis2box-adl` project.

You can copy the sample `docker-compose.override.sample.yml` file:

```shell
cp docker-compose.override.sample.yml docker-compose.override.yml
```

The contents of the `docker-compose.override.yml` file should look like this:

```yaml
x-backend-variables: &backend-variables
  WIS2BOX_ADL_ADCON_DATABASE_URL: ${WIS2BOX_ADL_ADCON_DATABASE_URL}
  WIS2BOX_ADL_ADCON_INIT_DATETIME: ${WIS2BOX_ADL_ADCON_INIT_DATETIME}

services:
  wis2box_adl:
    environment:
      <<: *backend-variables
    extra_hosts:
      - "host.docker.internal:host-gateway"
  wis2box_adl_celery_worker:
    environment:
      <<: *backend-variables
    extra_hosts:
      - "host.docker.internal:host-gateway"

  wis2box_adl_celery_beat:
    environment:
      <<: *backend-variables
    extra_hosts:
      - "host.docker.internal:host-gateway"
```






