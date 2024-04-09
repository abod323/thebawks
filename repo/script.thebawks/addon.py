import xbmcgui
import xbmc
import math


# http request
import requests
import json
base_url='http://192.168.1.105:8000'
window = xbmcgui.Window(10000)
# Function to save the token to addon settings
def save_token(token):
    window.setProperty('token', token)

# Function to retrieve the token from addon settings
def get_token():
    return window.getProperty('token')
# # Function to get data from API
def login( username, password,mac):
    # API URL
    url = base_url+'/api/auth/login'
    
    # send post request with username and password
    response = requests.post(url, data={'username': username, 'password': password, 'mac':mac})
    
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)
        
        # Return the data
        return data
    else:
        # Return an error message
        data = json.loads(response.text)
        return data
        
    

# Function to show custom dialog for username and password input
def show_custom_dialog():
    # Create dialog window
    dialog = xbmcgui.Dialog()
    
    # Get username input
    username = dialog.input('Enter username')
    
    # Get password input (hidden)
    password = dialog.input('Enter password', type=xbmcgui.INPUT_ALPHANUM)
    
    # Format the message with username and password
    message = 'Username: {}, Password: {}'.format(username, password)
    
    # check if username and password are not empty
    if username and password:
        # Maximum number of retries
        max_retries = 5
        retry_delay = 1  # Delay in seconds between retries

        for retry_count in range(max_retries):
            mac_address = xbmc.getInfoLabel('Network.MacAddress')
            if mac_address != 'Busy':
                data = login(username, password,mac_address)
                
                if data['status'] == True:
                    
                    save_token(data['token'])
                    # Show success message
                    xbmc.executebuiltin('ActivateWindow(10000)')
                else:
                    # Show error message
                    dialog.ok('Error', data['message'])
                    
                break
            else:
                xbmc.sleep(retry_delay * 1000)
            
      

     
    else:
        # Show error message
        dialog.ok('Error', 'Username and password are required')

#login by mac address
def login_by_mac(mac):
    # API URL
    url = base_url+'/api/auth/login-mac'

    # send post request with username and password
    response = requests.post(url, data={'mac': mac})

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Return the data
        return data
    else:
        # Return an error message
        dialog = xbmcgui.Dialog()
        dialog.ok('Error', response.text)
    

# get mac address and login
def get_mac_and_login():
    # DialogProgress
    dialog = xbmcgui.DialogProgress()
    dialog.create('Logging in', 'Please wait...')
    # wait for 5 seconds
    xbmc.sleep(2000)

    # Maximum number of retries
    max_retries = 3000
    retry_delay = 1  # Delay in seconds between retries

    for retry_count in range(max_retries):
        mac_address = xbmc.getInfoLabel('Network.MacAddress')
        if mac_address != 'Busy'and mac_address != None:
            data = login_by_mac(mac_address)

            if data['status'] == True:
                save_token(data['token'])
                #close dialog
                dialog.close()
             
                xbmc.executebuiltin('ActivateWindow(10000)')
            else:
                # close dialog
                dialog.close()
                xbmc.executebuiltin('ActivateWindow(11150)')
           

            break
        else:
            xbmc.sleep(retry_delay * 1000)




# check if window is 11150
if xbmcgui.getCurrentWindowId() == 11150:
    show_custom_dialog()
elif xbmcgui.getCurrentWindowId() == 12999:
    get_mac_and_login()



def SlideButton():
    # Get the window
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

    # get clicked button id
    clicked_button_id = window.getProperty('clicked_button_id')

    dialog = xbmcgui.Dialog()
    if clicked_button_id != '': 
       clicked_button_id = int(clicked_button_id)
    # Get the button control
    button = window.getControl(clicked_button_id)
    
    # Get current position
    current_x, current_y = button.getPosition()
    
    # Define target position
    target_x = -330 if current_x == 0 else 0
    
    # Slide the button
    step = 100  # Increase step size for faster animation
    while current_x != target_x:
        if current_x < target_x:
            current_x = min(current_x + step, target_x)
        else:
            current_x = max(current_x - step, target_x)
        button.setPosition(current_x, current_y)
        xbmc.sleep(10)  # Decrease delay for faster animation
        if current_x == 0:
            #    
            # ActivateWindow(videos,plugin://plugin.video.themoviedb.helper?info=mdblist_toplists,return)
            plugin_url = 'plugin://plugin.video.seren'
            xbmc.executebuiltin('ActivateWindow(1151)')



