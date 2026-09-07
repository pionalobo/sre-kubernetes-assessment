$Namespace = "sre-assessment"
$Username = "sreuser"
$Database = "sredb"

Write-Host "Creating PostgreSQL Kubernetes Secret..."
Write-Host "Namespace: $Namespace"

$Password = Read-Host "Enter PostgreSQL password" -AsSecureString

$PasswordPlainText = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password)
)

$DatabaseUrl = "postgresql://$Username`:$PasswordPlainText@postgres:5432/$Database"

kubectl create secret generic postgres-secret `
    --namespace $Namespace `
    --from-literal=POSTGRES_USER=$Username `
    --from-literal=POSTGRES_PASSWORD=$PasswordPlainText `
    --from-literal=POSTGRES_DB=$Database `
    --from-literal=DATABASE_URL=$DatabaseUrl `
    --dry-run=client `
    -o yaml | kubectl apply -f -

$PasswordPlainText = $null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Kubernetes Secret created/updated successfully."
}
else {
    Write-Host "Failed to create/update Kubernetes Secret."
    exit 1
}