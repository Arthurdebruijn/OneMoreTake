function Invoke-UE($Tool, $Arguments = @{}) {
    $payload = @{jsonrpc='2.0';id=2;method='tools/call';params=@{name=$Tool;arguments=$Arguments}} | ConvertTo-Json -Depth 60 -Compress
    $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8001/mcp' -Method Post -ContentType 'application/json' -Headers @{Accept='application/json, text/event-stream';'Mcp-Session-Id'='8caab51041e9f904c23f99bcc6dafa96'} -Body ([System.Text.Encoding]::UTF8.GetBytes($payload)) -TimeoutSec 60
    $response | ConvertTo-Json -Depth 70
}
function Call-UE($Set, $Tool, $UEParams = @{}) {
  $r = Invoke-UE call_tool @{toolset_name=$Set;tool_name=$Tool;arguments=$UEParams} | ConvertFrom-Json
  $r.result.content | ForEach-Object { if ($_.type -eq 'text') {$_.text} }
}
function Py-UE($Code) { Call-UE 'editor_toolset.toolsets.python_scripting.PythonScriptingTools' 'execute_python' @{script=@{content=$Code;language='Python'}} }

function Save-UEImage($Set,$Tool,$UEParams,$File) {
  $r=Invoke-UE call_tool @{toolset_name=$Set;tool_name=$Tool;arguments=$UEParams}|ConvertFrom-Json
  $im=$r.result.content | Where-Object type -eq image | Select-Object -First 1
  if ($im) {[IO.File]::WriteAllBytes((Join-Path (Get-Location) $File),[Convert]::FromBase64String($im.data)); return 'Image saved'}
  foreach($c in $r.result.content) { if($c.type -eq 'text') { $o=$c.text|ConvertFrom-Json; $v=$o.returnValue; if($v.image.data) {$v=$v.image}; if($v.data) {[IO.File]::WriteAllBytes((Join-Path (Get-Location) $File),[Convert]::FromBase64String($v.data));return 'Image saved'}; $c.text.Substring(0,[Math]::Min(300,$c.text.Length)) } }
}

