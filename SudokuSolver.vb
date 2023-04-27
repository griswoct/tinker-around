'Sudoku Solver
'Author: Caleb Griswold
'
'This program is an exercise in better understanding of VBA for Excel.
'The purpose of the program is to solve a Sudoku puzzle in Excel with a macro.

'Integer/index naming convention:
	'i = row
	'j = column
	'k = additional row/column index
	'l = additional row/column index
	'n = cell value

Option Explicit

Sub Clear()
    Range("G12:O20").ClearContents      'Solution matrix
    Range("G22:O102").ClearContents     'Working matrix
    Range("G22:O102").Select
        With Selection.Interior
        .Pattern = xlNone
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
End Sub

Sub Initialize()
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
				ActiveCell.Range("A1:A9")Interior.ColorIndex = 5
            Else
                'Populate working matrix options
                For n = 1 To 9
                    Range("F13").Offset(9 * i, j).Cells(n, 1).Value = n
                Next n
            End If
        Next j
    Next i
End Sub
