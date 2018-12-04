Declare @execution_id bigint
Declare @package_name nvarchar ?
Declare @folder_name nvarchar ?
Declare @project_name nvarchar ?


EXEC [SSISDB].[catalog].[create_execution] @package_name,
    @execution_id=@execution_id OUTPUT,
    @folder_name=@folder_name,
    @project_name=@project_name,
    @use32bitruntime=False,
    @reference_id=Null
Select @execution_id

DECLARE @var0 smallint = 1
EXEC [SSISDB].[catalog].[set_execution_parameter_value] @execution_id,
    @object_type=50,
      @parameter_name=N'LOGGING_LEVEL',
      @parameter_value=@var0
EXEC [SSISDB].[catalog].[start_execution] @execution_id
GO