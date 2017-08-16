Set-ExecutionPolicy -Scope CurrentUser remotesigned
# param([string]$file=$(throw "Parameter missing: -file xlsFile required"))
$sourcePath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath('.\input.xls')
$targetPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath('.\target.csv')
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.Workbooks.Open($sourcePath).SaveAs($targetPath, 6)
$excel.Workbooks.Close()
$excel.Quit()
# (Get-Content $targetPath) | Set-Content $targetPath -Encoding UTF8
python .\spy.py