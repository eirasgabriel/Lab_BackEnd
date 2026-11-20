# Execute na raiz Projeto_VSCode com as duas APIs iniciadas.
$url = 'http://127.0.0.1:8000/alunos'
$resposta = Invoke-WebRequest -Uri $url -SessionVariable sessao -UseBasicParsing
$token = $sessao.Cookies.GetCookies([uri]$url)['csrftoken'].Value
$corpo = @{nome='Bruno'; curso='Engenharia de Software'} | ConvertTo-Json
Invoke-RestMethod -Uri $url
Invoke-RestMethod -Uri $url -Method Post -WebSession $sessao -Headers @{'X-CSRFToken'=$token} -ContentType 'application/json' -Body $corpo
Invoke-RestMethod -Uri 'http://127.0.0.1:8001/alunos' -Method Post -ContentType 'application/json' -Body $corpo
Invoke-RestMethod -Uri $url
Invoke-RestMethod -Uri 'http://127.0.0.1:8001/alunos'
$invalido = '{"nome":"   ","curso":"Backend"}'
foreach ($porta in @(8000,8001)) {
    try {
        $parametros = @{Uri="http://127.0.0.1:$porta/alunos"; Method='Post'; ContentType='application/json'; Body=$invalido}
        if ($porta -eq 8000) {
            $parametros.WebSession = $sessao
            $parametros.Headers = @{'X-CSRFToken'=$token}
        }
        Invoke-RestMethod @parametros
    } catch {
        Write-Output "Porta $porta"
        Write-Output ([int]$_.Exception.Response.StatusCode)
        Write-Output $_.ErrorDetails.Message
    }
}
