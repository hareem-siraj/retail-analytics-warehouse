with source as (

    select *
    from {{ source('raw', 'products') }}

),

cleaned as (

    select
        nullif(trim(product_id), '') as product_id,
        nullif(trim(product_name), '') as product_name,
        initcap(nullif(trim(category), '')) as category,
        try_to_decimal(
            nullif(trim(unit_price), ''),
            12,
            2
        ) as unit_price

    from source

)

select *
from cleaned
