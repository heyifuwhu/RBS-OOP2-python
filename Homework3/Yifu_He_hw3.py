# -*- coding: utf-8 -*-
"""
Spyder Editor
Yifu Jason He
This is a temporary script file.
"""

class Account(object):
    def __init__(self, name_):
        self.name = name_
        self.cash = 0
        self.real_estate = RealEstate()
        self.stocks = Stock()
    
    def __eq__(self,acc2):
        if self.name == acc2.name:
            return True
        else:
            return False
    
    def __str__(self):
        string = "-------------------------------------------------------------\n"
        string += "Account Name: {}\n".format(self.name)
        string += "Cash Balance: {}\n".format(self.cash)
        string += "{}".format(self.real_estate)
        string += "{}".format(self.stocks)
        string += "-------------------------------------------------------------"
        return string
    
    def save(self,amount):
        if amount < 0:
            raise Exception("Amount should be positive. The amount is {}".format(amount))
        self.cash += amount
    
    def withdraw(self,amount):
        if amount < 0:
            raise Exception("Amount should be positive. The amount is {}".format(amount))
        if self.cash < amount:
            raise Exception("No enough deposit!")
        self.cash -= amount
        
    def buy_real_estate(self, address, price):
        self.withdraw(price)
        self.real_estate.buy(address,price)
        
    def sell_real_estate(self, address, price):
        self.save(price)
        self.real_estate.sell(address)
    
    def buy_stock(self,ticker, share,price):
        self.withdraw(share * price)
        self.stocks.buy1(ticker, share, price)
     
    def sell_stock(self,ticker, share,price):
        self.save(share * price)
        self.stocks.sell1(ticker, share, price)
    
    def merge_account(self,account2, name ):
        self.name = name
        self.cash += account2.cash
        self.real_estate.merge(account2.real_estate)
        self.stocks.merge1(account2.stocks)
    
class RealEstate(object):
    def __init__(self):
        self.pool = dict()
    
    def __str__(self):
        string = "Real Estate:\n"
        for k,v in self.pool.items():
            string  = string + "Address: {}   ".format(k) + "Price: {}\n".format(v)
        return string
    
    def get_price(self,address):
        if address not in self.pool:
            raise Exception("This account don't own this real estate: {}".format(address))
        return self.pool[address]
    
    def buy(self, address, price):
        if price < 0:
            raise Exception("Real Estate price cannot be negtive. The prices is {}".format(price))
        self.pool[address] = price
    
    def sell(self,address):
        if address not in self.pool:
            raise Exception("This account don't own this real estate: {}".format(address))
        else:
            del self.pool[address]
    def merge(self,real_estate2):
        self.pool.update(real_estate2.pool)

class Stock(object):
    def __init__(self):
        self.portfolio = dict()
    
    def __str__(self):
        string ="Stock Portfolios:\n"
        for k, v in self.portfolio.items():
            string = string + "Stock: {}   ".format(k)+"share: {}   ".format(v[0])+"total cost: {}\n".format(v[1])
        return string 
    
    def buy1(self, ticker, shares, price):
        if ticker not in self.portfolio:
            self.portfolio[ticker] = [shares, price * shares]
        else:
            new_share = shares + self.portfolio[ticker][0]
            new_cost = shares * price + self.portfolio[ticker][1]
            self.portfolio[ticker] = [new_share, new_cost]
            
    def sell1(self, ticker, shares, price):
        if ticker not in self.portfolio:
            raise Exception("Ticker ({}) not in portfolio".format(ticker))
        elif share > self.portfolio[ticker][0]:
            raise Exception("Ticker ({}) don't have enough shares".format(ticker))
        else:
            new_cost = self.portfolio[ticker][1] - shares * (self.portfolio[ticker][1]/self.portfolio[ticker][0])
            new_share = self.portfolio[ticker][0] - shares
            self.portfolio[ticker] = [new_share, new_cost]
            
    def merge1(self,stock2):
        for key,value in stock2.portfolio.items():
            if key not in self.portfolio:
                self.portfolio[key] = value
            else:
                self.portfolio[key][0] += value[0]
                self.portfolio[key][1] += value[1]
    def move_add(self,ticker,share):
        if ticker not in self.portfolio:
            self.portfolio[ticker] = [share, 0]
        else:
            self.portfolio[ticker][0] = share + self.portfolio[ticker][0]
    def move_sub(self,ticker,share):
        if ticker not in self.portfolio:
            raise Exception("Ticker ({}) not in portfolio".format(ticker))
        elif share > self.portfolio[ticker][0]:
            raise Exception("Ticker ({}) don't have enough shares".format(ticker))
        else:
            self.portfolio[ticker][0] = self.portfolio[ticker][0] - share
    
           
