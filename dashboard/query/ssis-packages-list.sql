SELECT 
    package_id,
    pa.name
FROM [catalog].packages pa 
	INNER JOIN catalog.projects pr ON pa.project_id = pr.project_id
	INNER JOIN internal.folders f ON pr.folder_id = f.folder_id
    WHERE  f.name $clause