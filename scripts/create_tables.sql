CREATE TABLE IF NOT EXISTS User
(
    id INT NOT NULL UNIQUE AUTO_INCREMENT,
    user_id VARCHAR(250) NOT NULL,
    date DATETIME NOT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Playlist
(
    id int NOT NULL unique AUTO_INCREMENT,
    user_id INT NOT null REFERENCES user(id),
    playlist_id VARCHAR(250),
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Track
(
    id INT NOT NULL AUTO_INCREMENT,
	track_id varchar(250) not null,
	playlist_id INT not null references Playlist(id),
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Reaction
(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL references user(id),
    track_id varchar(250) NOT NULL,
    hrv LONGTEXT NOT NULL,
    evaluation bool not null,
    user_evaluation bool not null,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE Reaction
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
    
ALTER TABLE Playlist
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;

ALTER TABLE Track ADD FOREIGN KEY (playlist_id)
REFERENCES Playlist(id);