'SUDOKU SOLVER
'
'PURPOSE: SOLVE A SUDOKU PUZZLE IN EXCEL WITH A MACRO
'LICENSE: THE UNLICENSE
'AUTHOR: CALEB GRISWOLD
'UPDATED: 2023-07-26
'
'This program is an exercise in better understanding of VBA for Excel.
'NOTE:	INITIAL SUDOKU PUZZLE MUST BE PLACED IN RANGE: G2:O10
'		SOLUTION WILL APPEAR IN RANGE G12:O20

Option Explicit

Sub Solve()
	Dim blanks, z, max As Integer
	Call Clear
	Call Initialize
	blanks = 81		'81 squares in a traditional Sudoku grid
	max = 9		'Max number of itterations
	z = 0
	Do While blanks > 0
		Call SimpleElimination
		Call OnlyOption
		Call SimpleElimination
		Call aPlaceForEverything
		blanks = NumBlanks
		Range("Q19").Value = blanks
		If z > max Then		'Abort after max itterations
			GoTo MaxItterations
		End If
		z = z + 1
		Range("Q20").Value = z		'Record number of itterations
	Loop
	If NumBlanks = 0 Then
		MsgBox "Solved!"
	End If
	Exit Sub
MaxItterations:
	MsgBox "Maximum number of itterations reached:" & max
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
	Range("Q19").Value = 0		'Number of blanks in solution
	Range("Q20").Value = 0		'Number of itterations
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

Sub SimpleElimination()     'Remove n as an option if it is already present in the row/column/section of the solution matrix
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

Sub OnlyOption()        'If solution cell is empty, but only one option remains, fill in the solution cell.
    Dim i, j, k, n As Integer
    For i = 1 To 9
        For j = 1 To 9
            If Range("G12:O20").Cells(i, j).Value = "" Then     'Solution cell is empty
                n = 0
                For k = 1 To 9      'Itterate through options
                    If Range("F13").Offset(9 * i, j).Cells(k) <> "" Then    'Option value exists
                        If n > 0 Then		'Possible value already found
                            GoTo MultipleOptions		'Multiple options, move to next cell
                        End If
                        n = k		'Save possible value
                    End If
                Next k
                If n > 0 Then
                    Range("G12:O20").Cells(i, j).Value = Range("F13").Offset(9 * i, j).Cells(n).Value      'Only on option, assign solution
                    Range("G12:O20").Cells(i, j).Font.Italic = True
                End If
            End If
MultipleOptions:
        Next j
    Next i
End Sub

Sub aPlaceForEverything()       'Each number 1-9 must fit somewhere. If only one spot is available, fill it in.
    Dim i, j, k, n, x As Integer
    For n = 1 To 9
        For i = 0 To 8      'Itterate through rows
            x = 0       'Number of spots n could be in row i
            For j = 1 To 9      'Itterate through columns in row
                If Range("G22:O102").Cells(i * 9 + n, j) <> "" Then   'If possible value listed in working matrix
                    x = x + 1       'k number of spots n could be located in the row
                    If x > 1 Then       'If more than one location is possible, move on to next row
                        GoTo MultipleSpotR
                    End If
                    k = j		'Save column
                End If
            Next j
            If x = 1 And Range("G12:O20").Cells(i + 1, k) = "" Then       'Only 1 spot n could be located in row i, and solution cell is blank
                Range("G12:O20").Cells(i + 1, k) = n        'Fill in solution
                Range("G12:O20").Cells(i + 1, k).Font.Italic = True
                For x = 1 To 9      'Delete other options from working matrix for this cell
                    If x <> n Then
                        Range("G22:O102").Cells(i * 9 + x, k).Value = ""
                    End If
                Next x
            End If
