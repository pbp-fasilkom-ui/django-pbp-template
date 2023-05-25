-- TRIGGER CHECK TIDAK ADA TIM DENGAN NAMA UNIV DAN NAMA TIM YANG SAMA 
-- AGAR HUBUNGAN 1-1 MANAJER DAN TIM DAPAT TERJAGA
CREATE OR REPLACE FUNCTION check_team_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM tim
        WHERE nama_tim = NEW.nama_tim
    ) THEN
        RAISE EXCEPTION 'Team with the same name already exists';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger on the Tim table
CREATE TRIGGER check_team_duplicate_trigger
BEFORE INSERT ON tim
FOR EACH ROW
EXECUTE FUNCTION check_team_duplicate();
