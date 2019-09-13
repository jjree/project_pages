Attribute VB_Name = "Module2"
'1. create loop to loop through one year of stock data
'2. return the total volume each stock had that year
'requirements (easy): need to show ticker symbol of each stock and its total volume
'                     (moderate): takes following info: ticker, yearly change (opening price to closing price), percent change (opening price to closing price), total volume with conditional formatting
'                     (hard): return stock with greatest % increase, greatest % decrease, greatest total volume

Sub stockVolume()

'Initiate variables
Dim ticker
Dim lastTicker
Dim i
Dim tickerCounter
Dim vol
Dim totVol
totVol = 0
Dim openPrice
Dim closePrice
Dim yearlyChange
Dim yearlyPercentChange
Dim redFill As FormatCondition, greenFill As FormatCondition
Dim rg As Range

'Variable for worksheet loop to run code on all worksheets in workbook
Dim Current As Worksheet

'Loop for each worksheet
For Each Current In Worksheets

'Conditional Formating for +/- Yearly Change in price Green/Red
    Set rg = Current.Range("J2", Current.Range("J2").End(xlDown))
    Set redFill = rg.FormatConditions.Add(xlCellValue, xlLess, "=0")
    Set greenFill = rg.FormatConditions.Add(xlCellValue, xlGreater, "=0")
    With redFill
    .Interior.Color = vbRed
    End With
    With greenFill
    .Interior.Color = vbGreen
    End With

    'Initiate Ticker and Stock Volume Column Title Strings
    Current.Range("I1").Value = "Ticker"
    Current.Range("J1").Value = "Yearly Change"
    Current.Range("K1").Value = "Percent Change"
    Current.Range("L1").Value = "Total Stock Volume"
    
    'Loop until the cell is empty
    'For loop is acceptable when the total rows are consistent over each worksheet
    'However, the total rows for each worksheet is different each time for this workbook
    'so use Do loop until cell is empty
    i = 2    'loop counter
    tickerCounter = 1   'ticker counter used to identify correct cells to input ticker and total volume
    lastTicker = "ZZZZZZZZZZZZZZZZZZZ" 'initiate lastTicker variable
    
    'Loop to traverse rows of Data
    Do Until IsEmpty(Current.Cells(i, 1))
    
    'assigning ticker and vol values of new row
        ticker = Current.Cells(i, 1).Value
        vol = Current.Cells(i, 7).Value
        
'-----------------------------------------------------
    'If1: Check if beginning of the worksheet or no tickers are being tracked
        If (lastTicker = "ZZZZZZZZZZZZZZZZZZZ") Then
            totVol = vol
            openPrice = Current.Cells(i, 3).Value
'-----------------------------------------------------
    'If2: Check if the ticker is the same as the last iteration and if so add the volume to the total volume
        ElseIf (ticker = lastTicker) Then
            totVol = totVol + vol
            'IF: Check if end of worksheet, if so print ticker and total volume
            If (IsEmpty(Current.Cells(i + 1, 1))) Then
                closePrice = Current.Cells(i, 6).Value
                If (openPrice = 0) Then 'check for zero values of open and close price
                    yearlyChange = 0
                    yearlyPercentChange = 0
                Else
                    yearlyChange = closePrice - openPrice
                    yearlyPercentChange = yearlyChange / openPrice
                End If
                
                Current.Cells(tickerCounter + 1, 9).Value = ticker
                Current.Cells(tickerCounter + 1, 10).Value = yearlyChange
                Current.Cells(tickerCounter + 1, 11).Value = FormatPercent(yearlyPercentChange, 2)
                Current.Cells(tickerCounter + 1, 12).Value = totVol
            End If
'-----------------------------------------------------
    'If3: Check if ticker is different from last iteration then record previous ticker and its total volume and restart recording new ticker
        ElseIf (ticker <> lastTicker And lastTicker <> "ZZZZZZZZZZZZZZZZZZZ") Then
            
    'Calculating yearly price and percentage change of previous ticker once new ticker is found AND outputting
            closePrice = Current.Cells(i - 1, 6).Value
            If (openPrice = 0 And closePrice = 0) Then 'check for zero values of open and close price
                    yearlyChange = 0
                    yearlyPercentChange = 0
                Else
                    yearlyChange = closePrice - openPrice
                    yearlyPercentChange = yearlyChange / openPrice
                End If
            Current.Cells(tickerCounter + 1, 9).Value = lastTicker
            Current.Cells(tickerCounter + 1, 10).Value = yearlyChange
            Current.Cells(tickerCounter + 1, 11).Value = FormatPercent(yearlyPercentChange, 2)
            Current.Cells(tickerCounter + 1, 12).Value = totVol
            
    'Assigning new row to output since new ticker found
            tickerCounter = tickerCounter + 1

    'Assigning new open price since new ticker was found AND initializing new total volume to new ticker's initial volume
            openPrice = Current.Cells(i, 3).Value
            totVol = vol
            
            'IF: Check if end of worksheet, if so print ticker and total volume (note: this IF statement will only run in the case where new ticker is found and only one row exists at the end of the worksheet)
            If (IsEmpty(Current.Cells(i + 1, 1))) Then
                closePrice = Current.Cells(i, 6).Value
                If (openPrice = 0 And closePrice = 0) Then 'check for zero values of open and close price
                    yearlyChange = 0
                    yearlyPercentChange = 0
                Else
                    yearlyChange = closePrice - openPrice
                    yearlyPercentChange = yearlyChange / openPrice
                End If
                Current.Cells(tickerCounter + 1, 9).Value = ticker
                Current.Cells(tickerCounter + 1, 10).Value = yearlyChange
                Current.Cells(tickerCounter + 1, 11).Value = FormatPercent(yearlyPercentChange, 2)
                Current.Cells(tickerCounter + 1, 12).Value = vol
            End If
        End If
    
    'assigning current ticker to lastTicker
        lastTicker = ticker
        
    'Continuing Do loop
        i = i + 1
        Loop


Next
     
MsgBox ("Macro Completed")

End Sub


