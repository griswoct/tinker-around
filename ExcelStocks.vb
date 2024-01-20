Sub Rec()
Dim i As Integer
Dim EoB As Date
Dim OpenBell As Date
OpenBell = TimeValue("08:30:00")
EoB = TimeValue("15:00:00")
For i = 0 To 40
        While Time < OpenBell
            'MsgBox "It is before " & OpenBell
            Application.Wait Now + TimeValue("00:10:00")
        Wend
        Rows("3:3").Select
        Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
        Range("C2:CH2").Select
        Selection.Copy
        Range("C3").Select
        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
            :=False, Transpose:=False
        Range("A3").Value = Date
        Range("B3").Value = Time
        Rows("4:4").Select
        Selection.Copy
        Rows("3:3").Select
        Selection.PasteSpecial Paste:=xlPasteFormats, Operation:=xlNone, _
            SkipBlanks:=False, Transpose:=False
        Application.CutCopyMode = False
        If Time > EoB Then  'Market closed
            MsgBox "Closed for the day"
            Exit For
        End If
        Application.Wait Now + TimeValue("00:10:00")
    Next
End Sub