# window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
# dialog = xbmcgui.Dialog()
# # window id
# dialog.ok('Window ID', '{}'.format(xbmcgui.getCurrentWindowId()))
# Call the function to slide the button
if xbmcgui.getCurrentWindowId() == 10000:
   SlideButton()


# if button is clicked 
if xbmcgui.getCurrentWindowId() == 11151:
    # Get the window
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    
    # Get the clicked button id
    clicked_button_id = window.getProperty('clicked_button_id')
    
    # if clicked button id == 20005 go home
    if clicked_button_id == '20005':
        xbmc.executebuiltin('ActivateWindow(videos,plugin://plugin.video.seren?action=showsHome)')

    if clicked_button_id == '20006':
        xbmc.executebuiltin('ActivateWindow(1152)')

    # if clicked button id == 20006 go to movies
    elif clicked_button_id == '20007':
        xbmc.executebuiltin('ActivateWindow(videos,plugin://plugin.video.seren?action=moviesHome)')

# def RotateButton():
#     # Get the window
#     window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

#     # Get the button control
#     button = window.getControl(20010)
    
#     # Get initial position of the button
#     initial_x, initial_y = button.getPosition()
    
#     # Define rotation parameters
#     rotation_radius = 50  # Radius of rotation circle (adjust as needed)
#     rotation_speed = 0.1  # Speed of rotation (adjust as needed)
#     rotation_angle = 0
    
#     # Rotate the button continuously
#     while True:
#         # Calculate new position using polar coordinates
#         new_x = initial_x + rotation_radius * math.cos(rotation_angle)
#         new_y = initial_y + rotation_radius * math.sin(rotation_angle)
        
#         # Set the new position of the button
#         button.setPosition(int(new_x), int(new_y))
        
#         # Increase rotation angle
#         rotation_angle += rotation_speed
        
#         # Delay for smooth animation (adjust as needed)
#         xbmc.sleep(10)

# listitem 
def listitem( label,label2,icon,url):
    # Create a list item
    list_item = xbmcgui.ListItem()

    # Set the label for the list item
    list_item.setLabel(label)

    # Set the label2 for the list item
    list_item.setLabel2(label2)

    # Set the icon for the list item
    list_item.setArt({'icon': icon})
    
    # Set the URL for the list item
    list_item.setPath(url)
    # Return the list item
    return list_item

# fill list
def fill_list():
    # Get window
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

    # Get the list control
    list = window.getControl(10000)

    # Add list items
    list.addItem(listitem('Movies', 'Watch movies online', 'DefaultMovies.png', 'plugin://plugin.video.seren?action=moviesHome'))
    list.addItem(listitem('TV Shows', 'Watch TV shows online', 'DefaultTVShows.png', 'plugin://plugin.video.seren?action=showsHome'))
    list.addItem(listitem('Search', 'Search for movies and TV shows', 'DefaultSearch.png', 'plugin://plugin.video.seren?action=search'))
    list.addItem(listitem('My Movies', 'View your movie collection', 'DefaultMyMovies.png', 'plugin://plugin.video.seren?action=myMovies'))
    list.addItem(listitem('My TV Shows', 'View your TV show collection', 'DefaultMyTVShows.png', 'plugin://plugin.video.seren?action=myShows'))
    list.addItem(listitem('Settings', 'Configure Seren settings', 'DefaultAddonSettings.png', 'plugin://plugin.video.seren?action=settings'))


# if window id is 10000

# fill_list()
