CREATE TABLE LE_Header (
    LEName varchar(50) NOT NULL,
    WellName varchar(50) NOT NULL,
    CorpID varchar(25) NOT NULL,
    Wedge varchar(35) NOT NULL,
	LE_Date datetime NOT NULL,
	ForecastMMBOED real,
	Update_Date datetime NOT NULL,
	Update_User varchar(50) NOT NULL
    PRIMARY KEY (CorpID, Wedge,LE_Date)
);


Create Table LE_Data (
	HeaderName varchar(50) NOT NULL,
	CorpID varchar(25) NOT NULL,
	Date_Key datetime NOT NULL,
	Gas_Production real NOT NULL,
	Oil_Production real,
	Water_Production real,
	Update_Date datetime NOT NULL,
	Update_User varchar(50) NOT NULL
	PRIMARY KEY(HeaderName, CorpID, Date_Key)
);

create table Forecast_Header (
	WellName varchar(25) NOT NULL,
	CorpID varchar(25) NOT NULL,
	ForecastName varchar(50) NOT NULL,
	GFOz bit default 0,
	GFOzYear datetime,
	Aries_ScenarioID varchar(100),
	DCA_b real,
	DCA_Di real,
	DCA_qi real,
	ForecastMMBOED real,
	Update_Date datetime NOT NULL, 
	Update_User varchar(50)
	PRIMARY KEY (CorpID, GFOz)
);

create table Forecast_Data (
	HeaderName varchar(50) NOT NULL,
	CorpID varchar(50) NOT NULL,
	Date_Key datetime NOT NULL,
	Gas_Production real,
	Oil_Production real,
	Water_Production real,
	Update_Date datetime,
	Update_User varchar(50)
	PRIMARY KEY (HeaderName, CorpID, Date_Key)
);

create table LE_Summary (
	SummaryName varchar(50) NOT NULL,
	WellName varchar(50) NOT NULL,
	CorpID varchar(25) NOT NULL,
	Area varchar(50),
	Wedge varchar(20),
	Midstream varchar(100),
	Reason varchar(255),
	Comments varchar(255),
	SummaryDate datetime,
	FirstOfMonthLEName varchar(50),
	AnnualLEName varchar(50),
	WeeklyLEName varchar(50),
	LEName varchar(50),
	MonthlyVariance real,
	WeeklyVariance real,
	AnnualVariance real,
	Update_Date datetime,
	Update_User varchar(50)
	PRIMARY KEY (SummaryName, CorpID)
);


create table NettingValues (
	WellName varchar(50),
	CorpID varchar(20),
	NettingValue real,
	Update_Date datetime,
	Update_User varchar(50)
	PRIMARY KEY (CorpID)
);

create table Frac_Hit_Scalars (
	LEName varchar(50),
	CorpID varchar(20),
	Date_Key datetime,
	ScalarValue int
	PRIMARY KEY (LEName, CorpID, Date_Key)
);