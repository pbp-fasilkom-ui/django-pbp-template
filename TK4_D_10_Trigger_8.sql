-- TRIGGER UNTUK MENON-AKTIFKAN CAPTAIN YANG LAMA, DAN ASSIGN KAPTEN BARU
CREATE OR REPLACE FUNCTION update_captain()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the team already has a captain
    IF EXISTS (
        SELECT 1
        FROM Pemain
        WHERE Nama_Tim = NEW.Nama_Tim
          AND Is_Captain = TRUE
    ) THEN
        -- If the team already has a captain, remove the existing captain
        UPDATE Pemain
        SET Is_Captain = FALSE
        WHERE Nama_Tim = NEW.Nama_Tim
          AND Is_Captain = TRUE;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pendaftaran_pemain_kapten
BEFORE INSERT OR UPDATE ON Pemain
FOR EACH ROW
WHEN (NEW.Is_Captain = TRUE)
EXECUTE FUNCTION update_captain();