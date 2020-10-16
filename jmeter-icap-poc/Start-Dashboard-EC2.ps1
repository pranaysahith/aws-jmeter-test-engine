$Name = "AWS-TestEngine-Dashboard"
$IP = ""

# Print Status of AWS-TestEngine-Dashboard
$outString = (aws ec2 describe-instances --filters "Name=tag:Name,Values=$($Name)") | Out-String
$outArray = $outString.split([environment]::NewLine)

# Get Instance ID
foreach ($line in $outArray) {
	#echo $line
	if ($line -Match "InstanceId") {
		$InstanceId = $line -replace("InstanceId", "") -replace('"', "") -replace(',', "") -replace(':', "") -replace(" ", "")
		break
	}
}

echo "InstanceId: $($InstanceId)"

# Get State
foreach ($line in $outArray) {
	#echo $line
	if ($line -Match """Name""") {
		$state = $line -replace("Name", "") -replace('"', "") -replace(':', "") -replace(" ", "")
		
		echo "State: $($state)"
		break
	}
}

# If status contains "stopped" then start AWS-TestEngine-Dashboard
if ($state -Match "stopped") {
	echo "Starting $($Name)"
	$start = (aws ec2 start-instances --instance-ids $InstanceId) | Out-String
	
	#echo $start
}


# Wait for machine to start
While ($state -Match "stopped") {
	$outString = (aws ec2 describe-instances --filters "Name=tag:Name,Values=$($Name)") | Out-String
	$outArray = $outString.split([environment]::NewLine)
	
	foreach ($line in $outArray) {
		#echo $line
		if ($line -Match """Name""") {
			$state = $line -replace("Name", "") -replace('"', "") -replace(':', "") -replace(" ", "")
			
			echo "State: $($state)"
			break
		}
	}
	
	Start-Sleep -Seconds 5
}

# Get IP Address
While ($IP -eq ""){
	$outString = (aws ec2 describe-instances --filters "Name=tag:Name,Values=$($Name)") | Out-String
	$outArray = $outString.split([environment]::NewLine)
	
	foreach ($line in $outArray) {
		#echo $line
		if ($line -Match "PublicIpAddress") {
			$IP = $line -replace("PublicIpAddress", "") -replace('"', "") -replace(',', "") -replace(':', "") -replace(" ", "")
			echo "IP Address: $($IP)"
			break
		}
	}
	
	Start-Sleep -Seconds 5
}

#Open Dashboard
$DashURL = "http://$($IP):3000"
echo "View Dashboard at: $DashURL"

start $DashURL