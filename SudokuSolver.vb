'SUDOKU SOLVER
'
'This program is an exercise in better understanding of VBA for Excel.
'The purpose of the program is to solve a Sudoku puzzle in Excel with a macro.
'
'Written by: Caleb Griswold

Option Explicit

Sub Solve()
	Dim blanks, z, max As Integer
	Call Clear
	Call Initialize
	blanks = 81
	max = 10		'Max number of itterations
	z = 0
	Do While blanks > 0
		Call SimpleElimination
		Call OnlyOption
		Call aPlaceForEverything
		blanks = NumBlanks
		If z > max Then		'Abort after max itterations
			GoTo SomethingWrong
		End If
		z = z + 1
	Loop
	If NumBlanks = 0 Then
		MsgBox "Done!"
	End If
	Exit Sub
SomethingWrong:
	MsgBox "An error occured!"
	Call Clear
End Sub

Sub Clear()     'Delete all values from the solution and working matricies, and reset formating.
    Range("G12:O20").ClearContents      'Solution matrix
    Range("G12:O20").Font.Bold = False
    Range("G12:O20").Font.Italic = False
    Range("G22:O102").ClearContents     'Working matrix
    Range("G22:O102").Select
        With Selection.Interior
        .Pattern = xlNone
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
End Sub

Sub Initialize()        'Copy initial values to the solution matrix, and populate the working matrix.
    Dim i, j, n As Integer
    For i = 1 To 9
        For j = 1 To 9
            If Range("G2:O10").Cells(i, j).Value <> "" Then     'Initial matrix has a value
                n = Range("G2:O10").Cells(i, j).Value
                Range("G12:O20").Cells(i, j).Value = n    'Copy initial value to solution matrix
                Range("G12:O20").Cells(i, j).Font.Bold = True
                Range("F13").Offset(9 * i, j).Cells(n, 1).Value = n  'Copy initial value to working matrix
                Range("F13").Offset(9 * i, j).Cells(n, 1).Font.Bold = True
                Range("F13").Offset(9 * i, j).Select
                'ActiveCell.Range("A1:A9").Interior.ColorIndex = 5
            Else		'Populate working matrix options
                For n = 1 To 9
                    Range("F13").Offset(9 * i, j).Cells(n, 1).Value = n
                Next n
            End If
        Next j
    Next i
	Range("A1").Select
End Sub

Sub SimpleElimination()     'Remove n as an option if it is already present in the row/column/section.
    Dim i, j, k, l, n As Integer
    For i = 1 To 9      'If n is in the solution matrix, remove n as an option elsewhere in the row
        For j = 1 To 9
            If Range("G12:O20").Cells(i, j).Value <> "" Then    'Solution cell is not empty
                n = Range("G12:O20").Cells(i, j).Value      'Solution cell's value
                For k = 1 To 9      'Iterate through columns in the row
                    If k <> j Then      'Ignore solution cell
                        Range("F13").Offset(9 * i, k).Cells(n, 1) = ""      'Delete n as an option
                    End If
                Next k
            End If
        Next j
    Next i
    For j = 1 To 9      'If n is in the solution matrix, remove n as an option elsewhere in the column
        For i = 1 To 9
            If Range("G12:O20").Cells(i, j).Value <> "" Then    'Solution cell is not empty
                n = Range("G12:O20").Cells(i, j).Value      'Solution cell's value
                For k = 1 To 9      'Iterate through rows in the column
                    If k <> i Then      'Ignore solution cell
                        Range("F13").Offset(9 * k, j).Cells(n, 1) = ""      'Delete n as an option
                    End If
                Next k
            End If
        Next i
    Next j
    i = 0
    Dim x, y As Integer
    Do While i < 9
        j = 0
        Do While j < 9
            For k = 1 To 3
                For l = 1 To 3
                    If Range("G12:O20").Cells(i + k, j + l).Value <> "" Then        'Solution cell is not empty
                        n = Range("G12:O20").Cells(i + k, j + l).Value      'Solution cell's value
                        For x = 0 To 2
                            For y = 1 To 3
                                If x = k - 1 And y = l Then
                                Else
                                    Range("G22:O102").Cells(9 * i + 9 * x + n, j + y).Value = ""
                                End If
                            Next y
                        Next x
                    End If
                Next l
            Next k
        j = j + 3
        Loop
    i = i + 3
    Loop
End Sub
