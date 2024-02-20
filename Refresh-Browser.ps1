#PURPOSE: RESTART A BROWSER EVERY DAY OR WEEK AND OPEN A SPECIFIC PAGE
#AUTHOR: CALEB GRISWOLD
#UPDATED: 02/20/2024

$Browser = "msedge"	#Set browser process name
$Path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"	#File path to browser's *.exe
$URL = '--start-fullscreen "https://app.powerbi.com/groups/me/reports/0cebbe70-aa32-48c1-a01d-cbc709f96a2c/ReportSectioncabb32f803074857db0a"'	#Webpage to open
$LoopRestart = $true	#Set to $true to periodically close and reopen the browser
$RestartTime = 86400	#Number of seconds between restarting the browser (1 day: 86400 - 1 week: 604800)

$Restart = {	#Function to restart the browser
	$Process = Get-Process -Name $Browser -ErrorAction SilentlyContinue	#Get the process, if broswer is running
	if ($Process) {	#Close browser, if open
		Stop-Process -Name $Browser -Force
		Start-Sleep -Seconds 10	#Slow computer, slow operating system, slow browser
	}
	Start-Process -FilePath $Path -ArgumentList $URL	#Open Browser to page URL
}

#Restarts the Browser every so often
$Loop = $true
while ($Loop) {	#Set to $true to loop forever, set to $false if scheduled with Task Manager, auto clicker, or other tools
	& $Restart	#Run $Restart function to restart browser
	Start-Sleep -Seconds $RestartTime	#Sleep for RestartTime
	$Loop = $LoopRestart
}