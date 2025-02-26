-- This model is used to refine the COT (Commitments of Traders) report data 
-- by removing unnecessary columns and adding a unique key for the date and commodity name.
-- It is also used to filter the data for a specific commodity, in this case, wheat.    

{{ config(
    materialized='incremental', -- Incremental strategy is used to update the data in the table
    unique_key=['date', 'commodity_name'], -- Unique key is used to ensure that the data is unique
    incremental_strategy='delete+insert' -- Incremental strategy is used to update the data in the table
) }}

{# Documentation for the model #}
{{ 
    config(
        description="Refined COT (Commitments of Traders) report data with position percentages for different trader categories",
        tags=['cftc', 'trading']
    )
}}

with raw_cot as (
    select raw_cot.*
    from {{ source('CFTC', '05_COT_Legacy_Combined_Report') }} raw_cot
    {% if is_incremental() %}
    where raw_cot.report_date_as_yyyy_mm_dd > (select max(date) from {{ this }})
    {% endif %}
)

select
    raw_cot.report_date_as_yyyy_mm_dd as date,
    raw_cot.commodity_name,
    raw_cot.pct_of_oi_noncomm_long_all,
    raw_cot.pct_of_oi_noncomm_short_all,
    raw_cot.pct_of_oi_comm_long_all,
    raw_cot.pct_of_oi_comm_short_all

from raw_cot

WHERE raw_cot.commodity_name = 'WHEAT'


