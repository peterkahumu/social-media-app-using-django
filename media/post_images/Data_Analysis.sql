USE water_quality;

-- Average contamination level of E. coli across all water sources
SELECT AVG(ContaminationLevel) AS AvgEColiContamination
FROM WaterQuality
WHERE ContaminantType = 'E. coli';

-- Total cases reported for each disease type across all regions
SELECT DiseaseType, SUM(CasesReported) AS TotalCases
FROM HealthIncident
GROUP BY DiseaseType;

-- Number of health incidents reported in each region
SELECT RegionID, COUNT(*) AS NumberOfIncidents
FROM HealthIncident
GROUP BY RegionID;

-- Average capacity of treatment plants and filters
SELECT FacilityType, AVG(Capacity) AS AvgCapacity
FROM Infrastructure
GROUP BY FacilityType;

-- Join water quality with health incidents to find regions with high E. coli contamination and high cases of cholera
SELECT h.RegionID, w.ContaminationLevel AS EColiContamination, h.CasesReported AS CholeraCases
FROM WaterQuality w
JOIN HealthIncident h ON w.WaterSourceID = h.RegionID
WHERE w.ContaminantType = 'E. coli' AND h.DiseaseType = 'Cholera'
ORDER BY w.ContaminationLevel DESC, h.CasesReported DESC;

-- Find regions with the highest number of water sources and their average water quality
SELECT r.RegionID, r.Name, COUNT(w.WaterSourceID) AS NumberOfWaterSources, AVG(wq.ContaminationLevel) AS AvgWaterQuality
FROM Region r
JOIN WaterSource w ON r.RegionID = w.RegionID
JOIN WaterQuality wq ON w.WaterSourceID = wq.WaterSourceID
GROUP BY r.RegionID, r.Name
ORDER BY NumberOfWaterSources DESC, AvgWaterQuality DESC;

-- Monthly trend of cholera cases reported
SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(CasesReported) AS MonthlyCholeraCases
FROM HealthIncident
WHERE DiseaseType = 'Cholera'
GROUP BY DATE_FORMAT(Date, '%Y-%m')
ORDER BY Month;

-- Impact of water quality on health incidents (Cholera)
SELECT w.WaterSourceID, w.ContaminationLevel, h.CasesReported
FROM WaterQuality w
JOIN HealthIncident h ON w.WaterSourceID = h.RegionID
WHERE h.DiseaseType = 'Cholera'
ORDER BY w.ContaminationLevel DESC, h.CasesReported DESC;
