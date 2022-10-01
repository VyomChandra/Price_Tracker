

import random
import requests
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from collections import defaultdict
from difflib import get_close_matches


root = Tk()

class PriceCompare:

    def __init__(self, master):
        
        self.productSearch = StringVar()
        self.flipkartVar = StringVar()
        self.amazonVar = StringVar()
        

        homeFrame = Frame(master, height='500', width='900')
        homeFrame.grid(row=0, column=0)
        homeFrame.grid_propagate(0)

        self.img = Image.open(r"img/homebg.png")
        self.img2 = ImageTk.PhotoImage(self.img)
        panel = Label(homeFrame, image=self.img2)
        panel.pack(side="top", fill="both", expand="yes")



        # label = Label(master, text='Enter the product')
        # label.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        entry = ttk.Entry(master, textvariable=self.productSearch, width=30, font = ('courier', 15, 'bold'))
        entry.focus_force()
        entry.place(x=350, y=274)

        style = Style()
        style.configure('TButton', font =
               ('calibri', 15, 'bold'),
                    borderwidth = '4')
        buttonSearch = Button(master, text='Search',  command=self.find, width=15)
        buttonSearch.place(x=750, y=270)

        
    def find(self):
        self.product = self.productSearch.get()
        self.productArr = self.product.split()
        self.nmb = 1
        self.key = ""
        self.titleFlipkartVar = StringVar()
        self.titleAmznVar = StringVar()
        self.variableAmzn = StringVar()
        self.variableFlip = StringVar()

        for word in self.productArr:
            if self.nmb == 1:
                self.key = self.key + str(word)
                self.nmb += 1

            else:
                self.key = self.key + '+' + str(word)

        self.window = Toplevel(root)
        self.window.title('Product Price Comparison')

        homeFrame = Frame(self.window, height='500', width='900')
        homeFrame.grid(row=0, column=0)
        homeFrame.grid_propagate(0)

        self.mainimg = Image.open(r"img/mainbg.png")
        self.mainimg2 = ImageTk.PhotoImage(self.mainimg)
        bgpanel = Label(homeFrame, image=self.mainimg2)
        bgpanel.pack(side="top", fill="both", expand="yes")


        entry_flipkart = Entry(self.window, textvariable=self.flipkartVar)
        entry_flipkart.place(x=680, y=350)

        entry_amzn = Entry(self.window, textvariable=self.amazonVar)
        entry_amzn.place(x=160, y=350)

        self.priceFlipkart(self.key)
        self.priceAmzn(self.key)

        try:
            self.variableAmzn.set(self.matches_amzn[0])
        except:
            self.variableAmzn.set('Product not available')
        try:
            self.variableFlip.set(self.matches_flip[0])
        except:
            self.variableFlip.set('Product not available')


        s = ttk.Style()
        s.configure('TMenubutton', font=("Cambria", 12, "bold"), anchor = 'w'  )



        option_flip = ttk.OptionMenu(self.window, self.variableFlip, *self.matches_flip, style='TMenubutton') # flipkart menu
        option_flip.configure(width=50)
        option_flip.place(x=758, y=225, anchor='center')


        option_amzn = ttk.OptionMenu(self.window, self.variableAmzn, *self.matches_amzn, style='TMenubutton')
        option_amzn.configure(width=50)
        option_amzn.place(x=250, y=225, anchor='center')

        button_search = Button(self.window, text='Search', command=self.search, width=20)
        button_search.place(x=396, y=19)

        button_amzn_visit = Button(self.window, text='Visit Site', command=self.visitAmzn,  width=20)
        button_amzn_visit.place(x=135, y=448)

        button_flip_visit = Button(self.window, text='Visit Site', command=self.visitFlip, width=20)
        button_flip_visit.place(x=648, y=448)

    def priceFlipkart(self, key):
        url_flip = 'https://www.flipkart.com/search?q=' +str(key) +'&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
        map = defaultdict(list)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        source_code = requests.get(url_flip, headers=self.headers)
        soup = BeautifulSoup(source_code.text, "html.parser")
        self.opt_title_flip = StringVar()
        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title, price, link = None, 'Currently Unavailable', None
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:]
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home + l.get('href')
            map[title] = [price, link]

        user_input = self.productSearch.get().title()
        self.matches_flip = get_close_matches(user_input, map.keys(), 20, 0.1)
        self.looktable_flip = {}
        for title in self.matches_flip:
            self.looktable_flip[title] = map[title]

        try:
            self.opt_title_flip.set(self.matches_flip[0])
            self.flipkartVar.set(self.looktable_flip[self.matches_flip[0]][0] + '.00')
            self.link_flip = self.looktable_flip[self.matches_flip[0]][1]
        except IndexError:
            self.opt_title_flip.set('Product not found')

    def priceAmzn(self, key):
        url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

        # Faking the visit from a browser
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        map = defaultdict(list)
        home = 'https://www.amazon.in'
        proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                        "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                        "134.213.29.202:4444"]
        proxies = {'https': random.choice(proxies_list)}
        source_code = requests.get(url_amzn, headers=headers)
        plain_text = source_code.text
        self.opt_title = StringVar()
        self.soup = BeautifulSoup(plain_text, "html.parser")
        for html in self.soup.find_all('div', {'class': 'sg-col-inner'}):
            title, link,price = None, None,None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text
            for l in html.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                link = home + l.get('href')
            if title and link:
                map[title] = [price, link]
        user_input = self.productSearch.get().title()
        self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        self.looktable = {}
        for title in self.matches_amzn:
            self.looktable[title] = map[title]
        self.opt_title.set(self.matches_amzn[0])
        self.amazonVar.set(self.looktable[self.matches_amzn[0]][0] + '.00')
        self.product_link = self.looktable[self.matches_amzn[0]][1]

    def search(self):
        amzn_get = self.variableAmzn.get()
        self.opt_title.set(amzn_get)
        product = self.opt_title.get()
        price, self.product_link = self.looktable[product][0], self.looktable[product][1]
        self.amazonVar.set(price + '.00')
        flip_get = self.variableFlip.get()
        flip_price, self.link_flip = self.looktable_flip[flip_get][0], self.looktable_flip[flip_get][1]
        self.flipkartVar.set(flip_price + '.00')

    def visitAmzn(self):
        webbrowser.open(self.product_link)

    def visitFlip(self):
        webbrowser.open(self.link_flip)

if __name__ == "__main__":
    c = PriceCompare(root)
    root.title('Product Price Comparison')
    root.mainloop()
