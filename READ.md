### Monthly Sales Analytics

The `MONTHLY_SALES` model aggregates completed sales by calendar month and provides the following business metrics:

- **Total orders:** Distinct order IDs within each month.
- **Unique customers:** Distinct customers who purchased during each month.
- **Units sold:** Total quantity sold during the month.
- **Total revenue:** Sum of sales-line revenue for the month.

#### Understanding Order Counts

The sample dataset contains 268 globally distinct order IDs, while summing the monthly order counts produces 355 distinct order-month combinations.

These metrics measure different things. An order ID that appears in multiple months is counted once in each relevant month's summary, but only once in the overall distinct order count. Therefore, monthly distinct order counts should not automatically be summed to calculate the global number of distinct orders.

The monthly revenue aggregation reconciles with the fact table, with both reporting total revenue of **277,002.88**.

This distinction highlights the importance of understanding data grain when designing analytical models and interpreting business metrics.