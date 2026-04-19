-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Front Desk Staff'
);

-- Tenants table
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    occupation TEXT,
    ni_number TEXT,
    lease_period TEXT,
    reference TEXT,
    apartment_requirement TEXT
);

-- Apartments table
CREATE TABLE IF NOT EXISTS apartments (
    apartment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    apartment_type TEXT,
    num_rooms INTEGER,
    floor_number INTEGER,
    monthly_rent REAL,
    occupancy_status TEXT DEFAULT 'Vacant',
    notes TEXT
);

-- Leases table
CREATE TABLE IF NOT EXISTS leases (
    lease_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL,
    apartment_id INTEGER NOT NULL,
    start_date TEXT,
    end_date TEXT,
    monthly_rent REAL,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id)
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL,
    apartment_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    due_date TEXT,
    payment_date TEXT,
    status TEXT DEFAULT 'Pending',
    invoice_number TEXT,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id)
);

-- Maintenance requests table
CREATE TABLE IF NOT EXISTS maintenance_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    apartment_id INTEGER NOT NULL,
    tenant_id INTEGER,
    description TEXT NOT NULL,
    priority TEXT DEFAULT 'Medium',
    status TEXT DEFAULT 'Reported',
    assigned_worker TEXT DEFAULT 'Unassigned',
    cost REAL DEFAULT 0,
    time_hours REAL DEFAULT 0,
    created_date TEXT,
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);