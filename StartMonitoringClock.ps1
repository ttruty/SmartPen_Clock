

Function ClockPgcToTxt ($strPgcIn) {
    $penrequest = new-object -comobject Anoto.ServiceAPI.PenRequest
    $file = new-object -comobject AnotoUtil.File
    $data = $file.Read($strPgcIn)
    $penrequest.Initialize($data)
    $reqpages = $penrequest.Pages
    foreach ($page in $reqpages) {
        $filename = ((get-item $strPgcIn).Directory.FullName + "\" + $page.PageAddress.Split("#")[0] + "_" + (get-item $strPgcIn).Name.TrimEnd("pgc") + "txt")
        $stream = [System.IO.StreamWriter] $filename
        if ($stream)
        {
            $stream.WriteLine("Pen id: " + $penrequest.PenId)
            $stream.WriteLine("Number of pages: 1")
            $bounds = $page.Bounds
            $strokes = $page.PenStrokes
            $stream.WriteLine("Page address: " + $page.PageAddress)
            $stream.WriteLine(("Page bounds:", $bounds.Left, $bounds.Top, $bounds.Right, $bounds.Bottom -join " "))
            $stream.WriteLine("Number of strokes: " + $strokes.Count)
            $strokeid = 1
            foreach ($stroke in $strokes) {
                $arrX = $stroke.x
                $arrY = $stroke.y
                $arrF = $stroke.Force
                $arrT = $stroke.DeltaTime
                $hexColor = [Convert]::ToString($stroke.Color, 16)
                $stream.WriteLine("StrokeID: " + $strokeid)
                $stream.WriteLine("Number of samples: " + $arrX.Count)
                $stream.WriteLine(("Color:", ([Convert]::ToInt32($hexColor.Substring(4, 2), 16)), ([Convert]::ToInt32($hexColor.Substring(2, 2), 16)), ([Convert]::ToInt32($hexColor.Substring(0, 2), 16)) -join " "))
                $stream.WriteLine("StartTime: " + $stroke.StartSecond + "." + $stroke.StartMillisecond.ToString("000"))
                for ($i = 0; $i -lt $arrX.Count; $i++) {
                    $stream.WriteLine(($arrX[$i].ToString("#.0000"), $arrY[$i].ToString("#.0000"), $arrT[$i], $arrF[$i] -join " "))
                }
                $strokeid++
            }
            $stream.Close()
        }
        & python.exe C:\Users\KinectProcessing\Dropbox\pen_printed_paper\clock_single_transform.py $filename         
    }
}

Function MmsePgcToTxt ($strPgcIn) {
    $penrequest = new-object -comobject Anoto.ServiceAPI.PenRequest
    $file = new-object -comobject AnotoUtil.File
    $data = $file.Read($strPgcIn)
    $penrequest.Initialize($data)
    $reqpages = $penrequest.Pages
    foreach ($page in $reqpages) {
        $filename = ((get-item $strPgcIn).Directory.FullName + "\" + $page.PageAddress.Split("#")[0] + "_" + (get-item $strPgcIn).Name.TrimEnd("pgc") + "txt")
        $stream = [System.IO.StreamWriter] $filename
        if ($stream)
        {
            $stream.WriteLine("Pen id: " + $penrequest.PenId)
            $stream.WriteLine("Number of pages: 1")
            $bounds = $page.Bounds
            $strokes = $page.PenStrokes
            $stream.WriteLine("Page address: " + $page.PageAddress)
            $stream.WriteLine(("Page bounds:", $bounds.Left, $bounds.Top, $bounds.Right, $bounds.Bottom -join " "))
            $stream.WriteLine("Number of strokes: " + $strokes.Count)
            $strokeid = 1
            foreach ($stroke in $strokes) {
                $arrX = $stroke.x
                $arrY = $stroke.y
                $arrF = $stroke.Force
                $arrT = $stroke.DeltaTime
                $hexColor = [Convert]::ToString($stroke.Color, 16)
                $stream.WriteLine("StrokeID: " + $strokeid)
                $stream.WriteLine("Number of samples: " + $arrX.Count)
                $stream.WriteLine(("Color:", ([Convert]::ToInt32($hexColor.Substring(4, 2), 16)), ([Convert]::ToInt32($hexColor.Substring(2, 2), 16)), ([Convert]::ToInt32($hexColor.Substring(0, 2), 16)) -join " "))
                $stream.WriteLine("StartTime: " + $stroke.StartSecond + "." + $stroke.StartMillisecond.ToString("000"))
                for ($i = 0; $i -lt $arrX.Count; $i++) {
                    $stream.WriteLine(($arrX[$i].ToString("#.0000"), $arrY[$i].ToString("#.0000"), $arrT[$i], $arrF[$i] -join " "))
                }
                $strokeid++
            }
            $stream.Close()
        }
        #& python.exe C:\Users\KinectProcessing\Dropbox\pen_printed_paper\clock_single_transform.py $filename         
    }
}


### SET FOLDER TO WATCH + FILES TO WATCH + SUBFOLDERS YES/NO
    $clock_watcher = New-Object System.IO.FileSystemWatcher
    $clock_watcher.Path = "C:\Users\KinectProcessing\Documents\Anoto\Clocks"
    $clock_watcher.Filter = "*.pgc*"
    $clock_watcher.IncludeSubdirectories = $false
    $clock_watcher.EnableRaisingEvents = $true 

### SET FOLDER TO WATCH + FILES TO WATCH + SUBFOLDERS YES/NO
    $mmse_watcher = New-Object System.IO.FileSystemWatcher
    $mmse_watcher.Path = "C:\Users\KinectProcessing\Documents\Anoto\MMSE"
    $mmse_watcher.Filter = "*.pgc*"
    $mmse_watcher.IncludeSubdirectories = $false
    $mmse_watcher.EnableRaisingEvents = $true 
 
### DEFINE ACTIONS AFTER AN EVENT IS DETECTED
    $clockaction = { $path = $Event.SourceEventArgs.FullPath                
                $changeType = $Event.SourceEventArgs.ChangeType
                $logline = "$(Get-Date), $changeType, $path"
                Add-content "C:\Users\KinectProcessing\Documents\Anoto\logs\log.txt" -value $logline
                ClockPgcToTxt ($path)
                move-item ($path) -destination "C:\Users\KinectProcessing\Documents\Anoto\Rawpgc"

              }

    $mmseaction = { $path = $Event.SourceEventArgs.FullPath                
                $changeType = $Event.SourceEventArgs.ChangeType
                $logline = "$(Get-Date), $changeType, $path"
                Add-content "C:\Users\KinectProcessing\Documents\Anoto\logs\log.txt" -value $logline
                MmsePgcToTxt ($path)
                move-item ($path) -destination "C:\Users\KinectProcessing\Documents\Anoto\Rawpgc"

              }
    $log = {    $path = $Event.SourceEventArgs.FullPath                
                $changeType = $Event.SourceEventArgs.ChangeType
                $logline = "$(Get-Date), $changeType, $path"
                Add-content "C:\Users\KinectProcessing\Documents\Anoto\\logs\log.txt" -value $logline
              }   
### DECIDE WHICH EVENTS SHOULD BE WATCHED
    
    Register-ObjectEvent $clock_watcher "Created" -Action $clockaction
    Register-ObjectEvent $mmse_watcher "Created" -Action $mmseaction
    #Register-ObjectEvent $clock_watcher "Changed" -Action $log
    #Register-ObjectEvent $clock_watcher "Deleted" -Action $log
    #Register-ObjectEvent $clock_watcher "Renamed" -Action $log
    #Register-ObjectEvent $mmse_watcher "Changed" -Action $log
    #Register-ObjectEvent $mmse_watcher "Deleted" -Action $log
    #Register-ObjectEvent $mmse_watcher "Renamed" -Action $log
    #while ($true) {sleep 1}

    