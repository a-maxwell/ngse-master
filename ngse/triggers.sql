CREATE FUNCTION add_blank_answers()	RETURNS trigger AS $add_blank_answers$
	BEGIN
		-- Check if user has a form or user_type_id is 3, 4 or 5
		IF NEW.user_type_id > 2 THEN
			RETURN NEW
		END IF;

		RETURN NEW;
	END;
$add_blank_answers$;

CREATE TRIGGER set_blank_answers
AFTER INSERT ON users
	FOR EACH ROW EXECUTE PROCEDURE add_blank_answers();