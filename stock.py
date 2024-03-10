import tkinter as tk
from tkinter import ttk,filedialog
import yfinance as yf
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import sys
import matplotlib.dates as mdates
def download():
    selected_value = val.get()
    path = path_var.get()
    if selected_value == 'k':
        canva_clean()        
        try:
            symbol = symbol_entry.get()
            start_date = start_date_entry.get_date()
            end_date = end_date_entry.get_date()
            plot_stock_trend_k(symbol, start_date, end_date)
        except IndexError:
            error_message()
    elif selected_value == 'trend':
        canva_clean()        
        try:
            symbol = symbol_entry.get()
            start_date = start_date_entry.get_date()
            end_date = end_date_entry.get_date()
            plot_stock_trend(symbol, start_date, end_date)
        except IndexError:
            error_message()
    elif selected_value == 'd':
        canva_clean()        
        try:
            symbol = symbol_entry.get()
            start_date = start_date_entry.get_date()
            end_date = end_date_entry.get_date()
            plot_stock_div(symbol, start_date, end_date)
        except IndexError:
            error_message()
    else:
        tk.messagebox.showerror(title='錯誤', message='請選擇要查看的圖表類型')
def canva_clean():
    # 清除舊的 Canvas
    canvas_widgets = window.grid_slaves(row=9, column=0)
    if canvas_widgets:
        canvas_widget = canvas_widgets[0]
        canvas_widget.grid_forget()
def stock_info(df_new):
    # 將 DataFrame 轉換為 mplfinance 支持的格式
    mpf_df = df_new[['Open', 'High', 'Low', 'Close', 'Volume']]
    mpf_df.index.name = 'Date'
    close_data = mpf_df['Close']
    min_close_data = close_data.min()
    min_close_labels.config(text=f'最低收盤價: {min_close_data:.2f}')

    max_close_data = close_data.max()
    max_close_labels.config(text=f'最高收盤價: {max_close_data:.2f}')

    high_data = mpf_df['High']
    max_high_data = high_data.max()
    max_high_labels.config(text=f'最高價: {max_high_data:.2f}')

    low_data = mpf_df['Low']
    min_low_data = low_data.min()
    min_low_labels.config(text=f'最低價: {min_low_data:.2f}')

    volume_data = mpf_df['Volume']
    avg_volume_data = volume_data.mean()
    avg_volume_labels.config(text=f'平均成交量: {avg_volume_data:.2f}')

    initial_price = df_new['Close'].iloc[0]
    final_price = df_new['Close'].iloc[-1]
    returns = ((final_price - initial_price) / initial_price) * 100
    returns_labels.config(text=f'報酬率: {returns:.2f}%')
def error_message():
    tk.messagebox.showerror(title='錯誤', message='請輸入正確的股票代號')
def plot_stock_div(symbol,start_date,end_date):
    canva_clean()
    stock_data = yf.download(symbol, start=start_date, end=end_date, actions=True)
    
    # 選擇時間範圍
    df_new = stock_data[(stock_data.index > str(start_date)) & (stock_data.index < str(end_date))]
    dividends= df_new['Dividends']
    
    df_new.info()
    stock_info(df_new)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 4)
    ax.bar(dividends.index, dividends)
    
    # 設置圖表標題和軸標籤
    ax.set_title('Dividends')
    ax.set_xlabel('Date')
    ax.set_ylabel('Dividends')
    # ax.legend()

    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=9,column=0,columnspan=2)
    
    path_label = tk.Label(window,text="下載路徑：")
    path_label.grid(row=10, column=0,columnspan=2) 
    path_entry = tk.Entry(window, textvariable=path_var, state='disabled', width=40)
    path_entry.grid(row=11, column=0,columnspan=2)
    browse_button = tk.Button(window, text="瀏覽", command=select_path)
    browse_button.grid(row=11, column=1,columnspan=2)
    save_fig_button = ttk.Button(window, text='儲存圖表', command=lambda: save_figure(fig, symbol, '_歷史股利'))
    save_fig_button.grid(row=12, column=0,columnspan=2)
def plot_stock_trend_k(symbol, start_date, end_date):
    canva_clean()
    # 使用 yfinance 獲取股價數據
    stock_data = yf.download(symbol, start=start_date, end=end_date,actions=True)

    # 選擇時間範圍
    df_new = stock_data[(stock_data.index > str(start_date)) & (stock_data.index < str(end_date))]
    stock_info(df_new)
    # 將 DataFrame 轉換為 mplfinance 支持的格式
    mpf_df = df_new[['Open', 'High', 'Low', 'Close', 'Volume']]    
    # 繪製 K 線圖
    if '.TW' in symbol:
        mc = mpf.make_marketcolors(up='r',down='g')
        s  = mpf.make_mpf_style(marketcolors=mc)
        fig, axlist = mpf.plot(mpf_df, type='candle',style=s, volume=True, returnfig=True)
    else:
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        fig, axlist = mpf.plot(mpf_df, type='candle',style=s, volume=True, returnfig=True)
    fig.set_size_inches(10, 5)
    # 設定圖形標題
    fig.suptitle(f"{symbol}")

    # 在 Tkinter 視窗中顯示 K 線圖
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=9, column=0,columnspan=2)
    path_label = tk.Label(window,text="下載路徑：")
    path_label.grid(row=10, column=0,columnspan=2) 
    path_entry = tk.Entry(window, textvariable=path_var, state='disabled', width=40)
    path_entry.grid(row=11, column=0,columnspan=2)
    browse_button = tk.Button(window, text="瀏覽", command=select_path)
    browse_button.grid(row=11, column=1,columnspan=2)
    save_fig_button = ttk.Button(window, text='儲存圖表', command=lambda: save_figure(fig, symbol, '_K線圖'))
    save_fig_button.grid(row=12, column=0, columnspan=2)
