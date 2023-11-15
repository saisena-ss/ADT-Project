-- Author Aditya Prajapati
drop database if exists datajobnexus;
CREATE DATABASE datajobnexus;
use datajobnexus;
drop table if exists job_postings;
drop table if exists job;
drop table if exists CompanyCompetitors;
drop table if exists Competitor;
drop table if exists company;

CREATE TABLE company (
	company_id int auto_increment PRIMARY KEY,
    c_name varchar(255) not null,
    founded year,
    headquarters varchar(255),
    size varchar(50),
    revenue varchar(100),
    ownership_type varchar(255),
    industry varchar(255),
    sector varchar(255)
    );
    
CREATE TABLE job (
	job_id int auto_increment PRIMARY KEY,
    job_title varchar(255) not null,
    min_sal int,
    max_sal int,
    avg_rating DECIMAL(2,1));

CREATE TABLE job_postings(
	job_id int,
    job_title varchar(255) not null,
    company_id int,
    job_description text,
    location varchar(255),
    min_sal int,
    max_sal int,
    easy_apply int,
    FOREIGN KEY (job_id) REFERENCES job(job_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id));

CREATE TABLE Competitor (
    CompetitorID INT AUTO_INCREMENT PRIMARY KEY,
    comp_name VARCHAR(255) NOT NULL
);

CREATE TABLE CompanyCompetitors (
    company_id INT,
    CompetitorID INT,
    PRIMARY KEY (company_id, CompetitorID),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (CompetitorID) REFERENCES Competitor(CompetitorID)
);


-- Author Sai Sena
-- staging table
drop table if exists StagingTable;
CREATE TABLE StagingTable (
    job_title VARCHAR(255),
    min_sal INT,
    max_sal INT,
    job_description TEXT,
    rating DECIMAL(2, 1),
    c_name VARCHAR(255),
    location VARCHAR(255),
    headquarters VARCHAR(255),
    size VARCHAR(255),
    founded year,
    ownership_type VARCHAR(255),
    industry VARCHAR(255),
    sector VARCHAR(255),
    revenue VARCHAR(255),
    competitors TEXT,
    easy_apply int
);

SET GLOBAL local_infile=ON;

LOAD DATA LOCAL INFILE 'C:/Users/saise/OneDrive - Indiana University/D532 - ADT/Project/DataAnalyst_FINAL.csv'
INTO TABLE StagingTable
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES; 

SET SQL_SAFE_UPDATES = 0;

update stagingtable set sector='Information Technology',
size= '1 to 50 employees',
ownership_type = 'Company - Private',
industry='IT Services',
revenue='Unknown / Non-Applicable'
where c_name like 'Eleven Recr%';

-- Normalize data
-- Insert data into Company table
INSERT INTO company (c_name, founded, headquarters, size, revenue, ownership_type, industry,sector)
SELECT DISTINCT c_name, founded, headquarters, Size, revenue, ownership_type, industry,sector
FROM StagingTable
WHERE c_name IS NOT NULL;

update company set founded=null where founded=0;

-- Insert data into Job table
INSERT INTO Job (job_title, min_sal, max_sal, avg_rating)
SELECT job_title, min(min_sal), max(max_sal), max(rating)
FROM StagingTable
WHERE job_title IS NOT NULL
group by 1;


-- Insert data into Job Postings table
INSERT INTO job_postings (job_id, job_title, company_id, job_description,location,min_sal, max_sal, easy_apply)
SELECT j.job_id, st.job_title, c.company_id, st.job_description, st.location, st.min_sal, st.max_sal,st.easy_apply
FROM StagingTable st join job j on st.job_title = j.job_title
join company c on st.c_name = c.c_name
WHERE st.job_title IS NOT NULL;


drop table if exists numbers;
CREATE TABLE Numbers (n INT PRIMARY KEY);

INSERT INTO Numbers (n)
SELECT a.N + b.N * 10 + 1 as n
FROM 
	(SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
	(SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b
ORDER BY n;

-- Step 1: Insert competitors into the Competitor table
INSERT INTO Competitor (comp_name)
SELECT DISTINCT SUBSTRING_INDEX(SUBSTRING_INDEX(t.competitors, ',', n.n), ',', -1) as competitor
FROM StagingTable t
JOIN Numbers n ON CHAR_LENGTH(t.competitors) - CHAR_LENGTH(REPLACE(t.competitors, ',', '')) >= n.n - 1
WHERE t.competitors <> '-1'
AND SUBSTRING_INDEX(SUBSTRING_INDEX(t.competitors, ',', n.n), ',', -1) NOT IN (SELECT comp_name FROM Competitor);

-- Step 2: Insert relations into CompanyCompetitors table
INSERT INTO CompanyCompetitors (company_id, CompetitorID)
SELECT DISTINCT c.company_id, comp.CompetitorID
FROM (select DISTINCT c_name, SUBSTRING_INDEX(SUBSTRING_INDEX(competitors, ',', n.n), ',', -1) as competitor 
		from StagingTable join numbers n ON CHAR_LENGTH(competitors) - CHAR_LENGTH(REPLACE(competitors, ',', '')) >= n.n - 1
        where competitors <> '-1' group by 1,2) t
JOIN Company c ON t.c_name = c.c_name
JOIN Competitor comp ON t.competitor = comp.comp_name
ON DUPLICATE KEY UPDATE company_id = VALUES(company_id), CompetitorID = VALUES(CompetitorID);

drop table stagingtable, numbers;