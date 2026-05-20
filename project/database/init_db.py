from database.connection import Connection


#Creating the Schemas needed for the DB

def init_db():
    conn = Connection.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE SCHEMA IF NOT EXISTS inventory;
    CREATE SCHEMA IF NOT EXISTS sales;
    CREATE SCHEMA IF NOT EXISTS purchases;
    """)

    # Creating the tables needed for the DB
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory.categories (  
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        active BOOLEAN DEFAULT TRUE
    );
    
    CREATE TABLE IF NOT EXISTS inventory.articles (
        id SERIAL PRIMARY KEY,
        bar_code VARCHAR(100) UNIQUE NOT NULL,
        description VARCHAR(100) NOT NULL,
        purchase_price NUMERIC(10,2) NOT NULL CHECK (purchase_price >= 0),
        retail_price NUMERIC(10,2) NOT NULL CHECK (retail_price >= 0),
        wholesale_price NUMERIC(10,2) NOT NULL CHECK (wholesale_price >= 0),
        stock NUMERIC(10,3) NOT NULL DEFAULT 0 CHECK (stock >= 0),
        active BOOLEAN DEFAULT TRUE,
        category_id INTEGER NOT NULL
            REFERENCES inventory.categories(id)
    );
    
    CREATE TABLE IF NOT EXISTS inventory.stock_movements ( 
        id SERIAL PRIMARY KEY,
        id_article INTEGER NOT NULL
            REFERENCES inventory.articles(id),
        type VARCHAR(20) NOT NULL CHECK (type in ('VENTA', 'COMPRA', 'AJUSTE')) ,
        quantity NUMERIC(10,3) NOT NULL CHECK (quantity > 0),
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id_reference INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS sales.sales ( 
        id SERIAL PRIMARY KEY,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total NUMERIC(12,2) NOT NULL,
        payment_method VARCHAR(50) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS sales.details_sales ( 
        id SERIAL PRIMARY KEY,
        id_sale INTEGER NOT NULL
            REFERENCES sales.sales(id) ON DELETE CASCADE,
        id_article INTEGER NOT NULL
            REFERENCES inventory.articles(id),
        quantity NUMERIC(10,3) NOT NULL CHECK (quantity > 0),
        unit_price NUMERIC(10,2) NOT NULL,
        subtotal NUMERIC(12,2) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS purchases.suppliers ( 
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL, 
        telephone_number VARCHAR(100),
        active BOOLEAN DEFAULT TRUE
    );
    
    CREATE TABLE IF NOT EXISTS purchases.purchases ( 
        id SERIAL PRIMARY KEY,
        id_supplier INTEGER
            REFERENCES purchases.suppliers(id),
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total NUMERIC(12,2) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS purchases.details_purchases ( 
        id SERIAL PRIMARY KEY,
        id_purchase INTEGER NOT NULL
            REFERENCES purchases.purchases(id) ON DELETE CASCADE,
        id_article INTEGER NOT NULL
            REFERENCES inventory.articles(id),
        quantity NUMERIC(10,3) NOT NULL CHECK (quantity > 0),
        unit_price NUMERIC(10,2) NOT NULL,
        subtotal NUMERIC(12,2) NOT NULL
    );
    
    """)

    conn.commit()
    cursor.close()
    Connection.release_connections(conn)
