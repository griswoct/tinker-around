Sub Rec()
Do
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
        Application.Wait Now + TimeValue("00:10:00")
    Loop
End Sub