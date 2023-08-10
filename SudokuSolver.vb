'SUDOKU SOLVER
'
'PURPOSE: SOLVE A SUDOKU PUZZLE IN EXCEL WITH A MACRO
'LICENSE: THE UNLICENSE
'AUTHOR: CALEB GRISWOLD
'UPDATED: 2023-08-04
'
'This program is an exercise in better understanding of VBA for Excel.
'NOTE:  INITIAL SUDOKU PUZZLE MUST BE PLACED IN RANGE: G2:O10
'       SOLUTION WILL APPEAR IN RANGE G12:O20
'IDEAS: If only two options remain, and they are in the same column, row, or section
'       Then eliminate thoes two options elseware in the column, row, or section
'       And remove other options from thoese two cells
'       Mark rows, columns, subsections, or numbers as done and skip checking them in the future

Option Explicit

Sub Solve()
    Dim blanks, z, max As Integer
    Call Clear
    Call Initialize
    blanks = 81     '81 squares in a traditional Sudoku grid
    max = 9     'Max number of itterations
    z = 0
    Do While blanks > 0
        Call SimpleElimination      'Remove n as an option if it is already in the solution for that row, column, or subsection
        Call OnlyOption     'Scan each cell and fill in the solution if only one option remains
        Call SimpleElimination      'Not needed if clean up is added to OnlyOption
        Call aPlaceForEverything        'If only one location possible for n, fill in the solution
        blanks = NumBlanks
        Range("Q19").Value = blanks
        If z > max Then     'Abort after max itterations
            GoTo MaxItterations
        End If
        z = z + 1
        Range("Q20").Value = z      'Record number of itterations
    Loop
    If NumBlanks = 0 Then
        MsgBox "Solved!"
    End If
    Exit Sub
MaxItterations:
    MsgBox "Maximum number of itterations reached:" & max + 1
End Sub

Sub Clear()     'Delete all values from the solution and working matricies, and reset formating.
    Range("G12:O20").ClearContents      'Solution matrix
    Range("G12:O20").Font.Bold = False
    Range("G12:O20").Font.Italic = False
    Range("G12:G20").Font.Color = RGB(0, 0, 0)
    Range("G22:O102").ClearContents     'Working matrix
    Range("G22:O102").Font.Bold = False
    Range("G22:O102").Font.Italic = False
    Range("G22:O102").Select
        With Selection.Interior
        .Pattern = xlNone
        .TintAndShade = 0
        .PatternTintAndShade = 0
        End With
    Range("Q19").Value = 0      'Number of blanks in solution
    Range("Q20").Value = 0      'Number of itterations
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
            Else        'Populate working matrix options
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
                        If n > 0 Then       'Possible value already found
                            GoTo MultipleOptions        'Multiple options, move to next cell
                        End If
                        n = k       'Save possible value
                    End If
                Next k
                If n > 0 Then
                    Range("G12:O20").Cells(i, j).Value = Range("F13").Offset(9 * i, j).Cells(n).Value      'Only one option, assign solution
                    Range("G12:O20").Cells(i, j).Font.Italic = True
                    'Remove n elsewhere in row
                    'Remove n elsewhere in column
                    'Remove n elsewhere in subsection
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
                    k = j       'Save column
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
                'Remove n elsewhere in column k
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
                    k = i       'Save row
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
                'Remove n elsewhere in row k
            End If
MultipleSpotC:
        Next j
    Next n
End Sub

