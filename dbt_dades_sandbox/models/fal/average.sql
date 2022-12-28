
{{ config(materialized='ephemeral') }}
/*
FAL_GENERATED 8735854b74e50be772c19fd589e86079

Script dependencies:

{{ ref('my_first_dbt_model') }}
{{ source('dades_sandbox', 'energy_budget') }}
{{ ref('my_first_dbt_model') }}

*/

SELECT * FROM {{ this }}
