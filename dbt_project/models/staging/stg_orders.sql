with source as (

    select *
    from {{ source('raw', 'orders') }}

),

cleaned as (

    select
        nullif(trim(order_line_id), '') as order_line_id,
        nullif(trim(order_id), '') as order_id,
        nullif(trim(customer_id), '') as customer_id,
        nullif(trim(product_id), '') as product_id,

        coalesce(
            try_to_date(nullif(trim(order_date), ''), 'YYYY-MM-DD'),
            try_to_date(nullif(trim(order_date), ''), 'DD/MM/YYYY')
        ) as order_date,

        try_to_number(nullif(trim(quantity), '')) as quantity,

        try_to_decimal(
            nullif(trim(unit_price), ''),
            12,
            2
        ) as unit_price,

        lower(nullif(trim(status), '')) as status,

        try_to_timestamp_ntz(
            nullif(trim(updated_at), '')
        ) as updated_at,

        try_to_timestamp_ntz(
            nullif(trim(loaded_at), '')
        ) as loaded_at

    from source

),

deduplicated as (

    select *
    from cleaned
    qualify row_number() over (
        partition by order_line_id
        order by loaded_at desc nulls last
    ) = 1

)

select
    *,
    quantity > 0 as is_valid_quantity,
    unit_price > 0 as is_valid_price,
    order_date is not null as is_valid_order_date
from deduplicated
