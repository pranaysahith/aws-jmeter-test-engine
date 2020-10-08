$Name = "AWS-TestEngine-LGs"
$Status = "null"
#$input = Read-Host "Enter path of directory containing git repository aws-jmeter-test-engine-v1"
$input = "c:\git\"

# Check for CloudFormation Script
if (!(Test-Path "$($input)\aws-jmeter-test-engine-v1\jmeter-icap-poc\cloudformation\GenerateLoadGenerators.json" -PathType Leaf)) {
	echo "Unable to locate Cloudformantion Script $($input)\aws-jmeter-test-engine-v1\jmeter-icap-poc\cloudformation\GenerateLoadGenerators.json"
	echo "expected path should be the directory containing the aws-jmeter-test-engine-v1 repository"
	exit
}
else {
	$ScriptPath = "$($input)\aws-jmeter-test-engine-v1\jmeter-icap-poc\cloudformation\GenerateLoadGenerators.json"
	echo "Script Path: $($ScriptPath)"
}

# Create Stack
echo "Creating Stack $($Name)"
$CreateStack = (aws cloudformation create-stack --stack-name $Name --template-body file://$ScriptPath) | Out-String
echo $CreateStack

#$StackStatus = (aws cloudformation describe-stacks --stack-name $Name) | Out-String
#echo $StackStatus
#
#$outArray = $StackStatus.split([environment]::NewLine)

#"StackStatus": "CREATE_IN_PROGRESS" "StackStatus": "CREATE_COMPLETE"

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

echo "----End of Script----"