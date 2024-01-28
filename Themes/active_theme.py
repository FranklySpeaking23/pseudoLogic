#WARNING: Changing anything in the "fields" part can mess up old files, recieved files or files send to other people.
#WARNING: To prevent this from happening, you should always use the same "field" settings. Especially for "margins", "widths", etc...

#colors
FIELD = (20, 100, 30) #default input field
IF_STATEMENT = (30, 80, 40) #if-statement
IF_THAN_LINE = (10, 50, 30) #the line between the if-than and if-statement fields
IF_ELSE_LINE = (10, 50, 30) #the line between the if-than and if-statement fields
IF_THAN = (30, 80, 40) #the "than" triangle of the if statement
IF_ELSE = (30, 80, 40) #the "else" triangle of the if statement
SUB_IF_TRUE_STATEMENT = (30, 80, 40) #every field inside of the if-statement
SUB_IF_FALSE_STATEMENT = (30, 80, 40) #every field inside of the if-statement
WHILE_STATEMENT = (40, 60, 50) #repeating-statement
SUB_WHILE_STATEMENT = (40, 60, 50) #every field inside of the repeating-statement
FUNCTION = (50, 40, 45) #the color of a function field
SUB_FUNCTION = (50, 40, 45) #the color of a field inside a function
HOVER = (125, 150, 200) #on mouse hover
SELECTED = (100, 100, 100) #when selected
TEXT = (255, 255, 255) #text
BACKGROUND = (10, 40, 10) #background

#window
WIDTH = 900 #at least 300
HEIGHT = 500
FPS = 60 #frames per second
TITLE = "pseudoLogic" #window title
CHANGE_Y_POS = 15 #the amount of pixels moved up/down when scrolling

#patern
BACKGROUND_PATERN = "fancy_lines" #options are: diagonal_lines, triangle_lines, fancy_lines, no_lines
BACKGROUND_LINE_COLOR = (255, 255, 255)

#save ad load
SAVE_NAME_FILE = "ustruct2_json_save" #the default name to save a file
SAVE_NAME_IMAGE = "ustruct2_png_save" #the default name to save an image
SAVE_DIR_FILE = "" #the default directory to save the file --> on windows use two \ for each folder, for macos and linux use a single /
SAVE_DIR_IMAGE = "" #the default directory to save the image --> on windows use two \ for each folder, for macos and linux use a single /
LOAD_NAME_FILE = "" #the default name for the file you want to load
LOAD_DIR_FILE = "" #the default directory to load a project --> on windows use two \ for each folder, for macos and linux use a single /

#text
BUTTONS_FONT = "Verdana" #buttons on the side font --> all installed fonts are possible
BUTTONS_FONT_SIZE = 20 #buttons on the side --> recommended: 20
FIELDS_FONT = "Verdana" #input fields font --> all installed fonts are possible
FIELDS_FONT_SIZE = 12 #input fields --> recommended: 12
FUNCTION_FONT_SIZE = 17


#fields
FIELD_HEIGHT = 50 #the height of a field
MARGIN_HEIGHT = 15 #the vertical space in between of fields --> needs to be at least 0
MARGIN_WHILE_STATEMENT = 30 #the horizontal gap for the fields in the while-statement
WIDTH_SIDEBAR_WHILE_STATEMENT = 15 #the width of the sidebar of a while-statement --> needs to be at least 1, can't be bigger than MARGIN_WHILE_STATEMENT
MARGIN_IF_STATEMENT_LEFT = 30 #the horizontal gap for the start of the True statement of the if-statement
MARGIN_IF_STATEMENT_MIDDLE = 10 #the open space between the two under parts of the if-statement --> needs to be at least 1
IF_LINE_WIDTH = 5 #the width of the line between the if-statement and the if-than and if-else fields
BORDER = 0 #the border around fields and buttons --> to use programmed borders: None
ROUNDING = 5 #the rounding of fields and buttons
IF_STATEMENT_TEXT = "Als " #the text that appears by default in the main box of the if-statement
IF_STATEMENT_LEFT = "T" #the text that appears by default in the upper left box of the if-statement
IF_STATEMENT_RIGHT = "F" #the text that appears by default in the upper right box of the if-statement
IF_STATEMENT_B_LEFT = "" #the text that appears by default in the lower left box of the if-statement
IF_STATEMENT_B_RIGHT = "" #the text that appears by default in the lower right box of the if-statement
WHILE_STATEMENT_TEXT = "terwijl " #the text that appears by default in the main box of the repeating-statement
WHILE_STATEMENT_LOWER_TEXT = "" #the text that appears by default in the first repeating field of the repeating-statement
FUNCTION_TEXT = ""
FUNCTION_LOWER_TEXT = ""
DEFAULT_TEXT = "" #the text that appears by default in a normal field
SAVE_AS_IMAGE = "I" #the text for the save as image button --> one character recommended
SAVE_AS_JSON = "J" #the text for the normal save as button --> one character recommended
LOAD_JSON = "O" #the text for the open file button --> one character recommended
FIELD_DEFAULT = "D" #the text for the make a field button --> one character recommended
FIELD_IF_STATEMENT = "I" #the text for the make an if-statement button --> one character recommended
FIELD_WHILE_STATEMENT = "W" #the text for the make a repeating-statement button --> one character recommended
FIELD_FUNCTION = "F"
FIELD_DELETE = "T" #the text for the delete current field button