def plot_stock_trend(symbol,start_date,end_date):
    canva_clean()
    stock_data = yf.download(symbol,start=start_date,end=end_date,actions=True)
    # 選擇時間範圍
    df_new = stock_data[(stock_data.index > str(start_date)) & (stock_data.index < str(end_date))]
    print(df_new.head())
    stock_info(df_new)    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 4)
    ax.plot(df_new['Close'],label=symbol)    
    ax.set_title(f'{symbol}')
    ax.set_xlabel('Date')
    
    ax.set_ylabel('Closing Price')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=9,column=0,columnspan=2)
    
    path_label = tk.Label(window,text="下載路徑：")
    path_label.grid(row=10, column=0,columnspan=2) 
    path_entry = tk.Entry(window, textvariable=path_var, state='disabled', width=40)
    path_entry.grid(row=11, column=0,columnspan=2)
    browse_button = tk.Button(window, text="瀏覽", command=select_path)
    browse_button.grid(row=11, column=1,columnspan=2)
    save_fig_button = ttk.Button(window, text='儲存圖表', command=lambda: save_figure(fig, symbol, '_趨勢圖'))
    save_fig_button.grid(row=12, column=0,columnspan=2)

def select_path():
    path = filedialog.askdirectory()
    path_var.set(path)
def save_figure(fig, symbol, chart_type):
    try:
        fig.savefig(f"{path_var.get()}/{symbol}{chart_type}.png")
        tk.messagebox.showinfo(title='成功', message='圖表已儲存至指定路徑')
    except Exception as e:
        tk.messagebox.showerror(title='錯誤', message=f'儲存圖表失敗：{e}')
window = tk.Tk()
window.title('全球股價趨勢')

path_var = tk.StringVar()
path_var.set("")
val = tk.StringVar(value=None)

symbol_label = ttk.Label(master=window,text='股票代號')
symbol_label.grid(row=0,column=0) # 0 0

symbol_entry = ttk.Entry(window)
symbol_entry.grid(row=0,column=1) # 0 1

start_date_label = ttk.Label(master=window,text='開始日期')
start_date_label.grid(row=1,column=0) # 1 0

start_date_entry = DateEntry(window,width=12,background='darkblue',foreground='white',date_pattern='yyyy-mm-dd',locale='zh_TW.UTF-8')
start_date_entry.grid(row=1,column=1) # 1 1

end_date_label = ttk.Label(master=window,text='結束日期')
end_date_label.grid(row=2,column=0) # 2 0

end_date_entry = DateEntry(window,width=12,background='darkblue',foreground='white',date_pattern='yyyy-mm-dd',locale='zh_TW.UTF-8')
end_date_entry.grid(row=2,column=1) # 2 1
radio_btn_tr = tk.Radiobutton(window, text='趨勢圖',variable=val, value='trend')
radio_btn_tr.grid(row=3, column=0) # 3 0
radio_btn_tr.select()
radio_btn_k = tk.Radiobutton(window, text='k線圖',variable=val, value='k')
radio_btn_k.grid(row=3, column=1) # 4 0
radio_btn_d = tk.Radiobutton(window, text='歷史股利',variable=val, value='d')
radio_btn_d.grid(row=4, column=0,columnspan=2) # 5 0
min_close_labels = ttk.Label(master=window,text='')
min_close_labels.grid(row=5,column=0)  # 4 0
max_close_labels = ttk.Label(master=window,text='')
max_close_labels.grid(row=5,column=1)  # 4 1
max_high_labels = ttk.Label(master=window,text='')
max_high_labels.grid(row=6,column=0)  #5 0
min_low_labels = ttk.Label(master=window,text='')
min_low_labels.grid(row=6,column=1)  # 5 1
avg_volume_labels = ttk.Label(master=window,text='')
avg_volume_labels.grid(row=7,column=0)  # 6 0
returns_labels = ttk.Label(master=window,text='')
returns_labels.grid(row=7,column=1)  # 6 1
submit_button = ttk.Button(window,text='送出',command=download)
submit_button.grid(row=8,column=0, columnspan=2) # 7 0
window.protocol("WM_DELETE_WINDOW",lambda: sys.exit())
window.mainloop()
