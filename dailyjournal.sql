CREATE TABLE `Mood` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`    TEXT NOT NULL
);

CREATE TABLE `Entry` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
	`date`	INTEGER NOT NULL,
	`moodId`	INTEGER NOT NULL,
     FOREIGN KEY (moodId) REFERENCES Mood(id)
);

SELECT * FROM Entry
SELECT * FROM Mood

INSERT INTO `Mood` VALUES (null, 'Good');
INSERT INTO `Mood` VALUES (null, 'Better');
INSERT INTO `Mood` VALUES (null, 'Best');


INSERT INTO `Entry` VALUES (null, 'Javascript', 'i miss it', 19208473625, 2);
INSERT INTO `Entry` VALUES (null, 'REACT', 'i miss it', 19208473625, 3);
INSERT INTO `Entry` VALUES (null, 'Python', 'building those connections', 19208473625, 1);

DROP TABLE NSS

SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM entry e
        WHERE e.entry LIKE '%b%'

SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId,
            m.label
        FROM entry e
        JOIN mood m
            ON m.id = e.moodId