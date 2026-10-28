select
    product_id,
    product_name,
    category,
    unit_price as current_product_price
from {{ ref('stg_products') }}
where product_id is not null
