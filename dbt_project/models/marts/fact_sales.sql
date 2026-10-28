with orders as (

    select *
    from {{ ref('stg_orders') }}

),

customers as (

    select *
    from {{ ref('dim_customers') }}

),

products as (

    select *
    from {{ ref('dim_products') }}

)

select
    o.order_line_id,
    o.order_id,
    o.order_date,

    c.customer_id,
    c.customer_name,
    c.city as customer_city,
    c.segment as customer_segment,

    p.product_id,
    p.product_name,
    p.category as product_category,

    o.quantity,
    o.unit_price,
    o.quantity * o.unit_price as line_revenue,
    o.status,
    o.updated_at

from orders o

inner join customers c
    on o.customer_id = c.customer_id

inner join products p
    on o.product_id = p.product_id

where o.status = 'completed'
    and o.is_valid_quantity
    and o.is_valid_price
    and o.is_valid_order_date
