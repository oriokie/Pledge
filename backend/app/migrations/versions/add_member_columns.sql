-- Add all missing columns to members table
ALTER TABLE members
ADD COLUMN IF NOT EXISTS phone VARCHAR,
ADD COLUMN IF NOT EXISTS email VARCHAR,
ADD COLUMN IF NOT EXISTS member_code VARCHAR,
ADD COLUMN IF NOT EXISTS alias1 VARCHAR,
ADD COLUMN IF NOT EXISTS alias2 VARCHAR,
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS created_by_id INTEGER REFERENCES users(id);

-- Create indexes for the new columns
CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone);
CREATE INDEX IF NOT EXISTS idx_members_email ON members(email);
CREATE INDEX IF NOT EXISTS idx_members_member_code ON members(member_code);
CREATE INDEX IF NOT EXISTS idx_members_created_by_id ON members(created_by_id);

-- Add unique constraints
ALTER TABLE members
ADD CONSTRAINT unique_member_phone UNIQUE (phone),
ADD CONSTRAINT unique_member_email UNIQUE (email),
ADD CONSTRAINT unique_member_code UNIQUE (member_code); 