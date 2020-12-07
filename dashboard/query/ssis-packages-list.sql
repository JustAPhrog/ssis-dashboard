SELECT 
    package_id,
    pa.name,
    p.name as project_name
FROM [catalog].packages pa 
	INNER JOIN catalog.projects pr ON pa.project_id = pr.project_id
	INNER JOIN internal.folders f ON pr.folder_id = f.folder_id
    INNER JOIN [catalog].projects p ON pa.project_id = p.project_id
    WHERE  f.name $clause