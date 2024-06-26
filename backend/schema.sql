CREATE DATABASE airbnb;
use airbnb;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    profile_picture VARCHAR(255),
    is_host BOOLEAN DEFAULT FALSE,
    account_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE accommodations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    price_per_night DECIMAL(10, 2) NOT NULL,
    num_bedrooms INT NOT NULL,
    num_bathrooms INT NOT NULL,
    max_guests INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    host_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id)
);
CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    guest_id INT,
    accommodation_id INT,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    booking_made_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guest_id) REFERENCES users(id),
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id)
);
CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reviewer_id INT,
    accommodation_id INT,
    rating INT NOT NULL,
    comment TEXT,
    review_made_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reviewer_id) REFERENCES users(id),
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id)
);
CREATE TABLE amenities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE accommodation_amenities (
    accommodation_id INT,
    amenity_id INT,
    PRIMARY KEY (accommodation_id, amenity_id),
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
CREATE TABLE hosts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    about_me TEXT,
    response_time_hours INT,
    response_rate DECIMAL(5, 2),
    host_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
show TABLES;
select * from reviews;

show tables;



-- Insert data into `users` table
INSERT INTO users (username, email, password, phone_number, profile_picture, is_host, account_created_at) VALUES
('john_doe', 'john.doe@example.com', 'password123', '123-456-7890', 'profile1.jpg', TRUE, '2024-06-24 12:00:00'),
('jane_smith', 'jane.smith@example.com', 'password456', '987-654-3210', 'profile2.jpg', FALSE, '2024-06-23 10:30:00'),
('michael_brown', 'michael.brown@example.com', 'password789', '456-789-0123', 'profile3.jpg', TRUE, '2024-06-22 09:15:00'),
('susan_jones', 'susan.jones@example.com', 'passwordabc', '789-012-3456', 'profile4.jpg', FALSE, '2024-06-21 08:00:00'),
('david_clark', 'david.clark@example.com', 'passwordxyz', '234-567-8901', 'profile5.jpg', TRUE, '2024-06-20 07:00:00'),
('emma_garcia', 'emma.garcia@example.com', 'password456', '456-789-0123', 'profile6.jpg', FALSE, '2024-06-19 06:00:00'),
('william_wilson', 'william.wilson@example.com', 'password789', '678-901-2345', 'profile7.jpg', TRUE, '2024-06-18 05:00:00');

-- Insert data into `accommodations` table
INSERT INTO accommodations (title, description, city, country, address, price_per_night, num_bedrooms, num_bathrooms, max_guests, is_active, host_id, created_at) VALUES
('Cozy Apartment in Downtown', 'A cozy apartment with great views.', 'New York City', 'USA', '123 Main St, Apt 101', 150.00, 2, 1, 4, TRUE, 1, '2024-06-24 14:00:00'),
('Spacious Villa with Pool', 'Luxury villa with private pool and garden.', 'Los Angeles', 'USA', '456 Elm St', 500.00, 4, 3, 8, TRUE, 3, '2024-06-23 13:00:00'),
('Modern Loft in Arts District', 'Modern loft near art galleries and cafes.', 'San Francisco', 'USA', '789 Maple Ave, Loft 5B', 200.00, 1, 1, 2, TRUE, 2, '2024-06-22 12:00:00'),
('Seaside Cottage Retreat', 'Charming cottage by the beach.', 'Miami', 'USA', '101 Ocean Blvd', 180.00, 3, 2, 6, TRUE, 5, '2024-06-21 11:00:00'),
('Rustic Cabin in the Woods', 'Quiet cabin nestled in the forest.', 'Seattle', 'USA', '234 Forest Dr', 120.00, 2, 1, 4, TRUE, 4, '2024-06-20 10:00:00'),
('Luxury Penthouse Suite', 'Elegant penthouse with panoramic city views.', 'Chicago', 'USA', '567 Skyline Ave, Penthouse 10', 800.00, 3, 2, 6, TRUE, 1, '2024-06-19 09:00:00'),
('Historic Mansion', 'Stately mansion with beautiful gardens.', 'Boston', 'USA', '890 Garden Way', 700.00, 5, 4, 10, TRUE, 3, '2024-06-18 08:00:00');

-- Insert data into `bookings` table
INSERT INTO bookings (guest_id, accommodation_id, check_in_date, check_out_date, total_price, is_paid, booking_made_at) VALUES
(1, 2, '2024-07-01', '2024-07-05', 2000.00, TRUE, '2024-06-24 16:00:00'),
(2, 3, '2024-07-02', '2024-07-07', 1000.00, TRUE, '2024-06-23 15:00:00'),
(3, 1, '2024-07-03', '2024-07-08', 750.00, FALSE, '2024-06-22 14:00:00'),
(4, 5, '2024-07-04', '2024-07-09', 900.00, TRUE, '2024-06-21 13:00:00'),
(5, 4, '2024-07-05', '2024-07-10', 1200.00, FALSE, '2024-06-20 12:00:00'),
(1, 7, '2024-07-06', '2024-07-11', 1400.00, TRUE, '2024-06-19 11:00:00'),
(3, 6, '2024-07-07', '2024-07-12', 1600.00, TRUE, '2024-06-18 10:00:00');

-- Insert data into `reviews` table
INSERT INTO reviews (reviewer_id, accommodation_id, rating, comment, review_made_at) VALUES
(1, 2, 4, 'Great location and amenities.', '2024-06-24 18:00:00'),
(2, 3, 5, 'Beautiful view from the loft!', '2024-06-23 17:00:00'),
(3, 1, 3, 'Cozy but could use some updates.', '2024-06-22 16:00:00'),
(4, 5, 4, 'Perfect for a quiet getaway.', '2024-06-21 15:00:00'),
(5, 4, 5, 'Absolutely loved the cabin!', '2024-06-20 14:00:00'),
(1, 7, 4, 'Historic charm with modern comforts.', '2024-06-19 13:00:00'),
(3, 6, 4, 'Luxury at its finest.', '2024-06-18 12:00:00');

-- Insert data into `amenities` table
INSERT INTO amenities (name) VALUES
('WiFi'),
('Kitchen'),
('Air Conditioning'),
('Heating'),
('Pool'),
('Gym'),
('Parking');

-- Insert data into `accommodation_amenities` table
INSERT INTO accommodation_amenities (accommodation_id, amenity_id) VALUES
(1, 1),
(1, 2),
(1, 4),
(2, 3),
(2, 5),
(3, 1),
(3, 2),
(4, 4),
(5, 1),
(6, 3),
(7, 5),
(8, 2),
(8, 6),
(9, 1),
(9, 5);

-- Insert data into `hosts` table
INSERT INTO hosts (user_id, about_me, response_time_hours, response_rate, host_created_at) VALUES
(1, 'Experienced host in NYC, happy to provide local tips!', 2, 95.5, '2024-06-24 20:00:00'),
(2, 'Passionate about art and culture, available to help guests.', 3, 88.2, '2024-06-23 19:00:00'),
(3, 'Luxury property management with attention to detail.', 1, 100.0, '2024-06-22 18:00:00'),
(4, 'Nature lover who enjoys sharing the beauty of the woods.', 4, 75.0, '2024-06-21 17:00:00'),
(5, 'Beach enthusiast ready to create memorable experiences.', 2, 92.3, '2024-06-20 16:00:00'),
(6, 'Experienced in managing properties in urban settings.', 3, 85.7, '2024-06-19 15:00:00'),
(7, 'Passionate about historic homes and their stories.', 1, 98.9, '2024-06-18 14:00:00');
select * from accommodations;
show tables;
select * from accommodation_amenities;
drop table accommodation_amenities;
