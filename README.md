# Stock-Chart in tkinter
## Introdution
本專案使用tkinter設計視窗介面，使用yfinance抓取全球股票數據，使用matplotlib和mplfinance繪製股票相關圖表，如趨勢圖、K線圖、歷史股利等。

This project uses tkinter to design the window interface, uses yfinance to capture global stock data, and uses matplotlib and mplfinance to draw stock-related charts, such as trend charts, K-line charts, and historical dividends.

## Requiresment
In requiresment.txt:
```
tk==0.1.0
tkcalender==1.6.1
matplotlib==3.8.2
mplfinance==0.12.10b0
```
## How to use
首先,執行stock.py程式,將會彈出一個操作視窗。接著,在該視窗中輸入所欲查詢的股票代號,並選定想要查看的日期範圍及圖表類型,包括趨勢圖、K線圖以及歷史股利圖等。完成上述設定後,點選「送出」按鈕,即可呈現您選擇的日期範圍間的最低與最高收盤價、最高與最低價、平均成交量及報酬率，還有您所需的股票資訊圖表。

此外,若您希望將查詢結果存為圖片檔案,可於圖表下方指定儲存路徑,再點選「儲存圖表」按鈕,即可將圖表下載至您的電腦中,以備後續使用。整個操作流程簡單便捷,讓您輕鬆掌握股市動態。

First, execute the stock.py program, and an operation window will pop up. Then, enter the stock code you want to query in the window, and select the date range and chart type you want to view, including trend charts, K-line charts, and historical dividend charts. After completing the above settings, click the "Send" button to display the lowest and highest closing prices, highest and lowest prices, average trading volume and return rate during the date range you selected, as well as the stock information charts you need.

In addition, if you want to save the query results as an image file, you can specify the storage path below the chart, and then click the "Save Chart" button to download the chart to your computer for subsequent use. The entire operation process is simple and convenient, allowing you to easily grasp the dynamics of the stock market.
## Demo
https://github.com/charley12009/Stock-Chart_in_tkinter/assets/76769844/5172d9dd-eada-426b-b380-0e7631d0e9fa

