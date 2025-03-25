-- Add full_name column to members table
ALTER TABLE members
ADD COLUMN IF NOT EXISTS full_name VARCHAR NOT NULL DEFAULT '';

-- Update existing records to set full_name based on available data
UPDATE members 
SET full_name = COALESCE(name, 'Unknown Member')
WHERE full_name = ''; 