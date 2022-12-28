{{ config(materialized='view') }}

select count(*)
from {{ ref('average') }}
