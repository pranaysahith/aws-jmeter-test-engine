$Name = "AWS-TestEngine-LGs"
$Status = "null"

# Get Script Path
$ScriptPath = "$($PSScriptRoot)\cloudformation\GenerateLoadGenerators.json"
echo "Script Path: $($ScriptPath)"

# Create Stack
echo "Creating Stack $($Name)"
$CreateStack = (aws cloudformation create-stack --stack-name $Name --template-body file://$ScriptPath) | Out-String
echo $CreateStack


# Wait for Stack Creation
While ($Status -ne "CREATE_COMPLETE"){
	$outString = (aws cloudformation describe-stacks --stack-name $Name) | Out-String
	$outArray = $outString.split([environment]::NewLine)
	
	foreach ($line in $outArray) {
		#echo $line
		if ($line -Match "StackStatus") {
			$Status = $line -replace("StackStatus", "") -replace('"', "") -replace(',', "") -replace(':', "") -replace(" ", "")
			echo "StackStatus: $($Status)"
			break
		}
	}
	
	Start-Sleep -Seconds 5
}
