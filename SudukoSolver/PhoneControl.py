import ppadb.client as Client
from PIL import Image
import Board
import numpy as np


def countPixels(pixels):
    counter = 0
    for i in pixels:
        if i == (44, 44, 44, 255):
            counter += 1
    return counter


# If you play Multi-Player so change to True, if Single-Player so False ------------------------------------------------
isMultiPlayer = True
if isMultiPlayer:
    player_grid = (36, 550, 1044, 1558)
    player_square = 566
else:
    player_grid = (36, 477, 1044, 1485)
    player_square = 493

numDic = {
    0: 0,
    503: 1,
    839: 2,
    856: 3,
    893: 4,
    935: 5,
    953: 6,
    621: 7,
    1066: 8,
    959: 9, }

# Phone connect
adb = Client.Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]

# Take a screen-shot
image = device.screencap()
open('screen1.png', 'wb').write(image)
image = Image.open('screen1.png')

# Crop the screen-shot to the grid
cropped_image = image.crop(player_grid)
cropped_image.save('C:/Users/reuve/PycharmProjects/SudukoSolver/screen2.png', 'PNG')

full_board = Board.board(np.zeros((9, 9)))  # Create a board and fill it with solution
empty_board = Board.board(np.zeros((9, 9)))  # Create a board and fill it like the Sudoku

# Copy the board from phone to program
for x in range(9):
    for y in range(9):                                                  # Crop the grid to square at X and Y position {
        square = cropped_image.crop((112 * x, 112 * y, 112 * (x + 1), 112 * (y + 1)))                               # -
        square.save('C:/Users/reuve/PycharmProjects/SudukoSolver/square.png', 'PNG')                                # -
        test = Image.open('square.png')                                                                             # }
        pixels = list(test.getdata())        # Set the square to RGB
        num = numDic[countPixels(pixels)]    # Print the number through the dictionary
        full_board.setNumber(num, y, x)      # Set the number to the full board
        empty_board.setNumber(num, y, x)     # Set the number to the empty board

full_board.solve()  # Solve the full board

# Place the numbers to the phone
for y in range(9):
    for x in range(9):
        if empty_board.board[y][x] == 0:  # Solve the square only if there is no number
            device.shell('input touchscreen swipe %s %s %s %s 0' % ((122*x)+52, (122*y)+player_square, (122*x)+52,
                                                                    (122*y)+player_square))
            device.shell(f'input touchscreen swipe %s 2000 %s 2000 0' % (str(((120*(full_board.board[y][x]-1))+60)),
                                                                         (str(((120*(full_board.board[y][x]-1))+60)))))


'Screen Touch'
#device.shell('input touchscreen swipe 200 1000 700 1000 time')

'Pointer Setting'
#device.shell(f'settings put system pointer_location 1')