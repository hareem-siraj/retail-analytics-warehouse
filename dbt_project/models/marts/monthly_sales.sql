
with sales as (
    select *
    from {{ ref('fact_sales') }}
)

select
    date_trunc('month', order_date)::date as sales_month,
    count(distinct order_id) as total_orders,
    count(distinct customer_id) as unique_customers,
    sum(quantity) as units_sold,
    round(sum(line_revenue), 2) as total_revenue
from sales
group by 1
order by 1
