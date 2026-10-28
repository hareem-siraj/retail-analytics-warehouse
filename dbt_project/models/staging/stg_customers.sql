with source as (

    select *
    from {{ source('raw', 'customers') }}

),

cleaned as (

    select
        nullif(trim(customer_id), '') as customer_id,
        nullif(trim(customer_name), '') as customer_name,
        nullif(lower(trim(email)), '') as email,
        initcap(nullif(trim(city), '')) as city,
        initcap(nullif(trim(segment), '')) as segment,
        try_to_timestamp_ntz(
            nullif(trim(updated_at), '')
        ) as updated_at

    from source

)

select *
from cleaned
