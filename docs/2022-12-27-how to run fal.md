
# from scratch dbt-fal setup

How to start a dbt-fal project in SomEnergia, prepared to be run by airflow

[getting started dbt](https://docs.getdbt.com/docs/get-started/getting-started-dbt-core)

First we init the project, which will create a dbt directory within our project

```bash
dbt init dbt_dades_sandbox
```

You should then check `~/.dbt/profiles.yml` to check your database connections or add one if you're starting anew
under the `dbt_dades_sandbox` section.






# Run fal locally

[Getting started](https://github.com/fal-ai/fal#getting-started)

[Quickstart](https://docs.fal.ai/dbt-fal/quickstart)

```bash
fal run --project-dir dbt_jardiner/ --target prod
```

# Run fal/dbt in airflow

Airflow will need a profiles.yaml that we'll pass via command-line using the airflow secrets.

https://docs.getdbt.com/docs/get-started/connection-profiles#advanced-using-environment-variables



