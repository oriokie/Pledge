-- Drop existing table and its dependencies
DROP TABLE IF EXISTS members CASCADE;

-- Recreate the members table with the correct schema
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    phone VARCHAR,
    email VARCHAR,
    member_code VARCHAR,
    alias1 VARCHAR,
    alias2 VARCHAR,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by_id INTEGER REFERENCES users(id)
);

-- Create indexes
CREATE INDEX idx_members_full_name ON members(full_name);
CREATE INDEX idx_members_phone ON members(phone);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_members_member_code ON members(member_code);
CREATE INDEX idx_members_created_by_id ON members(created_by_id);

-- Add unique constraints
ALTER TABLE members
ADD CONSTRAINT unique_member_phone UNIQUE (phone),
ADD CONSTRAINT unique_member_email UNIQUE (email),
ADD CONSTRAINT unique_member_code UNIQUE (member_code); 