Sub TicTacToe()     'If 1 to 3 possible locations remain for n in a subsection, all in the same row or column, remove elsewhere in the row or column
    Dim g, h, i, j, k1, k2, k3, l1, l2, l3, n, x As Integer
    For n = 1 To 9
        g = 0
        Do While g < 9  'Itterate through subsection (rows)
            h = 0
            Do While h < 9  'Itterate through subsection (columns)
                x = 0   'Number of spots n could be in subsection (g, h)
                k1 = 0: l1 = 0: k2 = 0: l2 = 0: k3 = 0: l3 = 0  'Saved subrow and subcolumns
                For i = 0 To 2  'Itterate through subrows
                    For j = 1 To 3  'Itterate through subcolumns
                        If Range("G12:O20").Cells(g + i + 1, h + j) = n Then  'Solution already filled in
                            GoTo NextSection
                        ElseIf Range("G22:O102").Cells(9 * g + 9 * i + n, h + j) <> "" Then   'If possible value listed in working matrix
                            x = x + 1  'x number of spots n could be located in subsection
                            If x > 3 Then   'If more than 3 locations are possible, move to next section
                                GoTo NextSection
                            ElseIf x = 1 Then
                                k1 = i  'Save subrow 1
                                l1 = j  'Save subcolumn 1
                            ElseIf x = 2 Then
                                k2 = i  'Save subrow 2
                                l2 = j  'Save subcolumn 2
                            ElseIf x = 3 Then
                                k3 = i  'Save subrow 3
                                l3 = j  'Save subcolumn 3
                            Else    'Not populated or error
                                GoTo NextSection
                            End If
                        End If
                    Next j
                Next i
                If x = 1 Then   'Only 1 spot n could be located in subsection , and solution cell is blank
                    Range("G12:O20").Cells(g + k1 + 1, h + l1) = n   'Fill in solution
                    Range("G12:O20").Cells(g + k1 + 1, h + l1).Font.Italic = True    'Italic solution
                    Range("G12:O20").Cells(g + k1 + 1, h + l1).Font.Color = RGB(0, 255, 0)   'For testing
                    For i = 1 To 9      'Delete other options from working matrix for this cell
                        If i <> n Then
                            Range("G22:O102").Cells(9 * g + 9 * k1 + i, h + l1).Value = ""
                            'Range("G22:O102").Cells(9 * g + 9 * k1 + i, h + l1).Interior.Color = RGB(0, 255, 0) 'For testing
                        End If
                    Next i
                    For j = 1 To 9  'Delete n as an option elsewhere in the row g + k1
                        If j <> h + l1 Then      'Ignore solution cell
                            Range("G22:O102").Cells(9 * g + 9 * k1 + n, j).Value = ""
                            'Range("G22:O102").Cells(9 * g + 9 * k1 + n, j).Interior.Color = RGB(0, 255, 0)  'For testing
                        End If
                    Next j
                    For i = 0 To 8  'Delete n as an option elsewhere in the column h + l1
                        If i <> g + k1 Then      'Ignore solution cell
                            Range("G22:O102").Cells(9 * i + n, h + l1).Value = ""
                            'Range("G22:O102").Cells(9 * i + n, h + l1).Interior.Color = RGB(0, 255, 0)  'For testing
                        End If
                    Next i
                ElseIf x = 2 Or x = 3 Then
                    If x = 2 Then   'If only 2 options remain, set third saved location to second saved location
                        k3 = k2
                        l3 = l2
                    End If
                    If k1 = k2 And k2 = k3 Then 'All possible locations for n within the subsection are in the same row
                        For j = 1 To 9  'Delete n as an option elsewhere in the row g + k
                            If j = h + l1 Or j = h + l2 Or j = h + l3 Then      'Possible solution locations
                                'Range("G22:O102").Cells(9 * g + 9 * k1 + n, j).Font.Color = RGB(255, 0, 0)   'Possible value in red for testing
                            Else
                                Range("G22:O102").Cells(9 * g + 9 * k1 + n, j).Value = ""
                                'Range("G22:O102").Cells(9 * g + 9 * k1 + n, j).Interior.Color = RGB(255, 0, 0)  'For testing
                            End If
                        Next j
                    End If
                    If l1 = l2 And l2 = l3 Then 'All possible locations for n within the subsection are in the same column
                        For i = 0 To 8  'Delete n as an option elsewhere in the column h + l
                            If i = g + k1 Or i = g + k2 Or i = k3 Then      'Possible solution locations
                                'Range("G22:O102").Cells(9 * i + n, h + l1).Font.Color = RGB(255, 0, 0)  'Possible value in red for testing
                            Else
                                Range("G22:O102").Cells(9 * i + n, h + l1).Value = ""
                                'Range("G22:O102").Cells(9 * i + n, h + l1).Interior.Color = RGB(255, 0, 0)  'For testing
                            End If
                        Next i
                    End If
                End If
NextSection:
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

