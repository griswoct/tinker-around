# PURPOSE: RESTART A BROWSER EVERY DAY, AND CLICK PIXAL PERIODICALLY
# AUTHOR: CALEB GRISWOLD, HANNAH SPARGUR
# UPDATED: 05/06/2024

# Set browser process name
$BrowserProcessName = "msedge"

# Set file path to browser's *.exe
$BrowserExePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Set URL of the webpage to open
$URL = "https://app.powerbi.com/groups/me/apps/a9586831-a6bc-4cc7-bcc8-7f290c253bca/reports/ac43fbe2-08b1-4ff0-b760-2cf190248e1b/ReportSection06d38b8985a52a6ba432?ctid=1f67262f-d37c-4cf9-8a56-fa1608024af7&experience=power-bi"

# Function to restart the browser
function Restart-Browser {
    try {
        # Check if the browser process is running
        $Process = Get-Process -Name $global:BrowserProcessName -ErrorAction SilentlyContinue

        if ($Process) {
            # Close the browser process
            Stop-Process -Name $global:BrowserProcessName -Force
            Start-Sleep -Seconds 10
        }
        # Start the browser in full screen mode with the specified URL
        Start-Process -FilePath $global:BrowserExePath -ArgumentList "--start-fullscreen", "--disable-session-crashed-bubble", "--disable-features=BrowserAddPersonEnabled", $global:URL
    }
    catch {
        Write-Host "An error occurred: $_"
    }
}

# Function to send mouse click at specified position
function Send-MouseClick {
    param (
        [int]$X,
        [int]$Y
    )

    Add-Type @"
    using System;
    using System.Runtime.InteropServices;

    public class MouseInput {
        [DllImport("user32.dll",CharSet=CharSet.Auto, CallingConvention=CallingConvention.StdCall)]
        public static extern void mouse_event(long dwFlags, long dx, long dy, long cButtons, long dwExtraInfo);

        public const int MOUSEEVENTF_LEFTDOWN = 0x02;
        public const int MOUSEEVENTF_LEFTUP = 0x04;

        public static void Click(int x, int y) {
            mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, x, y, 0, 0);
        }
    }
"@
    [MouseInput]::Click($X, $Y)
}

# Constants
$SecondsInDay = 86400
$SecondsIn3Minutes = 180
$NumRefresh = $SecondsInDay / $SecondsIn3Minutes

# Loop to restart the browser once per day and click every 3 minutes
while ($true) {
    # Restart the browser
    Restart-Browser

    # Click at specified position every 3 minutes
    for ($i = 0; $i -lt $NumRefresh; $i++)
	{
        Send-MouseClick -X 1108 -Y 117
        Start-Sleep -Seconds $SecondsIn3Minutes
    }
}