MultipleSpotR:
        Next i
        For j = 1 To 9      'Itterate through columns
            x = 0       'Number of spots n could be in column j
            For i = 0 To 8      'Itterate through rows in column
                If Range("G22:O102").Cells(i * 9 + n, j) <> "" Then   'If possible value listed in working matrix
                    x = x + 1       'x number of spots n could be located in the column
                    If x > 1 Then       'If more than one location is possible, move on to next row
                        GoTo MultipleSpotC
                    End If
                    k = i		'Save row
                End If
            Next i
            If x = 1 And Range("G12:O20").Cells(k + 1, j) = "" Then       'Only 1 spot n could be located in row i, and solution cell is blank
                Range("G12:O20").Cells(k + 1, j) = n        'Fill in solution
                Range("G12:O20").Cells(k + 1, j).Font.Italic = True
                For x = 1 To 9      'Delete other options from working matrix for this cell
                    If x <> n Then
                        Range("G22:O102").Cells(k * 9 + x, j).Value = ""
                    End If
                Next x
            End If
MultipleSpotC:
        Next j
		Dim g, h, l As Integer
		g = 0
		Do While g < 9	'Itterate through subsection (rows)
			h = 0
			Do While h < 9	'Itterate through subsection (columns)
				x = 0	'Number of spots n could be in subsection (g, h)
				For i = 0 To 2	'Itterate through subrows
					For j = 1 To 3	'Itterate through subcolumns
						If Range("G22:O102").Cells(9 * g + 9 * i + n, h + j) <> "" Then   'If possible value listed in working matrix
							x = x + 1	'x number of spots n could be located in subsection
							If x > 1 Then	'If more than one subcell is possible, move to next section
								GoTo MultipleSpotS
							Else
								k = i	'Save subrow
								l = j	'Save subcolumn
							End If
						End If
					Next j
				Next i
				If x = 1 And Range("G12:O20").Cells(g + k + 1, h + l) = "" Then	'Only 1 spot n could be located in row i, and solution cell is blank
					Range("G12:O20").Cells(g + k + 1, h + l) = n	'Fill in solution
					Range("G12:O20").Cells(g + k + 1, h + l).Font.Italic = True	'Italic SOLUTION
					'Range("G12:O20").Cells(g + k + 1, h + l).Font.Color = RGB(255, 0, 0)	'For testing
					For x = 1 To 9      'Delete other options from working matrix for this cell
						If x <> n Then
							Range("G22:O102").Cells(9 * g + 9 * k + x, h + l).Value = ""
						End If
					Next x
				End If
MultipleSpotS:
				h = h + 3
			Loop
			g = g + 3
		Loop
    Next n
End Sub

Function NumBlanks() As Integer
    Dim i, j, k As Integer
    NumBlanks = 0
    For i = 1 To 9
        For j = 1 To 9
            If Range("G12:O20").Cells(i, j).Value = "" Then        'The cell is blank
                NumBlanks = NumBlanks + 1
            Else        'Cell is not blank, check for duplicate values
                For k = 1 To 9     'Itterate through row
                    If j <> k Then      'Don't check the original cell
                        If Range("G12:O20").Cells(i, j).Value <> "" Then
                            If Range("G12:O20").Cells(i, j).Value = Range("G12:O20").Cells(i, k).Value Then     'Duplicate value in same row!
                                GoTo ErrorHandler
                            End If
                        End If
                    End If
                Next k
            End If
        Next j
    Next i
    For j = 1 To 9
        For i = 1 To 9
            If Range("G12:O20").Cells(i, j).Value <> "" Then        ''Cell is not blank, check for duplicate values
                For k = 1 To 9     'Itterate through column
                    If i <> k Then      'Don't check the original cell
                        If Range("G12:O20").Cells(i, j).Value = Range("G12:O20").Cells(k, j).Value Then     'Duplicate value in same column!
                            GoTo ErrorHandler
                        End If
                    End If
                Next k
            End If
        Next i
    Next j
Exit Function
ErrorHandler:
    MsgBox "Duplicate values found in the same row or column!"
    NumBlanks = 99       'There 81 squares in a Sudoku puzzle
End Function
