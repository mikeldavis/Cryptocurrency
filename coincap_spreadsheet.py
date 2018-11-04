########################################################################
##### This script uses a text file named "portfolio.txt" as input  #####
##### and uses api.coinmarketcap.com/v2 to look up three variables #####
#####  'Name', 'Symbol', and 'Price' which are then written to a   #####
#####  spreadsheet named "cryptocurrencies.xlsx" into column 'A',  #####
#####  'B', and 'C', so each time you run it, you get up to date   #####
#####   prices for all the cryptocurrencies in your portfolio.     #####
##### YOU NEED TO CREATE "portfolio.txt" by typing in the SYMBOL   #####
#####   of the cryptocurrencies you own followed by a space and    #####
#####  the amount you own. This needs to be done only once before  #####   
#####         running the script for the first time.               #####
########################################################################
##### Since I keep different cryptos in different wallets and on   #####
#####  different exchanges, I have another spreadsheet that just   #####
#####    lists the exchange or wallet, and 3 variables: 'Name',    #####
##### 'Symbol', and 'Holdings'. I then calculate what my holdings  #####
#####  are currently worth by linking to "cryptocurrencies.xlsx"   #####
##### & multiplying 'Holdings' from this spreadsheet times 'Price' #####
#####              from "cryptocurrencies.xlsx".                   #####

########################################################################
#####   Thanks to Ian Annase for his great course on python!       #####
#####  I'm just re-cycling his code from the course with slight    #####
##### modifications. The course is available at Udemy (see link)   #####
#####   https://www.udemy.com/coinmarketcap/learn/v4/overview      #####
######################################################################## 
import xlsxwriter
import requests
import json
import os

convert = 'USD'
f = 1
#############################################################
#####  If you want the file named differently, replace  #####
####      'cryptocurrencies.xlsx' in the line below      ####
############################################################# 
crypto_workbook = xlsxwriter.Workbook('cryptocurrencies.xlsx')
crypto_sheet = crypto_workbook.add_worksheet()

crypto_sheet.write('A1', 'Name')
crypto_sheet.write('B1', 'Symbol')
crypto_sheet.write('C1', 'Price')

listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()
data = results['data']

ticker_url_pairs = {}
for currency in data:
	symbol = currency['symbol']
	url = currency['id']
	ticker_url_pairs[symbol] = url
 
with open("portfolio.txt") as inp:
	for line in inp:
		ticker, amount = line.split()
		ticker = ticker.upper()
		
		ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

		request = requests.get(ticker_url)
		results = request.json()

		currency = results['data'][0]
		name = currency['name']
		symbol = currency['symbol']
		quotes = currency['quotes'][convert]
		price = quotes['price']
			
		crypto_sheet.write(f,0,name)
		crypto_sheet.write(f,1,symbol)
		crypto_sheet.write(f,2,str(price))		

		f += 1
		
crypto_workbook.close()

