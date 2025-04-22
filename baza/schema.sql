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
	fields json NOT NULL, -- edytowalne pola w protokole zapisane jako json

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

CREATE TABLE IF NOT EXISTS protocols_filled ( -- Protokoły wypełniane/wypełnione przez technika
	id int NOT NULL,
	protocol_id varchar(16) NOT NULL,
	user_id int NOT NULL, -- osoba, która wypełniła protokół
	state int NOT NULL, -- bit 0 - czy w pełni wypełniony, bit 1 - czy podpisany przez technika, bit 2 - czy podpisany przez odbiorcę

	fields json NOT NULL, -- wypełnione pola, razem z notatkami

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	PRIMARY KEY (id)
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
	next date NOT NULL, -- Data następnego cyklicznego wypełniania protokołu

	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	PRIMARY KEY (id)
);
