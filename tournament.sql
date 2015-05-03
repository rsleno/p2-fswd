-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament

CREATE TABLE IF NOT EXISTS players (
	id serial PRIMARY KEY,
	name text 
);

CREATE TABLE IF NOT EXISTS matches (
	id serial PRIMARY KEY,
	winner integer REFERENCES players (id),
	loser integer REFERENCES players (id)
);

CREATE VIEW scores AS
	SELECT players.id, players.name, (SELECT count(matches.winner) FROM matches WHERE players.id = matches.winner) AS wins, 
	(SELECT count(*) FROM matches WHERE players.id = matches.winner or players.id = matches.loser) AS num FROM matches
	RIGHT JOIN players ON matches.winner=players.id OR matches.loser=players.id GROUP BY players.id ORDER BY wins desc
;