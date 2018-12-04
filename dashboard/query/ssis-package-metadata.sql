Declare @package_id BIGINT = ?
SELECT pa.name AS PackageName, pr.name AS ProjectName, f.name AS FolderName
FROM catalog.packages pa 
	INNER JOIN catalog.projects pr ON pa.project_id = pr.project_id
	INNER JOIN internal.folders f ON pr.folder_id = f.folder_id
WHERE pa.package_id = @package_id