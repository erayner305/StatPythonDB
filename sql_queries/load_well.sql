LOAD DATA LOCAL INFILE 'C:/StatPythonDB/StatPythonDB/wells.csv'
INTO TABLE gwstats.well
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;