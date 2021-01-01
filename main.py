from danawa import DanawaSearch
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas
import webbrowser


# 웹 크롤러 생성
danawa_control = DanawaSearch()

# 다이얼로그 생성
window = Tk()
window.title("다나와 최저가 모니터")
window.geometry("640x400+100+100")
window.resizable(False, False)

# csv 파일 열기
csv_file = ''
while csv_file == '':
    csv_file = filedialog.askopenfilename(initialdir='/', title='항목/URL이 담긴 csv 파일을 선택하세요.', filetypes=[("csv files", "*.csv")])
data = pandas.read_csv(csv_file, names=['항목', 'URL'], encoding='UTF-8')

# 탭 생성
tabcontrol = ttk.Notebook(window)
index_length = len(data['항목'].values)
tab = [ttk.Frame(tabcontrol) for i in range(index_length)]
for i in range(index_length):
    tabcontrol.add(tab[i], text=data['항목'].values[i])
tabcontrol.pack(expand=1, fill="both")

# 가격 크롤링
product_data = danawa_control.get_data(data['URL'].values)

for i in range(index_length):
    product_name = StringVar()
    product_name.set(product_data[i]['product_name'])
    Entry(tab[i], textvariable=product_name, width=50, fg="black", bg="white", bd=0, state="readonly", font=("맑은 고딕", 15, "bold"), justify='left').place(x=10, y=5)

    Label(tab[i], text="가   격:", font=("맑은 고딕", 13)).place(x=10, y=40)
    is_cash = StringVar()
    is_cash.set(product_data[i]['is_cash'])
    Entry(tab[i], textvariable=is_cash, width=5, fg="black", bg="white", bd=0, state="readonly", font=("맑은 고딕", 13)).place(x=70, y=42)
    Label(tab[i], text="원", font=("맑은 고딕", 13), justify='right').place(x=220, y=40)
    product_price = StringVar()
    product_price.set(product_data[i]['product_price'])
    Entry(tab[i], textvariable=product_price, width=10, fg="black", bg="white", bd=0, state="readonly", font=("맑은 고딕", 13), justify='right').place(x=132, y=42)

    Label(tab[i], text="배송비:", font=("맑은 고딕", 13)).place(x=10, y=70)
    ship_price = StringVar()
    ship_price.set(product_data[i]['ship_price'])
    Entry(tab[i], textvariable=ship_price, width=10, fg="black", bg="white", bd=0, state="readonly", font=("맑은 고딕", 13), justify='right').place(x=149, y=72)
    Button(tab[i], text="다나와 사이트", command=lambda: webbrowser.open(data['URL'].values[i], new=1)).place(x=300, y=40)
    Button(tab[i], text="최저가 사이트", command=lambda: webbrowser.open(product_data[i]['link'], new=1)).place(x=300, y=70)
    # Button(tab[i], text="최저가 사이트", command=lambda: webbrowser.open(low_price_url, new=1)).place(x=300, y=70)

window.mainloop()
del danawa_control