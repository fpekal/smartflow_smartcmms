CREATE DATABASE smartcmms;
USE smartcmms;

-- TODO: Informacja, do którego budynku przypisany jest protokół

CREATE TABLE IF NOT EXISTS users (
	id int NOT NULL,
	name varchar(128) NOT NULL,
	surname varchar(128) NOT NULL,
	email varchar(128) NOT NULL,
	hashed_pass varchar(64) NOT NULL,
	role int NOT NULL, -- 0 osoba zewnętrzna; 1 technik; 2 kierownik budynku; 3 administrator
	state int NOT NULL, -- 0 aktywne konto; 1 usunięte konto

	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users_change (
	id int NOT NULL,
	user_id int NOT NULL,
	new_role int, -- Nowa wartość, która będzie wpisana w pole `role` w tabeli `users`; NULL jeżeli bez zmian
	new_state int, -- Nowa wartość, która będzie wpisana w pole `state` w tabeli `users`; NULL jeżeli bez zmian
	commit_date date NOT NULL, -- Kiedy ta zmiana powinna zostać wdrożona do systemu

	FOREIGN KEY (user_id) REFERENCES users(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols (
	id varchar(16) NOT NULL, -- np. 1.1.1 4.2.5
	name varchar(256) NOT NULL,
	author_id int NOT NULL, -- Osoba, która utworzyła dany protokół
	state int NOT NULL, -- bit 0 - czy protokół jest obowiązujący (prawda - obowiązuje; fałsz - nieobowiązuje)

	FOREIGN KEY (author_id) REFERENCES users(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols_change (
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	new_state int, -- Nowa wartość, która będzie wpisana w pole `state` w tabeli `protocols`; NULL jeżeli bez zmian
	commit_date date NOT NULL, -- Kiedy ta zmiana powinna zostać wdrożona do systemu

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols_fields ( -- Pole do zaptaszkowania na protokole
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	name varchar(256) NOT NULL,

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS protocols_filled ( -- Protokoły wypeniane/wypełnione przez technika
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	user_id int NOT NULL, -- osoba, która wypełniła protokół
	state int NOT NULL, -- 0 niewypełniony do końca, nadal można edytować; 1 wypełniony, brak możliwości edycji; 2 wypełniony i podpisany przez technika i odbiorcę
	-- NOTE: Czy na pewno w stanie 1 nie powinno być możliwości edycji? Co, jak technik chce coś poprawić?

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
