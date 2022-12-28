
# from scratch dbt-fal setup

How to start a dbt-fal project in SomEnergia, prepared to be run by airflow

[getting started dbt](https://docs.getdbt.com/docs/get-started/getting-started-dbt-core)

First we init the project, which will create a dbt directory within our project

```bash
dbt init dbt_dades_sandbox
```

You should then check `~/.dbt/profiles.yml` to check your database connections or add one if you're starting anew
under the `dbt_dades_sandbox` section.


To add fal you have to add another target in your profiles.yml. [Quickstart](https://docs.fal.ai/dbt-fal/quickstart)

```yaml
    pre_with_fal:
      type: fal
      db_profile: pre # This points to your main adapter
```

You can now create a python script in `dbt_dades_sandbox/fal_models/`

We will continue with [Getting started](https://github.com/fal-ai/fal#getting-started).

e.g. `average.py`

Airflow will need a profiles.yaml that we'll pass via command-line using the airflow secrets. [More info](https://docs.getdbt.com/docs/get-started/connection-profiles#advanced-using-environment-variables)

```bash
'DBUSER="{{ var.value.puppis_prod_db }}" DBPASSWORD="{{ var.value.puppis_prod_db }}" fal flow run --profile-dir config'
```

and locally you can specify the profile directory in the same way or run with the default `~/.dbt/profiles.yml`.

Note that you have to run it from the dbt_dades_sandbox directory.

```bash
fal flow run
```

`fal flow run` will run the dbt models, then the python scripts creating an ephemeral table
and finally the following models. If you don't re-run dbt you can also do `fal run` or `dbt run` only.

`--project-dir` doesn't seem to be correctly supported by fal as it stores part of its output on the root directory (`target`) and another in the dbt project dir instead of placing everything in the `dbt_dades_sandbox/target`

You can check [this fal post](https://blog.fal.ai/python-data-modes/) for a more detailed info.

# nice things

Now in the python script you can reference tables and dbt models using `ref` and `source` and save the output in a table using `write_to_model`.

# documentation

With this command we create the documentation to serve in a web with the Directed Acyclic Graph of the dbt models and its descriptions.

```bash
dbt docs generate
```

```bash
dbt docs serve
```
