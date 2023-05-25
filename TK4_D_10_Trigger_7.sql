-- TRIGGER BUAT CEK PELATIH WAKTU ASSIGN PELATIH BARU
CREATE OR REPLACE FUNCTION check_coach_specialization()
RETURNS TRIGGER AS $$
DECLARE
    coach_count INTEGER;
    specialization_count INTEGER;
BEGIN
    -- Skip validation for team "tim_ghaib"
    IF NEW.Nama_Tim = 'tim_ghaib' THEN
        RETURN NEW;
    END IF;
    
    -- Count the number of coaches for the team
    SELECT COUNT(*) INTO coach_count
    FROM Pelatih
    WHERE Nama_Tim = NEW.Nama_Tim;

    IF coach_count = 0 THEN
        -- If no coach exists, allow the registration
        RETURN NEW;
    ELSIF coach_count = 1 THEN
        -- Check if the new coach has a different specialization
        SELECT COUNT(*) INTO specialization_count
        FROM Spesialisasi_Pelatih
        WHERE ID_Pelatih = NEW.ID_Pelatih
          AND Spesialisasi NOT IN (
              SELECT Spesialisasi
              FROM Spesialisasi_Pelatih
              WHERE ID_Pelatih IN (
                  SELECT ID_Pelatih
                  FROM Pelatih
                  WHERE Nama_Tim = NEW.Nama_Tim
              )
          );

        IF specialization_count > 0 THEN
            -- New coach has a different specialization, allow the registration
            RETURN NEW;
        ELSE
            -- New coach has the same specialization, raise an error
            RAISE EXCEPTION 'Error: The coach must have a different specialization.';
        END IF;
    ELSE
        -- Maximum number of coaches (2) reached, raise an error
        RAISE EXCEPTION 'Error: The team can have a maximum of 2 coaches.';
    END IF;

    RETURN NULL;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_coach_specialization_trigger
BEFORE INSERT ON Pelatih
FOR EACH ROW
EXECUTE FUNCTION check_coach_specialization();
