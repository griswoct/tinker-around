Option Explicit

Sub Rec()
    Dim i As Integer
    Dim OpenBell, EoB As Date
    Dim Time0, Time1
    OpenBell = TimeValue("08:25:00AM")
    EoB = TimeValue("03:05:00PM")
    'For i = 0 To 48 'Record every 10min for up to 8hrs
        If Time < OpenBell Then
            Application.OnTime Now + TimeValue("00:10:00"), "Sheet2.Rec"
            MsgBox "Market not yet open"
        Else
            If Time > EoB Then  'Market closed
                MsgBox "Closed for the day"
            Else
                Call SaveData
                Application.OnTime Now + TimeValue("00:10:00"), "Sheet2.Rec"
            End If
        End If
    'Next
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
