select
    customer_id,
    customer_name,
    email,
    city,
    segment,
    updated_at
from {{ ref('stg_customers') }}
where customer_id is not null
