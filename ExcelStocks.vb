Option Explicit

Sub Rec()
    Dim i As Integer
    Dim OpenBell, EoB As Date
    Dim Time0, Time1
    OpenBell = TimeValue("08:30:00AM ")
    EoB = TimeValue("03:00:59PM")
    Workbooks("TickTrack.xlsm").Activate
        If Time < OpenBell Then 'Market closed
            Application.OnTime OpenBell, "TickTrack.xlsm!Sheet2.Rec"   'Try again at the opening bell
            MsgBox "Market not yet open"
        Else
            If Time > EoB Then  'Market closed
                MsgBox "Closed for the day"
            Else
                Application.OnTime Now + TimeValue("00:09:59"), "TickTrack.xlsm!Sheet2.Rec"
                Call SaveData
            End If
        End If
End Sub

Sub SaveData()
    Rows("3:3").Select
    Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
    Range("C2:CZ2").Select
    Selection.Copy
    Range("C3").Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks:=False, Transpose:=False
    Range("A3").Value = Date
    Range("B3").Value = Time
    Rows("4:4").Select
    Selection.Copy
    Rows("3:3").Select
    Selection.PasteSpecial Paste:=xlPasteFormats, Operation:=xlNone, SkipBlanks:=False, Transpose:=False
    Application.CutCopyMode = False
    ActiveWorkbook.Save
End Sub
