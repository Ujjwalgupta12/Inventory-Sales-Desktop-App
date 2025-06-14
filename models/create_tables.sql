CREATE TABLE IF NOT EXISTS operators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    sku_id TEXT,
    category TEXT,
    subcategory TEXT,
    product_image TEXT,
    product_name TEXT,
    description TEXT,
    tax REAL,
    price REAL,
    default_unit TEXT
);

CREATE TABLE IF NOT EXISTS goods_receiving (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    supplier_name TEXT,
    quantity REAL,
    unit TEXT,
    rate_per_unit REAL,
    total_rate REAL,
    tax REAL
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    customer_name TEXT,
    quantity REAL,
    unit TEXT,
    rate_per_unit REAL,
    total_rate REAL,
    tax REAL
);
