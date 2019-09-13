Attribute VB_Name = "Module3"
'1. create loop to loop through one year of stock data
'2. return the total volume each stock had that year
'requirements (easy): need to show ticker symbol of each stock and its total volume
'                     (moderate): takes following info: ticker, yearly change (opening price to closing price), percent change (opening price to closing price), total volume with conditional formatting
'                     (hard): return stock with greatest % increase, greatest % decrease, greatest total volume

Sub stockVolume()

'Initiate variables
Dim ticker
Dim nextTicker
Dim i
Dim tickerCounter
Dim totVol

'totVol = 0
'Dim vol
'vol = 0
Dim openPrice
Dim closePrice
Dim yearlyChange
Dim yearlyPercentChange
Dim redFill As FormatCondition, greenFill As FormatCondition
Dim rg As Range
Dim greatestIncrease
Dim greatestDecrease
Dim greatestVol
Dim maxTicker
Dim yearlyPercentChangeMax
yearlyPercentChangeMax = 0
Dim minTicker
Dim yearlyPercentChangeMin
yearlyPercentChangeMin = 0
Dim volTicker
Dim volMax
volMax = 0

'Initiating Greatest x table
Cells(2, 14).Value = "Greatest % Increase"
Cells(3, 14).Value = "Greatest % Decrease"
Cells(4, 14).Value = "Greatest Total Volume"
Cells(1, 15).Value = "Ticker"
Cells(1, 16).Value = "Value"

'Worksheet Variable for worksheet loop to run code on all worksheets in workbook
Dim Current As Worksheet

'Loop for each worksheet
For Each Current In Worksheets

'Conditional Formating for +/- Yearly Change column price: Green/Red, respectively
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
    
    'yearlyPercentChangeMax = 0
    'yearlyPercentChangeMin = 0
    'volMax = 0
    
    'Loop until the cell is empty
    'For loop is acceptable when the total rows are consistent over each worksheet
    'However, the total rows for each worksheet is different each time for this workbook
    'so use Do loop until cell is empty
    i = 2    'loop counter
    tickerCounter = 1   'ticker counter used to identify correct cells to input ticker and total volume

    
    'Loop to traverse rows of Data
    Do Until IsEmpty(Current.Cells(i, 1))
    
    'assigning ticker, nextTicker, and vol values of new row and adding vol to totVol
        
        ticker = Current.Cells(i, 1).Value
        nextTicker = Current.Cells(i + 1, 1).Value
        vol = Current.Cells(i, 7).Value
        totVol = totVol + vol
        
    'assign open price if beginning of worksheet
        If (i = 2) Then
            openPrice = Current.Cells(i, 3).Value
        End If
        
    'If1: Check if ticker is different from next ticker
        If (ticker <> nextTicker) Then
            
            'assign close price
            closePrice = Current.Cells(i, 6).Value
            
            'Error check for zero values of open price to avoid division by 0 for runtime: overflow error
                If (openPrice = 0) Then
                    yearlyChange = 0
                    yearlyPercentChange = 0
                Else
                    yearlyChange = closePrice - openPrice
                    yearlyPercentChange = yearlyChange / openPrice
                End If
                
            'Print ticker, yearly change, yearly percentage change, and total volume to table
            'printTicker tickerCounter, ticker, yearlyChange, yearlyPercentChange, totVol
                Current.Cells(tickerCounter + 1, 9).Value = ticker
                Current.Cells(tickerCounter + 1, 10).Value = yearlyChange
                Current.Cells(tickerCounter + 1, 11).Value = FormatPercent(yearlyPercentChange, 2)
                Current.Cells(tickerCounter + 1, 12).Value = totVol
            
            If (yearlyPercentChange > yearlyPercentChangeMax) Then
                yearlyPercentChangeMax = yearlyPercentChange
                maxTicker = ticker
            End If
            
            If (yearlyPercentChange < yearlyPercentChangeMin) Then
                yearlyPercentChangeMin = yearlyPercentChange
                minTicker = ticker
            End If
            
            If (totVol > volMax) Then
                volMax = totVol
                volTicker = ticker
            End If
            

            '+1 stock counter to prevent overwriting summary
            tickerCounter = tickerCounter + 1
            
            'assign new open price for new stock in next row
            openPrice = Current.Cells(i + 1, 3).Value
            
            'reinitiate  total volume to 0 for new stock
            totVol = 0

        End If
        
    'Continuing Do loop
        i = i + 1
        Loop

Worksheets(1).Cells(2, 15).Value = maxTicker
Worksheets(1).Cells(2, 16).Value = FormatPercent(yearlyPercentChangeMax, 2)
Worksheets(1).Cells(3, 15).Value = minTicker
Worksheets(1).Cells(3, 16).Value = FormatPercent(yearlyPercentChangeMin, 2)
Worksheets(1).Cells(4, 15).Value = volTicker
Worksheets(1).Cells(4, 16).Value = volMax

'Worksheet Loop next
Next
  
MsgBox ("Macro Completed")

End Sub
