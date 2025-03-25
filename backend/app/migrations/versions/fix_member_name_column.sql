-- First, check if the name column exists and has data
DO $$ 
BEGIN
    -- If name column exists and full_name is empty, copy data from name to full_name
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'members' AND column_name = 'name') THEN
        UPDATE members 
        SET full_name = name 
        WHERE full_name IS NULL OR full_name = '';
    END IF;
END $$;

-- Drop the name column if it exists
ALTER TABLE members
DROP COLUMN IF EXISTS name;

-- Ensure full_name is NOT NULL
ALTER TABLE members
ALTER COLUMN full_name SET NOT NULL;

-- Create index on full_name if it doesn't exist
CREATE INDEX IF NOT EXISTS idx_members_full_name ON members(full_name); 