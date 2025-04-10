CREATE DATABASE smartcmms;
USE smartcmms;

-- TODO: Informacja, do którego budynku przypisany jest protokół

CREATE TABLE IF NOT EXISTS users (
	id int NOT NULL,
	name varchar(128) NOT NULL,
	surname varchar(128) NOT NULL,
	email varchar(128) NOT NULL,
	hashed_pass varchar(64) NOT NULL,
	role int NOT NULL, -- bit 0 - osoba zewnętrzna, bit 1 - technik, bit 2 - kierownik budynku, bit 3 - administrator
	state int NOT NULL, -- bit 0 - czy konto jest usunięte (fałsz - aktywne, prawda - usunięte)

	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols (
	id varchar(16) NOT NULL, -- np. 1.1.1 4.2.5
	name varchar(256) NOT NULL,

	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols_fields ( -- Pole do zaptaszkowania na protokole
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	name varchar(256) NOT NULL,

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols_filled ( -- Protokoły wypełniane/wypełnione przez technika
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	user_id int NOT NULL, -- osoba, która wypełniła protokół
	state int NOT NULL, -- bit 0 - czy w pełni wypełniony, bit 1 - czy podpisany przez technika, bit 2 - czy podpisany przez odbiorcę

	notes varchar(4096) NOT NULL, -- notatki, które może dopisać technik. Wyniki pomiarów ilościowych itp.

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols_filled_fields (
	id int NOT NULL,
	protocol_filled_id int NOT NULL,
	field_id int NOT NULL,
	value boolean NOT NULL, -- 0 nie ma ptaszka; 1 jest ptaszek

	FOREIGN KEY (protocol_filled_id) REFERENCES protocols_filled(id),
	FOREIGN KEY (field_id) REFERENCES protocols_fields(id),
	PRIMARY KEY (id)

	-- TODO: CONSTRAINT żeby field_id i protocol_filled_id dotyczyło tego samego protokołu
	-- CONSTRAINT CHK_protocols_filled_fields CHECK ()
);

CREATE TABLE IF NOT EXISTS protocol_sign (
	id int NOT NULL,
	protocol_filled_id int NOT NULL,

	-- TODO: Jakieś dodatkowe dane o podpisie

	FOREIGN KEY (protocol_filled_id) REFERENCES protocols_filled(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS schedules (
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	user_id int NOT NULL, -- Technik, któremu wyświetli się powiadomienie, że musi wypełnić nowy protokół
	week_interval int NOT NULL, -- Co ile tygodni będzie trzeba wypełnić ten protokół

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	PRIMARY KEY (id)
);