if __name__ =="__main__":
    try:
        print("Create an Account Book as dictionary\n")
        account_book = dict() 
        with open("input.txt") as input_file:
            print("Begin to read transactions from input.txt file.....\n")
            num = 1
            for line in input_file:
                print("transaction {}:   ".format(num),line[:-1])
                num +=1
                command = line[:-1].split(',')
                for i in range(len(command)):
                    command[i] = command[i].strip()
                if command[0] == "Cp":
                    account_book[command[1]] = Account(command[1])
                elif command[0] == "Bs":
                    temp, ticker, share, price = account_book[command[4]],command[1],float(command[2]), float(command[3])
                    temp.buy_stock(ticker, share, price)
                elif command[0] == "Ss":
                    temp, ticker, share, price = account_book[command[4]],command[1],float(command[2]), float(command[3])
                    #account_book[command[4]].sell_stock(ticker, share, price)
                    temp.sell_stock(ticker, share, price)
                elif command[0] == "Mg":
                    if (command[1] not in account_book) or (command[2] not in account_book):
                        raise Exception("Don't have this account in account book")
                    else:
                        temp1,temp2,name = account_book[command[1]],account_book[command[2]],command[3]
                        temp1.merge_account(temp2,name)
                        account_book[name] = temp1
                        del account_book[command[1]]
                        del account_book[command[2]]
                    
                elif command[0] == "Dp":
                    if command[1] not in account_book:
                        raise Exception("Don't have this account {}".format(command[1]))
                    else:
                        temp, amount = account_book[command[1]], float(command[2])
                        temp.save(amount)
                elif command[0] == "Wd":
                    if command[1] not in account_book:
                        raise Exception("Don't have this account {}".format(command[1]))
                    else:
                        temp, amount = account_book[command[1]], float(command[2])
                        temp.withdraw(amount)
                elif command[0] == "Br":
                    if command[3] not in account_book:
                        raise Exception("Don't have this account {}".format(command[3]))
                    else:
                        temp, address,price = account_book[command[3]], command[1], float(command[2])
                        temp.buy_real_estate(address,price)
                elif command[0] == "Sr":
                    if command[3] not in account_book:
                        raise Exception("Don't have this account {}".format(command[1]))
                    else:
                        temp, address,price = account_book[command[3]], command[1], float(command[2])
                        temp.sell_real_estate(address,price)
                elif command[0] == "Xf":
                    if (command[1] not in account_book) or (command[2] not in account_book):
                        raise Exception("Don't have this account in account book")
                    else:
                        temp1,temp2 = account_book[command[1]],account_book[command[2]]
                        amount = float(command[3])
                        temp1.withdraw(amount)
                        temp2.save(amount)
                elif command[0] == "Xr":
                    if (command[1] not in account_book) or (command[2] not in account_book):
                        raise Exception("Don't have this account in account book")
                    else:
                        temp1,temp2 = account_book[command[1]],account_book[command[2]]
                        address = command[3]
                        price = temp1.real_estate.get_price(address)
                        temp1.sell_real_estate(address,price)
                        temp1.withdraw(price)
                        temp2.save(price)
                        temp2.buy_real_estate(address,price)
                elif command[0] == "Xs":    
                    if (command[1] not in account_book) or (command[2] not in account_book):
                        raise Exception("Don't have this account in account book")
                    else:
                        temp1,temp2 = account_book[command[1]],account_book[command[2]]
                        ticker,share = command[3],float(command[4])
                        
                        temp1.stocks.move_sub(ticker,share)
                        temp2.stocks.move_add(ticker,share)
                print("Print the information of current account book")
                for value in account_book.values():
                    print(value)     
        output = open("output.txt","w")
        for value in account_book.values():
            print(value,file=output)
        output.close()
        print("\nFinish Transaction \n")
        print("Begin to write final account information into output.txt file......\n")
    except Exception as e:
        print("\nError handleing: "+str(e))
        print("Error Input, quit!")
    finally:
        print("Finished")