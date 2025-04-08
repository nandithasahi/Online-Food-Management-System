use food_ordering_project;
DROP DATABASE food_ordering_project;
CREATE DATABASE food_ordering_project;

SHOW TABLES;
/*pending,delivery,first name, last name, check other attributes */
SELECT * FROM orders_cart;
SELECT * FROM orders_delivery;
SELECT * FROM orders_menuitem;
SELECT * FROM orders_order;
SELECT * FROM orders_orderitem;
SELECT * FROM orders_restaurant;
SELECT * FROM orders_review;
select * from auth_user;
select * from orders_delivery;
select * from orders_deliverypersonnel;

INSERT INTO orders_restaurant (restaurant_id, res_name, res_email, res_phone_number, res_address)
VALUES
(1, 'Foodie Palace', 'contact@foodiepalace.com', '9876543210', '123 Main Street'),
(2, 'Biryani Bliss', 'hello@biryanibliss.com', '9123456780', '56 Aroma Avenue'),
(3, 'Tandoori Treats', 'info@tandooritreats.com', '9012345678', '99 Grill Lane'),
(4, 'Pizza Planet', 'order@pizzaplanet.com', '8800123456', '45 Cheese Avenue'),
(5, 'Sushi House', 'connect@sushihouse.com', '7009988776', '87 Tokyo Street');

INSERT INTO orders_menuitem (menuitem_id, restaurant_id, item_name, item_price, item_description)
VALUES
-- Foodie Palace (restaurant_id = 1)
(1, 1, 'Veg Burger', 120.00, 'Crispy patty with lettuce and cheese'),
(2, 1, 'Cheese Fries', 80.00, 'Fries topped with cheese sauce'),
(3, 1, 'Paneer Wrap', 150.00, 'Wrap with spicy paneer filling'),
(4, 1, 'Grilled Sandwich', 100.00, 'Stuffed with veggies and cheese'),
(5, 1, 'Choco Shake', 90.00, 'Thick chocolate milkshake'),

-- Biryani Bliss (restaurant_id = 2)
(6, 2, 'Chicken Biryani', 220.00, 'Aromatic rice with spicy chicken'),
(7, 2, 'Mutton Biryani', 250.00, 'Flavorful rice with tender mutton'),
(8, 2, 'Veg Biryani', 180.00, 'Basmati rice with vegetables'),
(9, 2, 'Egg Biryani', 200.00, 'Boiled eggs with biryani rice'),
(10, 2, 'Biryani Combo Meal', 300.00, 'Includes biryani, raita & sweet'),

-- Tandoori Treats (restaurant_id = 3)
(11, 3, 'Tandoori Chicken', 280.00, 'Charcoal-grilled spicy chicken'),
(12, 3, 'Paneer Tikka', 200.00, 'Grilled paneer with spices'),
(13, 3, 'Tandoori Roti', 30.00, 'Clay oven baked Indian bread'),
(14, 3, 'Butter Naan', 40.00, 'Naan topped with butter'),
(15, 3, 'Chicken Tikka', 260.00, 'Boneless grilled chicken cubes'),

-- Pizza Planet (restaurant_id = 4)
(16, 4, 'Margherita Pizza', 200.00, 'Classic cheese pizza with herbs'),
(17, 4, 'Veggie Supreme', 250.00, 'Loaded with fresh vegetables'),
(18, 4, 'Pepperoni Pizza', 300.00, 'Topped with spicy pepperoni'),
(19, 4, 'Cheese Garlic Bread', 120.00, 'Garlic bread with cheese'),
(20, 4, 'Choco Lava Cake', 110.00, 'Warm chocolate-filled dessert'),

-- Sushi House (restaurant_id = 5)
(21, 5, 'Salmon Sushi', 350.00, 'Fresh salmon with rice and wasabi'),
(22, 5, 'Tuna Roll', 320.00, 'Tuna wrapped in rice and seaweed'),
(23, 5, 'Avocado Maki', 280.00, 'Vegan sushi with avocado'),
(24, 5, 'Tempura Prawn Roll', 360.00, 'Crispy prawns with sushi rice'),
(25, 5, 'Miso Soup', 150.00, 'Traditional Japanese soup');

SET SQL_SAFE_UPDATES = 0;
UPDATE orders_deliverypersonnel
SET status = 'free'
WHERE status = 'busy';
SET SQL_SAFE_UPDATES = 1;  


