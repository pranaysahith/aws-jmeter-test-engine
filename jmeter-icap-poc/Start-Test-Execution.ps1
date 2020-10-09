# This script checks the status of the dashboard EC2 instance. Starts it if necessary, and launches the Dashboard login page.
$Script1 = "Start-Dashboard-EC2.ps1"

# This script launches a CloudFormation Stack in AWS and monitors it till creation is complete.
$Script2 = "Start-LoadGenerators-CloudFormation.ps1"

echo "Executing Script: $($PSScriptRoot)\$($Script1)"
.("$($PSScriptRoot)\$($Script1)")

echo "Executing Script: $($PSScriptRoot)\$($Script2)"
.("$($PSScriptRoot)\$($Script2)")