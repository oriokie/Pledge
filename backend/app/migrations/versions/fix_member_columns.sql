-- Drop existing constraints if they exist
ALTER TABLE members
DROP CONSTRAINT IF EXISTS unique_member_phone,
DROP CONSTRAINT IF EXISTS unique_member_email,
DROP CONSTRAINT IF EXISTS unique_member_code;

-- Drop existing columns if they exist
ALTER TABLE members
DROP COLUMN IF EXISTS phone,
DROP COLUMN IF EXISTS email,
DROP COLUMN IF EXISTS member_code,
DROP COLUMN IF EXISTS alias1,
DROP COLUMN IF EXISTS alias2,
DROP COLUMN IF EXISTS full_name;

-- Add columns with correct data types and constraints
ALTER TABLE members
ADD COLUMN full_name VARCHAR NOT NULL,
ADD COLUMN phone VARCHAR,
ADD COLUMN email VARCHAR,
ADD COLUMN member_code VARCHAR,
ADD COLUMN alias1 VARCHAR,
ADD COLUMN alias2 VARCHAR;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone);
CREATE INDEX IF NOT EXISTS idx_members_email ON members(email);
CREATE INDEX IF NOT EXISTS idx_members_member_code ON members(member_code);
CREATE INDEX IF NOT EXISTS idx_members_full_name ON members(full_name);

-- Add unique constraints
ALTER TABLE members
ADD CONSTRAINT unique_member_phone UNIQUE (phone),
ADD CONSTRAINT unique_member_email UNIQUE (email),
ADD CONSTRAINT unique_member_code UNIQUE (member_code); 