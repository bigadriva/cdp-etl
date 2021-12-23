DROP SCHEMA IF EXISTS cdp CASCADE;

CREATE SCHEMA cdp;

-- Cliente da driva
CREATE TABLE cdp.company (
    cnpj VARCHAR(14),
    name VARCHAR(100),
    PRIMARY KEY(cnpj)
);

CREATE TABLE cdp.product (
    internal_id VARCHAR(100),
    name VARCHAR(100),
    type VARCHAR(100),
    PRIMARY KEY(internal_id)
);

CREATE TABLE cdp.acting_region (
    id VARCHAR(20),
    city VARCHAR(100),
    address VARCHAR(100),
    neighborhood VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE cdp.salesperson (
    internal_id VARCHAR(100),
    name VARCHAR(100),
    company_cnpj VARCHAR(14),
    PRIMARY KEY(internal_id, name),
    FOREIGN KEY(company_cnpj) REFERENCES cdp.company(cnpj)
);

-- Cliente da empresa que é cliente da driva.
CREATE TABLE cdp.client (
    cnpj VARCHAR(14),
    name VARCHAR(100),
    acting_region_id VARCHAR(20) NOT NULL,
    PRIMARY KEY(cnpj),
    FOREIGN KEY(acting_region_id) REFERENCES cdp.acting_region(id)
);

CREATE TABLE cdp.sale (
    id VARCHAR(20),
    nf VARCHAR(50),
    total_ammount INTEGER,
    total_value FLOAT,
    date DATE,
    client_cnpj VARCHAR(14),
    product_internal_id VARCHAR(100),
    salesperson_internal_id VARCHAR(100),
    salesperson_name VARCHAR(100),
    PRIMARY KEY(id),
    FOREIGN KEY(client_cnpj) REFERENCES cdp.client(cnpj),
    FOREIGN KEY(product_internal_id) REFERENCES cdp.product(internal_id),
    FOREIGN KEY(salesperson_internal_id, salesperson_name) REFERENCES cdp.salesperson(internal_id, name)
);

-- DBV2
CREATE TABLE cdp.potential_client (
    cnpj VARCHAR(14),
    name VARCHAR(100),
    acting_region_id VARCHAR(20),
    PRIMARY KEY(cnpj),
    FOREIGN KEY(acting_region_id) REFERENCES cdp.acting_region(id)
);

CREATE TABLE cdp.buys_from (
    company_cnpj VARCHAR(14),
    client_cnpj VARCHAR(14),
    PRIMARY KEY(company_cnpj, client_cnpj),
    FOREIGN KEY(company_cnpj) REFERENCES cdp.company(cnpj),
    FOREIGN KEY(client_cnpj) REFERENCES cdp.client(cnpj)
);

CREATE TABLE cdp.sells_to (
    client_cnpj VARCHAR(14),
    salesperson_internal_id VARCHAR(100),
    salesperson_name VARCHAR(100),
    PRIMARY KEY(client_cnpj, salesperson_internal_id),
    FOREIGN KEY(client_cnpj) REFERENCES cdp.client(cnpj),
    FOREIGN KEY(salesperson_internal_id, salesperson_name) REFERENCES cdp.salesperson(internal_id, name)
);

CREATE TABLE cdp.closes_sale (
    salesperson_internal_id VARCHAR(100),
    salesperson_name VARCHAR(100),
    sale_id VARCHAR(20),
    PRIMARY KEY(salesperson_internal_id, salesperson_name, sale_id),
    FOREIGN KEY(salesperson_internal_id, salesperson_name) REFERENCES cdp.salesperson(internal_id, name),
    FOREIGN KEY(sale_id) REFERENCES cdp.sale(id)
);

CREATE TABLE cdp.acts_in (
    salesperson_internal_id VARCHAR(100) NOT NULL,
    salesperson_name VARCHAR(100) NOT NULL,
    acting_region_id VARCHAR(20) NOT NULL,
    PRIMARY KEY(salesperson_internal_id, salesperson_name, acting_region_id),
    FOREIGN KEY(salesperson_internal_id, salesperson_name) REFERENCES cdp.salesperson(internal_id, name),
    FOREIGN KEY(acting_region_id) REFERENCES cdp.acting_region(id)
);

CREATE TABLE cdp.characteristics (
    name_array TEXT[] NOT NULL,
    value_array FLOAT[] NOT NULL,
    order_array INTEGER[] NOT NULL,
    company_cnpj VARCHAR(14) NOT NULL,
    client_cnpj VARCHAR(14) NOT NULL,
    PRIMARY KEY(name_array, value_array),
    FOREIGN KEY(company_cnpj) REFERENCES cdp.company(cnpj),
    FOREIGN KEY(client_cnpj) REFERENCES cdp.client(cnpj)
);

-- DBV2
CREATE TABLE cdp.prospects (
    company_cnpj VARCHAR(14),
    potential_client_cnpj VARCHAR(14),
    PRIMARY KEY(company_cnpj, potential_client_cnpj),
    FOREIGN KEY(company_cnpj) REFERENCES cdp.company(cnpj),
    FOREIGN KEY(potential_client_cnpj) REFERENCES cdp.potential_client(cnpj)
);
