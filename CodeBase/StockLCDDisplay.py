import lcd
import time

lcd.lcd_init()

lcd.GPIO.output(lcd.LED_ON, True)
lcd.time.sleep(1)
lcd.GPIO.output(lcd.LED_ON, False)
lcd.time.sleep(1)
lcd.GPIO.output(lcd.LED_ON, True)
lcd.time.sleep(1)

def display(func):
    def wrapper(*args):
        lines = func(*args)
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string(lines[0],2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string(lines[1],2)
    return wrapper

@display
def display_stock(symbol,price,change):
    '''
        The goal of this function is to build the two lines that will hold
        the stock information. Determining the number of spaces in the line
        is important in order to center the data on the 16x2 LCD.
        
        What the lines contain:
        
        Line1: SYMBOL + SPACES + CURRENT_STOCK_PRICE
        Line2: Change: + SPACES + SIGN + CHANGE
    '''
    #Building Line 1
    formatted_price = '$' + ('%.2f' % float(price))
    spaces1 = 16 - len(str(symbol)) - len(formatted_price) - 4
    line1 = '|'+f'{symbol}'+'|'+' '*spaces1+'|'+formatted_price+'|'
    
    #Building Line 2
    #Get the Symbol (+ sign if the change is positive)
    symbol = ''
    if float(change) > 0:
        symbol = '+'
    else:
        symbol = ' '
        
    formatted_change = symbol + ('%.2f' % float(change))
    spaces2 = 16 - len('Change:') - 2 - len(formatted_change)
    line2 = f'|Change:'+ ' '*spaces2 + formatted_change +'|'
    
    #Return a tuple of both the lines to be used in the display function
    return (line1,line2)

@display
def display_iteration(timestamp,iteration):
    spaces1 = 1
    if iteration < 10:
        spaces1 += 1
    line1 = f'Iteration:'+' '*spaces1+f'{iteration}/24'
    
    spaces2 = 2
    if len(timestamp) < 5:
        spaces2 += 1
    line2 = f'Obtained:' + ' '*spaces2 + f'{timestamp}'
    return (line1,line2)

@display
def display_startup():
    line1 = 'Retrieving'
    line2 = 'Data'
    return (line1,line2)

@display
def display_inactive():
    line1 = 'Market Closed'
    line2 = 'Hours are 9-4'
    return (line1,line2)


if __name__ == '__main__':
    display_startup()
    time.sleep(5)
    display_inactive()