Declare @folderName nvarchar(255) = ?
Declare @projectName nvarchar(255) = ?
Declare @packageName nvarchar(255) = ?
Declare @parameters nvarchar(max) = ?
INSERT INTO VD_Log.dbo.SSIS_QUE VALUES(@folderName, @projectName, @packageName, @parameters);