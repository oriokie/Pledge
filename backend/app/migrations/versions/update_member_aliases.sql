-- Update member table to make alias fields optional
ALTER TABLE members
ADD COLUMN IF NOT EXISTS alias1 VARCHAR,
ADD COLUMN IF NOT EXISTS alias2 VARCHAR;

-- Update existing records to set aliases as NULL
UPDATE members SET alias1 = NULL WHERE alias1 = '';
UPDATE members SET alias2 = NULL WHERE alias2 = ''; 