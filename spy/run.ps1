$curPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath('.\target.csv')
$targetPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath('.\fuck.xls')
$excel = New-Object -ComObject Excel.Application
# $excel.Visible = $true
$excel.Workbooks.Open($targetPath).SaveAs($curPath, 6)
$excel.Workbooks.Close()
$excel.Quit()
(Get-Content $curPath) | Set-Content $curPath -Encoding UTF8