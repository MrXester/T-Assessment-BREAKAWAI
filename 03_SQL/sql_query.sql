--BEGIN create main table --
CREATE TABLE IF NOT EXISTS ProcureToPay (
    CASEID INT,
    STARTTIMESTAMP DATETIME,
    COMPLETETIMESTAMP DATETIME,
    ACTIVITY VARCHAR(50),
    RESOURCE VARCHAR(30),
    ROLE VARCHAR(30),
    INVOICEAMOUNT DECIMAL(30, 2),
    DISCOUNT DECIMAL(30, 2),
    COUNTRY CHAR(3),
    QUARTER CHAR(2),
    WEEK INT,
    FOREIGN KEY (COUNTRY) REFERENCES ISOCodes(Iso3)
);
--END



--BEGIN create iso table --
CREATE TABLE IF NOT EXISTS ISOCodes (
    Iso3 CHAR(3) PRIMARY KEY,
    Country VARCHAR(100)
);
--END



--BEGIN create continents table --
CREATE TABLE IF NOT EXISTS Continents (
    Continent VARCHAR(100),
    Country VARCHAR(100)
);
--END


--BEGIN create phases table --
CREATE TABLE IF NOT EXISTS Phases (
    Phase INT,
    Activity VARCHAR(50)
);
--END


--BEGIN Join Info--
SELECT ProcureToPay.*, ISOView.Continent, Phases.Phase
    FROM ProcureToPay 
    INNER JOIN 
        (
            SELECT ISOCodes.Iso3 AS Iso3, Continents.Continent AS Continent
                FROM ISOCodes 
                INNER JOIN Continents
                ON Continents.Country = ISOCodes.Country
        )AS ISOView
    ON ProcureToPay.COUNTRY = ISOView.Iso3
    INNER JOIN Phases
    ON Phases.Activity = ProcureToPay.ACTIVITY
    ORDER BY ProcureToPay.CASEID;
--END
