CREATE TABLE gwstats.data (
  wellID INT NOT NULL,
  constituentID INT NOT NULL,
  mdl DECIMAL(5, 4),
  pql DECIMAL(5, 4),
  observed INT,
  sampleDate DATE,
  FOREIGN KEY (wellId) REFERENCES well(wellId),
  FOREIGN KEY (constituentId) REFERENCES constituent(constituentId)
);