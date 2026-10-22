-- =====================================================================
-- Realistic sample data for the QueryPilot demo analytics database.
-- Enough volume and variety to make generated charts/aggregates
-- actually look meaningful (not just 2-3 rows).
-- =====================================================================

INSERT INTO categories (category_name) VALUES
    ('Electronics'), ('Home & Kitchen'), ('Books'), ('Sportswear'), ('Beauty')
ON CONFLICT (category_name) DO NOTHING;

INSERT INTO customers (full_name, email, city, country, signup_date, is_active) VALUES
    ('Aarav Sharma', 'aarav.sharma@example.com', 'Bengaluru', 'India', '2024-01-12', TRUE),
    ('Meera Nair', 'meera.nair@example.com', 'Kochi', 'India', '2024-02-03', TRUE),
    ('Rohan Gupta', 'rohan.gupta@example.com', 'Delhi', 'India', '2024-02-20', TRUE),
    ('Ishita Verma', 'ishita.verma@example.com', 'Mumbai', 'India', '2024-03-05', TRUE),
    ('Karan Patel', 'karan.patel@example.com', 'Ahmedabad', 'India', '2024-03-18', FALSE),
    ('Sofia Rossi', 'sofia.rossi@example.com', 'Milan', 'Italy', '2024-04-01', TRUE),
    ('Liam O''Connor', 'liam.oconnor@example.com', 'Dublin', 'Ireland', '2024-04-14', TRUE),
    ('Yuki Tanaka', 'yuki.tanaka@example.com', 'Osaka', 'Japan', '2024-05-02', TRUE),
    ('Emma Johnson', 'emma.johnson@example.com', 'Austin', 'USA', '2024-05-19', TRUE),
    ('Noah Kim', 'noah.kim@example.com', 'Seoul', 'South Korea', '2024-06-07', TRUE)
ON CONFLICT (email) DO NOTHING;

INSERT INTO products (product_name, category_id, unit_price, stock_quantity) VALUES
    ('Wireless Earbuds Pro', 1, 3499.00, 120),
    ('4K Action Camera', 1, 8999.00, 45),
    ('Smart LED Desk Lamp', 2, 1299.00, 200),
    ('Stainless Steel Cookware Set', 2, 4599.00, 60),
    ('Atomic Habits (Book)', 3, 399.00, 300),
    ('The Pragmatic Programmer (Book)', 3, 899.00, 150),
    ('Running Shoes Air Flex', 4, 2999.00, 90),
    ('Yoga Mat Premium', 4, 899.00, 180),
    ('Vitamin C Serum', 5, 649.00, 250),
    ('Herbal Shampoo 500ml', 5, 349.00, 220)
ON CONFLICT DO NOTHING;

-- 15 orders spread across customers and dates, each with 1-3 line items
INSERT INTO orders (customer_id, order_date, status) VALUES
    (1, '2024-06-01', 'completed'),
    (2, '2024-06-02', 'completed'),
    (3, '2024-06-03', 'completed'),
    (1, '2024-06-10', 'completed'),
    (4, '2024-06-12', 'cancelled'),
    (5, '2024-06-15', 'completed'),
    (6, '2024-06-18', 'completed'),
    (7, '2024-06-20', 'refunded'),
    (8, '2024-06-22', 'completed'),
    (9, '2024-06-25', 'completed'),
    (2, '2024-07-01', 'completed'),
    (10, '2024-07-03', 'completed'),
    (3, '2024-07-05', 'pending'),
    (6, '2024-07-10', 'completed'),
    (9, '2024-07-15', 'completed');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 3499.00), (1, 5, 2, 399.00),
    (2, 3, 1, 1299.00),
    (3, 7, 1, 2999.00), (3, 8, 1, 899.00),
    (4, 2, 1, 8999.00),
    (5, 9, 2, 649.00),
    (6, 6, 1, 899.00), (6, 5, 1, 399.00),
    (7, 4, 1, 4599.00),
    (8, 10, 3, 349.00),
    (9, 1, 2, 3499.00),
    (10, 8, 1, 899.00), (10, 9, 1, 649.00),
    (11, 3, 2, 1299.00),
    (12, 2, 1, 8999.00),
    (13, 7, 1, 2999.00),
    (14, 5, 5, 399.00),
    (15, 1, 1, 3499.00), (15, 10, 2, 349.00);