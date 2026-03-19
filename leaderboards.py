import os
import psycopg2
import flet
import time
from dotenv import load_dotenv
# This will be used to find out what the current year is when the event form is submitted.
from datetime import date
from login import login as login_page 
# This will import all of the libraries that will be used in the solution. This is neccessary for creating the GUI via flet, connecting and talking to my database via psycopg2 and using os and dotenv to load and use the credentials(allows me to connect to my database) to my database as well as the keyword for my login system.
# This also imports the login system from login.py that will be called when a user tries to click the event from entry or admin button for the first time.
load_dotenv()

def main(page):
    connection = psycopg2.connect(database = os.getenv("dbName"),
                              host = os.getenv("dbHost"),
                              user = os.getenv("dbUser"),
                              password = os.getenv("dbPassword"),
                              port = os.getenv("dbPort"))
# This establishes a connection to my database using the credentials stored in my dot env. (They have been stored in my dot env so that my real credentials cannot be found in the source code maintaining security)
    cursor = connection.cursor()
    # cursor will be used to execute queries on the database.
    page.scroll = None
    def create_leaderboard(houseANDpoints):
        page.add(
            # Creates a leaderboard on screen displaying the position, the house and the points for that respective house, retrieved from the database which is passed in as a list houseANDpoints
            flet.DataTable(
                columns = [
                    flet.DataColumn(flet.Text("Rank")),
                    flet.DataColumn(flet.Text("House")),
                    flet.DataColumn(flet.Text("Points"))
                ],
                rows = [
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(value = "1")),
                            flet.DataCell(flet.Text(value = houseANDpoints[0])),
                            flet.DataCell(flet.Text(value = houseANDpoints[1]))
                        ]
                    ),
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(value = "2")),
                            flet.DataCell(flet.Text(value = houseANDpoints[2])),
                            flet.DataCell(flet.Text(value = houseANDpoints[3]))
                        ]
                    ),
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(value = "3")),
                            flet.DataCell(flet.Text(value = houseANDpoints[4])),
                            flet.DataCell(flet.Text(value = houseANDpoints[5]))
                        ]
                    ),
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(value = "4")),
                            flet.DataCell(flet.Text(value = houseANDpoints[6])),
                            flet.DataCell(flet.Text(value = houseANDpoints[7]))
                        ]
                    ),
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(value = "5")),
                            flet.DataCell(flet.Text(value = houseANDpoints[8])),
                            flet.DataCell(flet.Text(value = houseANDpoints[9]))
                        ]
                    ),
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(value = "6")),
                            flet.DataCell(flet.Text(value = houseANDpoints[10])),
                            flet.DataCell(flet.Text(value = houseANDpoints[11]))
                        ]
                    )
                ]
            )
        )
    def bubbleSort(array):
        # This is a bubble sort that will sort the list given to it but, when swapping items it swaps 4 items rather than 2 as both the house and the points that house has must be swapped.
        length = len(array)
        # swaps counts how many swaps happen, initialise to 1 so that it can enter the while loop and iterate through the list.
        swaps = 1
        while swaps != 0 :
            swaps = 0
            # resets swaps back to 0 at the start of each pass
            for i in range (1,length-2,2):
                if array[i]<array[i+2]:
                    # compares the points of the current house and the points of the next house via going forward 2 indexes in the list
                    temp = array[i]
                    tempHouse = array[i-1]
                    # Creates 2 temporary place holders so that the house names and house points can be swapped.
                    array[i] = array[i+2]
                    array[i+2] = temp
                    array[i-1] = array[i+1]
                    array[i+1] = tempHouse
                    # Swap is now complete
                    swaps += 1
                    # The number of swaps is incremented by 1
        return array
        # Sorted list is returned
    def timeToSeconds(t):
        # Function to convert the data received in a specific format into just seconds
      t = str(t)
      if ":" in t:
          parts = t.split(":")
          # Seperates the minutes and the seconds
          return int(parts[0]) * 60 + float(parts[1])
          # Multiplies the first part or the minutes part by 60 and adds it to the second part or the seconds part. Returns this value which is now converted the min:secs format to just a time in seconds only.
      else:
          # if the function was accidentally called and the time supplied was just in seconds(so did not need to call this function in the first place) then no proccessing needs to occur, just returns the value that was input.
        return float(t)
    def secondsToDisplay(s):
        # Function to convert raw seconds back into minutes and seconds
        s = float(s)                                                                                                                              
        if s >= 60:
            mins = int(s // 60) # divide by 60 to get the number of minutes
            secs = int(s % 60) # find remainder when dividing by 60 to get the number of seconds
            return f"{mins}:{secs:02d}" # returns min:secs but the secs part is to 2 decimal places
        else:
            return str(round(s, 2))
            # if s is less than 60 hence 0 minutes and n seconds then no proccessing is needed, this simply returns s to 2 dp.
    def select_event(event_name):
        # Function to select the point each house got in a certain event specified by event_name
        cursor.execute("SELECT points FROM bridges_events WHERE event = %s", (event_name,))
        bridgespoint = cursor.fetchone()
        # selects how bridges did in that specific event
        if bridgespoint is None:
            # validation check, if nothing was selected that means that the event does not exist. 
            return None
        else:
            # select each house's respective point score for that event and stores it to a variable
            bridgespoint = bridgespoint[0]
            cursor.execute("SELECT points FROM carew_events WHERE event = %s", (event_name,))
            carewpoint = cursor.fetchall()
            carewpoint = carewpoint[0][0]
            cursor.execute("SELECT points FROM mandeville_events WHERE event = %s", (event_name,))
            mandevillepoint = cursor.fetchall()
            mandevillepoint = mandevillepoint[0][0]
            cursor.execute("SELECT points FROM radcliffe_events WHERE event = %s", (event_name,))
            radcliffepoint = cursor.fetchall()
            radcliffepoint = radcliffepoint[0][0]
            cursor.execute("SELECT points FROM ruskin_events WHERE event = %s", (event_name,))
            ruskinpoint = cursor.fetchall()
            ruskinpoint = ruskinpoint[0][0]
            cursor.execute("SELECT points FROM woodcote_events WHERE event = %s", (event_name,))
            woodcotepoint = cursor.fetchall()
            woodcotepoint = woodcotepoint[0][0]
            # Put all the fetched data paired with their respective house into a list so that is much easier to handle using the bubbleSort function later on. 
            houseANDpoint = ["Bridges", bridgespoint, "Carew", carewpoint, "Mandeville", mandevillepoint, "Radcliffe", radcliffepoint, "Ruskin", ruskinpoint, "Woodcote", woodcotepoint]
            return houseANDpoint
    def dropdownform(e):
        # This function is called to display on screen many many buttons which are labelled as one of the many events. 
        page.controls.clear()
        page.scroll = None
        def getoptions():
            OPTIONS = []
            global house_events
            for i in range(0, len(house_events)):
                OPTIONS.append(house_events[i][0])
            return OPTIONS
            # This retrieves all the events that are going to be displayed on screen as buttons and takes them out of the previous tuple format and appends them to a new list which is then returned
        dropdownoptions = getoptions()
        # This returned list is saved by the identifier dropdownoptions
        for i in range(0,len(dropdownoptions),3):
            page.add(
                flet.Row(
                    controls = [
                        # Adds a row with 3 event buttons onto the screen iteratively.
                        flet.ElevatedButton(text = dropdownoptions[i], on_click = eventClicked),
                        flet.ElevatedButton(text = dropdownoptions[i+1], on_click = eventClicked),
                        flet.ElevatedButton(text = dropdownoptions[i+2], on_click = eventClicked)
                    ],
                    alignment=flet.MainAxisAlignment.CENTER,
                ),
            )
        page.add(
            flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage) # Creates a button that allows user to go back to the previous page
        )
        page.update()
    def CHCSclicked(e):
        # When Cock House Cup Standings button is clicked this is the path it will follow
        # Leads user to a singular leaderboard that displays the cumulative results for the Cock House Cup
        page.controls.clear()
        page.scroll = None
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        select = """ SELECT SUM(points) FROM bridges_events ; """
        cursor.execute(select)
        bridgespoints = cursor.fetchone()
        bridgespoints = bridgespoints[0]
        # This selects and sums all of the points column in the bridges_events table.
        select = """ SELECT SUM(points) FROM carew_events ; """
        cursor.execute(select)
        carewpoints = cursor.fetchone()
        carewpoints = carewpoints[0]
        # This selects and sums all of the points column in the carew_events table.
        select = """ SELECT SUM(points) FROM mandeville_events ; """
        cursor.execute(select)
        mandevillepoints = cursor.fetchone()
        mandevillepoints = mandevillepoints[0]
        # This selects and sums all of the points column in the mandeville_events table.
        select = """ SELECT SUM(points) FROM radcliffe_events ; """
        cursor.execute(select)
        radcliffepoints = cursor.fetchone()
        radcliffepoints = radcliffepoints[0]
        # This selects and sums all of the points column in the radcliffe_events table.
        select = """ SELECT SUM(points) FROM ruskin_events ; """
        cursor.execute(select)
        ruskinpoints = cursor.fetchone()
        ruskinpoints = ruskinpoints[0]
        # This selects and sums all of the points column in the ruskin_events table.
        select = """ SELECT SUM(points) FROM woodcote_events ; """
        cursor.execute(select)
        woodcotepoints = cursor.fetchone()
        woodcotepoints = woodcotepoints[0]
        # This selects and sums all of the points column in the woodcote_events table.
        #Must implement bubble sort using every other index of the array as these will be integers which are the cumulative scores of each house and houses must be ordered based on cumulative. Therefore using step in the for loop for this specific implementation of bubble sort.
        houseANDpoints = ["Bridges", bridgespoints, "Carew", carewpoints, "Mandeville", mandevillepoints, "Radcliffe", radcliffepoints, "Ruskin", ruskinpoints, "Woodcote", woodcotepoints]
        houseANDpoints = bubbleSort(houseANDpoints) # sorts the list so that it can now be passed into the create_leaderboard function as the function will assume that 1st position is the first house in the list 2 position is the second house in the list etc...
        create_leaderboard(houseANDpoints)
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage) # Creates a button that allows user to go back to the previous page
        page.add(
            backButton
        )
        page.update()
    def IERclicked(e):
        #When the individual event results button is clicked this function is called, which by calling other functions will eventually display on screen a list of buttons that represent every single normal Cock House Cup event and when any of the buttons are clicked the respective individual leaderboard for that event will be displayed.
        page.controls.clear()
        page.scroll = None
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        select = """ SELECT * FROM house_event_list """
        cursor.execute(select)
        # This selects all items from the table containing all the house events for the year and returns them in tuple form which is then assigned to the variable house_events
        global house_events
        house_events = cursor.fetchall()
        dropdownform(e)
    def eventClicked(e):
        # This is the function called when any of the individual event results buttons from the dropwdown function are clicked.
        page.controls.clear()
        page.scroll = None
        leaderboard_data = select_event(e.control.text) # selects the result for the event via taking the label/text displayed on the button - which is the event's name
        if leaderboard_data is None:
            #Validation check - presence check. The database will be searched for the result of this event but if the result does not exist, indicated by the "None" value then the event has not taken place yet as no results for it have been entered. The user should be notified of this:
            page.add(
                flet.Text(value = "This event has not taken place yet!"),
                flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = dropdownform) # Creates a button that allows user to go back to the previous page
            )
        else:
            leaderboard_data = bubbleSort(leaderboard_data) # Sort the list in descending order
            create_leaderboard(leaderboard_data) # Create the leaderboard to display the data
            page.add(
                flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = dropdownform) # Creates a button that allows user to go back to the previous page
            )
        page.update()
    def athleticsButtonClicked(e):
        # This is the function called when the View Top 3 of any event button is clicked. This function will select and display the top 3 athletes of every sports day event that has a result.
        page.controls.clear()
        page.scroll = None
        page.update()
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        Rows = []
        for i in range(1,57):
            # Selects all of the time based results 1 by 1 row by row iteratively
            # The table has a column called row order which is used to order the rows in a logical sequence, like all year 7 events should be retrieved and displayed first before year 8 events and so on.
            select = """SELECT "event", "player_bridges", "player_bridges_time", "player_carew", "player_carew_time", "player_mandeville", 
            "player_mandeville_time", "player_radcliffe", "player_radcliffe_time", "player_ruskin", "player_ruskin_time", 
            "player_woodcote", "player_woodcote_time"
                        FROM sports_day_times
                        WHERE row_order = %s; """
            cursor.execute(select, (i,))
            #executes the query and retrieves the result
            temp = cursor.fetchone()
            if None in temp:
                # This is when the event does not have a result, so no extra formatting needs to be done and the fetched data can be added to the list.
                templistready = []
                for i in range(1,7):
                    templistready.append(temp[i])
            else:
                # When there is a result for the event then need to make sure that the time is in only seconds
                templist = []
                for i in range(1, len(temp)-1,2):
                    templist.append(temp[i])
                    templist.append(timeToSeconds(temp[i+1]))# the data fetched is converted into only seconds
                    # adds the athlete name and the athlete's score to templist
                templist = bubbleSort(templist) # sorts the athletes and their respective so that the top 3 can be extracted.
                templistready = []
                for i in range(0, 6):
                    # adds the top 3 which are at the end of the sorted list to another list which now contains only the neccessary data.
                    templistready.append(templist[11-i])
                # adds the top 3 athletes with their respective times to a list called Rows which has the nice and formatted top 3 athlete data
                Rows.append(
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(temp[0])),
                            flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(secondsToDisplay(templistready[0])),
                                flet.Text(templistready[1])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                            flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(secondsToDisplay(templistready[2])),
                                flet.Text(templistready[3])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                            flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(secondsToDisplay(templistready[4])),
                                flet.Text(templistready[5])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        ]
                    )
                )
        for i in range(1,42):
            # Selects all of the time based results 1 by 1 row by row iteratively
            # The table has a column called row order which is used to order the rows in a logical sequence, like all year 7 events should be retrieved and displayed first before year 8 events and so on.
            select = """SELECT "event", "player_bridges", "player_bridges_distance", "player_carew", "player_carew_distance", "player_mandeville", 
            "player_mandeville_distance", "player_radcliffe", "player_radcliffe_distance", "player_ruskin", "player_ruskin_distance", 
            "player_woodcote", "player_woodcote_distance"
                        FROM sports_day_distances
                        WHERE row_order = %s; """
            cursor.execute(select, (i,))
            #executes the query and retrieves the result
            temp = cursor.fetchone()
            if None in temp or "" in temp:
                # when there is no result for the event no formatting or processing needs to be done hence added straightaway to templistready.
                templistready = []
                for i in range(1,7):
                    templistready.append(temp[i])
            else:
                # when there is a result:
                templist = []
                for i in range(1, len(temp)-1,2):
                    templist.append(temp[i])
                    templist.append(float(temp[i+1]))
                    # adds the athlete name and the athlete's score to templist
                templist = bubbleSort(templist) #sorts the list so that the top 3 are now the first few indexes
                templistready = []
                for i in range(0, 6):
                    templistready.append(templist[i])
                # adds the top 3 athletes with their respective times to a list called Rows which has the nice and formatted top 3 athlete data
                Rows.append(
                    flet.DataRow(
                        cells = [
                            flet.DataCell(flet.Text(temp[0])),
                            flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(templistready[0]),
                                flet.Text(templistready[1])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                            flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(templistready[2]),
                                flet.Text(templistready[3])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                            flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(templistready[4]),
                                flet.Text(templistready[5])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        ]
                    )
                )
        # Creates a table that will be used to display the top 3 atheletes of every event
        athleticstable = flet.DataTable(
            columns = [
                # defines all the columns that will be in the table
                flet.DataColumn(flet.Text("Event")),
                flet.DataColumn(flet.Text("1st")),
                flet.DataColumn(flet.Text("2nd")),
                flet.DataColumn(flet.Text("3rd"))
            ],
            rows = Rows # The list that contains all the relevant data with the nice formatting is now assigned to the tables rows.
        )
        page.add(flet.Text(value = "Top 3 in each event!", color = "red", size = 100))
        page.add(flet.Text(value = "For events that have not occured yet the top 3 for that event will not be displayed!", color = "Blue", size = 20))
        page.add(
            flet.Column(
                controls = [athleticstable],
                scroll = "auto", # allows the table to be scrollable as all the results of all 100ish events probably can't fit on the screen
                expand = True
            )
        ) 
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = SDRclicked) # Creates a back button that when clicked leads the user back to the previous page.
        page.add(backButton)
    def recordtable(e):
        # This is the function called when the WCGS Athletics Records button is clicked, which will be used to display a table containing all of the WCGS records for the sports day events.
        page.controls.clear()
        page.scroll = None
        page.update()
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        selectyear7 = """SELECT "year7player", "year7time", "year7date"
                        FROM "school_records"
                        ORDER BY "row_order" ASC """
        cursor.execute(selectyear7)
        # selects all of the year 7 athletics records and stores them
        datayear7 = cursor.fetchall()

        selectyear8 = """SELECT "year8player", "year8time", "year8date"
                        FROM "school_records"
                        ORDER BY "row_order" ASC  """
        cursor.execute(selectyear8)
        # selects all of the year 8 athletics records and stores them
        datayear8 = cursor.fetchall()

        selectyear9 = """SELECT "year9player", "year9time", "year9date"
                        FROM "school_records"
                        ORDER BY "row_order" ASC  """
        cursor.execute(selectyear9)
        # selects all of the year 9 athletics records and stores them
        datayear9 = cursor.fetchall()

        selectyear10 = """SELECT "year10player", "year10time", "year10date"
                        FROM "school_records"
                        ORDER BY "row_order" ASC  """
        cursor.execute(selectyear10)
        # selects all of the year 10 athletics records and stores them
        datayear10 = cursor.fetchall()

        selectsenior = """SELECT "seniorplayer", "seniortime", "seniordate"
                        FROM "school_records"
                        ORDER BY "row_order" ASC  """
        cursor.execute(selectsenior)
        # selects all of the senior athletics records and stores them
        datasenior = cursor.fetchall()

        selectgirls = """SELECT "girlsplayer", "girlstime", "girlsdate"
                        FROM "school_records"
                        ORDER BY "row_order" ASC  """
        cursor.execute(selectgirls)
        # selects all of the girls athletics records and stores them
        datagirls = cursor.fetchall()


        recordstable = flet.DataTable(
            columns = [
                # defines all the columns that will be in the table
                flet.DataColumn(flet.Text("Event")),
                flet.DataColumn(flet.Text("Year 7")),
                flet.DataColumn(flet.Text("Year 8")),
                flet.DataColumn(flet.Text("Year 9")),
                flet.DataColumn(flet.Text("Year 10")),
                flet.DataColumn(flet.Text("Senior")),
                flet.DataColumn(flet.Text("Girls"))
            ],
            rows = [
                # Creates a row containing all the records for each age category for the 100m event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("100m")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[0][0]),
                                flet.Text(value = datayear7[0][1]+"s"),
                                flet.Text(datayear7[0][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[0][0]),
                                flet.Text(value = datayear8[0][1]+"s"),
                                flet.Text(datayear8[0][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[0][0]),
                                flet.Text(value = datayear9[0][1]+"s"),
                                flet.Text(datayear9[0][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[0][0]),
                                flet.Text(value = datayear10[0][1]+"s"),
                                flet.Text(datayear10[0][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[0][0]),
                                flet.Text(value = datasenior[0][1]+"s"),
                                flet.Text(datasenior[0][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[0][0]),
                                flet.Text(value = datagirls[0][1]+"s"),
                                flet.Text(datagirls[0][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the 200m event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("200m")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[1][0]),
                                flet.Text(value = datayear7[1][1]+"s"),
                                flet.Text(datayear7[1][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[1][0]),
                                flet.Text(value = datayear8[1][1]+"s"),
                                flet.Text(datayear8[1][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[1][0]),
                                flet.Text(value = datayear9[1][1]+"s"),
                                flet.Text(datayear9[1][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[1][0]),
                                flet.Text(value = datayear10[1][1]+"s"),
                                flet.Text(datayear10[1][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[1][0]),
                                flet.Text(value = datasenior[1][1]+"s"),
                                flet.Text(datasenior[1][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[1][0]),
                                flet.Text(value = datagirls[1][1]+"s"),
                                flet.Text(datagirls[1][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the 300m event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("300m")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[2][0]),
                                flet.Text(value = datayear7[2][1]+"s"),
                                flet.Text(datayear7[2][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[2][0]),
                                flet.Text(value = datayear8[2][1]+"s"),
                                flet.Text(datayear8[2][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[2][0]),
                                flet.Text(value = datayear9[2][1]+"s"),
                                flet.Text(datayear9[2][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[2][0]),
                                flet.Text(value = datayear10[2][1]+"s"),
                                flet.Text(datayear10[2][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[2][0]),
                                flet.Text(value = "N/A"),
                                flet.Text(datasenior[2][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[2][0]),
                                flet.Text(value = datagirls[2][1]+"s"),
                                flet.Text(datagirls[2][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the 400m event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("400m")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[3][0]),
                                flet.Text(value = datayear7[3][1]+"s"),
                                flet.Text(datayear7[3][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[3][0]),
                                flet.Text(value = datayear8[3][1]+"s"),
                                flet.Text(datayear8[3][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[3][0]),
                                flet.Text(value = datayear9[3][1]+"s"),
                                flet.Text(datayear9[3][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[3][0]),
                                flet.Text(value = datayear10[3][1]+"s"),
                                flet.Text(datayear10[3][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[3][0]),
                                flet.Text(value = datasenior[3][1]+"s"),
                                flet.Text(datasenior[3][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[3][0]),
                                flet.Text(value = "N/A"),
                                flet.Text(datagirls[3][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the 800m event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("800m")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[4][0]),
                                flet.Text(value = datayear7[4][1][0]+"mins "+datayear7[4][1][2]+datayear7[4][1][3]+"secs"),
                                flet.Text(datayear7[4][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[4][0]),
                                flet.Text(value = datayear8[4][1][0]+"mins "+datayear8[4][1][2]+datayear8[4][1][3]+"secs"),
                                flet.Text(datayear8[4][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[4][0]),
                                flet.Text(value = datayear9[4][1][0]+"mins "+datayear9[4][1][2]+datayear9[4][1][3]+"secs"),
                                flet.Text(datayear9[4][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[4][0]),
                                flet.Text(value = datayear10[4][1][0]+"mins "+datayear10[4][1][2]+datayear10[4][1][3]+"secs"),
                                flet.Text(datayear10[4][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[4][0]),
                                flet.Text(value = datasenior[4][1][0]+"mins "+datasenior[4][1][2]+datasenior[4][1][3]+"secs"),
                                flet.Text(datasenior[4][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[4][0]),
                                flet.Text(value = datagirls[4][1][0]+"mins "+datagirls[4][1][2]+datagirls[4][1][3]+"secs"),
                                flet.Text(datagirls[4][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the 1500m event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("1500m")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[5][0]),
                                flet.Text(value = datayear7[5][1][0]+"mins "+datayear7[5][1][2]+datayear7[5][1][3]+"secs"),
                                flet.Text(datayear7[5][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[5][0]),
                                flet.Text(value = datayear8[5][1][0]+"mins "+datayear8[5][1][2]+datayear8[5][1][3]+"secs"),
                                flet.Text(datayear8[5][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[5][0]),
                                flet.Text(value = datayear9[5][1][0]+"mins "+datayear9[5][1][2]+datayear9[5][1][3]+"secs"),
                                flet.Text(datayear9[5][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[5][0]),
                                flet.Text(value = datayear10[5][1][0]+"mins "+datayear10[5][1][2]+datayear10[5][1][3]+"secs"),
                                flet.Text(datayear10[5][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[5][0]),
                                flet.Text(value = datasenior[5][1][0]+"mins "+datasenior[5][1][2]+datasenior[5][1][3]+"secs"),
                                flet.Text(datasenior[5][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[5][0]),
                                flet.Text(value = "N/A"),
                                flet.Text(datagirls[5][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the 200m Relay event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("200m Relay")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[6][0]),
                                flet.Text(value = datayear7[6][1][0]+"mins "+datayear7[6][1][2]+datayear7[6][1][3]+"secs"),
                                flet.Text(datayear7[6][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[6][0]),
                                flet.Text(value = datayear8[6][1][0]+"mins "+datayear8[6][1][2]+datayear8[6][1][3]+"secs"),
                                flet.Text(datayear8[6][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[6][0]),
                                flet.Text(value = datayear9[6][1][0]+"mins "+datayear9[6][1][2]+datayear9[6][1][3]+"secs"),
                                flet.Text(datayear9[6][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[6][0]),
                                flet.Text(value = datayear10[6][1][0]+"mins "+datayear10[6][1][2]+datayear10[6][1][3]+"secs"),
                                flet.Text(datayear10[6][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[6][0]),
                                flet.Text(value = datasenior[6][1][0]+"mins "+datasenior[6][1][2]+datasenior[6][1][3]+"secs"),
                                flet.Text(datasenior[6][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[6][0]),
                                flet.Text(value = datagirls[6][1][0]+"mins "+datagirls[6][1][2]+datagirls[6][1][3]+"secs"),
                                flet.Text(datagirls[6][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the Triple Jump event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("Triple Jump")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[7][0]),
                                flet.Text(value = datayear7[7][1]+"m"),
                                flet.Text(datayear7[7][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[7][0]),
                                flet.Text(value = datayear8[7][1]+"m"),
                                flet.Text(datayear8[7][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[7][0]),
                                flet.Text(value = datayear9[7][1]+"m"),
                                flet.Text(datayear9[7][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[7][0]),
                                flet.Text(value = datayear10[7][1]+"m"),
                                flet.Text(datayear10[7][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[7][0]),
                                flet.Text(value = datasenior[7][1]+"m"),
                                flet.Text(datasenior[7][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[7][0]),
                                flet.Text(value = "N/A"),
                                flet.Text(datagirls[7][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the Long Jump event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("Long Jump")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[8][0]),
                                flet.Text(value = datayear7[8][1]+"m"),
                                flet.Text(datayear7[8][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[8][0]),
                                flet.Text(value = datayear8[8][1]+"m"),
                                flet.Text(datayear8[8][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[8][0]),
                                flet.Text(value = datayear9[8][1]+"m"),
                                flet.Text(datayear9[8][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[8][0]),
                                flet.Text(value = datayear10[8][1]+"m"),
                                flet.Text(datayear10[8][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[8][0]),
                                flet.Text(value = datasenior[8][1]+"m"),
                                flet.Text(datasenior[8][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[8][0]),
                                flet.Text(value = datagirls[8][1]+"m"),
                                flet.Text(datagirls[8][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the High Jump event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("High Jump")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[9][0]),
                                flet.Text(value = datayear7[9][1]+"m"),
                                flet.Text(datayear7[9][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[9][0]),
                                flet.Text(value = datayear8[9][1]+"m"),
                                flet.Text(datayear8[9][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[9][0]),
                                flet.Text(value = datayear9[9][1]+"m"),
                                flet.Text(datayear9[9][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[9][0]),
                                flet.Text(value = datayear10[9][1]+"m"),
                                flet.Text(datayear10[9][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[9][0]),
                                flet.Text(value = datasenior[9][1]+"m"),
                                flet.Text(datasenior[9][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[9][0]),
                                flet.Text(value = datagirls[9][1]+"m"),
                                flet.Text(datagirls[9][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the Discus event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("Discus")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[10][0]),
                                flet.Text(value = datayear7[10][1]+"m"),
                                flet.Text(datayear7[10][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[10][0]),
                                flet.Text(value = datayear8[10][1]+"m"),
                                flet.Text(datayear8[10][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[10][0]),
                                flet.Text(value = datayear9[10][1]+"m"),
                                flet.Text(datayear9[10][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[10][0]),
                                flet.Text(value = datayear10[10][1]+"m"),
                                flet.Text(datayear10[10][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[10][0]),
                                flet.Text(value = datasenior[10][1]+"m"),
                                flet.Text(datasenior[10][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[10][0]),
                                flet.Text(value = datagirls[10][1]+"m"),
                                flet.Text(datagirls[10][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the Shotput event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("Shotput")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[11][0]),
                                flet.Text(value = datayear7[11][1]+"m"),
                                flet.Text(datayear7[11][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[11][0]),
                                flet.Text(value = datayear8[11][1]+"m"),
                                flet.Text(datayear8[11][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[11][0]),
                                flet.Text(value = datayear9[11][1]+"m"),
                                flet.Text(datayear9[11][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[11][0]),
                                flet.Text(value = datayear10[11][1]+"m"),
                                flet.Text(datayear10[11][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[11][0]),
                                flet.Text(value = datasenior[11][1]+"m"),
                                flet.Text(datasenior[11][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[11][0]),
                                flet.Text(value = datagirls[11][1]+"m"),
                                flet.Text(datagirls[11][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
                # Creates a row containing all the records for each age category for the Javelin event
                flet.DataRow(
                    cells = [
                        flet.DataCell(flet.Text("Javelin")),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear7[12][0]),
                                flet.Text(value = datayear7[12][1]+"m"),
                                flet.Text(datayear7[12][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear8[12][0]),
                                flet.Text(value = datayear8[12][1]+"m"),
                                flet.Text(datayear8[12][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear9[12][0]),
                                flet.Text(value = datayear9[12][1]+"m"),
                                flet.Text(datayear9[12][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datayear10[12][0]),
                                flet.Text(value = datayear10[12][1]+"m"),
                                flet.Text(datayear10[12][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER   
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datasenior[12][0]),
                                flet.Text(value = datasenior[12][1]+"m"),
                                flet.Text(datasenior[12][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                        flet.DataCell(flet.Column(
                            controls = [
                                flet.Text(datagirls[12][0]),
                                flet.Text(value = datagirls[12][1]+"m"),
                                flet.Text(datagirls[12][2])
                            ],
                            spacing = 2,
                            alignment=flet.MainAxisAlignment.CENTER,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER
                        )),
                    ]
                ),
            ],
            data_row_max_height = 70
        )
        page.add(flet.Text(value = "WCGS Athletics Records", size = 75, color = "Red"))
        page.add(
            flet.Column(
                controls = [recordstable],
                scroll = "auto", # allows the table to be scrollable as the whole table will not be able to fit on the page.
                expand = True
            )
        ) 
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = SDRclicked) # creates a back button that when clicked will lead the user back to the previous page.
        page.add(backButton)
    def SDRclicked(e):
        # This function is called when the sports day results button is clicked.
        # This function displays another set of buttons that allow the user to view different aspects of sports day like the overall standings for example and much more!
        page.controls.clear()
        page.scroll = None
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        # Creates 4 different buttons each for different features to do with sportsday
        overall_leaderboardSD = flet.ElevatedButton(text = "Overall sports day leaderboard", width = 400, height = 100, on_click = OSDLButtonClicked)
        individual_LeaderboardSD = flet.ElevatedButton(text = "Individual sports day leaderboards", width = 400, height = 100, on_click = ISDLclicked)
        athleticsButton = flet.ElevatedButton(text = "View Top 3 of all Sports Day Events", width = 300, height = 100, on_click = athleticsButtonClicked)
        recordsButton = flet.ElevatedButton(text = "WCGS Athletics Records", width = 300, height = 100, on_click = recordtable)
        # Adds them to the page in a nice visually appealing format.
        page.add(
            flet.Column(
                [
                    flet.Row(
                        controls=[
                            overall_leaderboardSD,
                            individual_LeaderboardSD,
                            athleticsButton,
                            recordsButton
                        ],
                        alignment="center",   # aligns button to centre horizontally
                        spacing=15
                    ),
                    flet.Row(
                        controls = [
                            flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage) # Creates a button that allows user to go back to the previous page
                        ],
                        alignment = "center"
                    )
                ],
                alignment="center",           # aligns button to centre vertically
                horizontal_alignment="center",
                expand=True                   # Column expands across height
            )
        )
        page.update()
    def ISDLclicked(e):
        # This function is called when the individual sports day leaderboard button is clicked
        # Using this function the user will be able to search for and view the individual standings of the event they search for via this function.
        page.scroll = None
        def sportsDaySearch(e):
            # This function is used to search and select the individual event results of the sports day event that the user searches for.
            # retrieve the user's input for what event they want to see the result of:
            userinput = sportsDaySearchBar.value
            selectedEvent = ""
            # Search through the list of sports day events (sportsDayEventsCleaned) and find/select the event that the user has searched for
            # 
            for i in range(0,len(sportsDayEventsCleaned)):
                iterateEvent = sportsDayEventsCleaned[i]
                if userinput.lower() in iterateEvent.lower():
                    # Compared in this way so that the user does not have to type the full event name - this could be quite tedious, instead the user needs to type in enough of the event to uniquely identify it from another event.
                    selectedEvent = sportsDayEventsCleaned[i] # makes sure that selectedEvent has the same value/name of the event as the database does that way the selection of that event's result is much smoother.
            # Create and add a message letting the user know what event they have selected as a result of the input they have entered in the searchbar.
            selectedEventMessage = flet.Text(value = ("You have selected event: " + selectedEvent), visible = False, color = "Green")# set to false for now since, I first need to check that an event has been selected - selectedEvent therefore would have a value.
            page.add(selectedEventMessage)
            if selectedEvent == "":
                # if selectedEvent does not have a value, then nothing was written to the variable hence no matches for the user's input were found meaning that the user's input was an invalid input and hence toggling the error message's visibility to true will let the user know to try again.                errorMessage.visible = True
                selectedEventMessage.visible = False
                page.update()# refreshes the page so that the message can be seen
                return # stops the function here so that the next instructions of selecting from the database do not occur as I would be executing select * from table where event = "".
                # the where clause will never find a match and hence return none and when later these fetched results are used, doing processing with the none value will cause errors.
                # this in some sense is another form of a validation check - presence check, making sure that selectedEvent has a value before executing SQL select.
            else:
                # if selectedEvent does have a value that means a match for the user's input was found and so the results for that event will now be retrieved from the database.
                selectedEventMessage.visible = True # Lets the user know which event what event they have selected by toggling the visibility of the message to true then updating/refreshing the page
                errorMessage.visible = False
                page.update()
            page.update()
            selectPoints = """SELECT "bridgespoints", "carewpoints", "mandevillepoints", "radcliffepoints", "ruskinpoints", "woodcotepoints"
                                FROM "sports_day_events"
                                WHERE "event" = %s;  """
            cursor.execute(selectPoints, (selectedEvent,))
            # selects all the house's respective points for the event 
            points = cursor.fetchall()
            houseANDpoints = ["Bridges", 0, "Carew", 0, "Mandeville", 0, "Radcliffe", 0, "Ruskin", 0, "Woodcote", 0]
            for i in range(1, 7):
                # Iteratively adds all the respective points for each house to the list houseANDpoints
                houseANDpoints[(2*i)-1] = points[0][i-1]
            bubbleSort(houseANDpoints) # sorts the list
            page.controls.clear()
            page.update()
            page.add(flet.Text(selectedEvent, color = "Red", size = 50))# displays at the top of the page the event name
            create_leaderboard(houseANDpoints) # creates a leaderboard displaying the fetched results
            back = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = ISDLclicked) # creates a button that leads the user back to the previous page
            page.add(back)
        page.controls.clear()
        page.update()
        #select all of the possible events that sports day could have via:
        select_sports_day_events = """SELECT "event" FROM "sports_day_events";  """
        cursor.execute(select_sports_day_events)
        global sportsDayEvents
        sportsDayEvents = cursor.fetchall()
        # fetches and stores these results to a list, but currently in tuple format, need to convert to a plain list format via:
        sportsDayEventsCleaned = []
        for i in range(0, len(sportsDayEvents)):
            # extract the event name only
            sportsDayEventsCleaned.append(sportsDayEvents[i][0])
        sportsDaySearchBar = flet.TextField(label = "Enter event you would like to see the leaderboard for...") # creates a searchbar for the user to input what event they would like to see the result of.
        page.add(sportsDaySearchBar)
        SUBMIT = flet.ElevatedButton(text = "Search", on_click = sportsDaySearch, width = 150, height = 60) # creates a submit button for when the user is done entering the input for what event they want to see the result of.
        page.add(SUBMIT)
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = SDRclicked) # creates a back button that leads the user back to the previous page
        page.add(backButton)
        selectedEvent = ""
        selectedEventMessage = flet.Text(value = ("You have selected event: " + selectedEvent), visible = False, color = "green") # creates a message that lets the user know what event they have selected
        errorMessage = flet.Text("Please enter an actual event!", visible = False, color = "Red")# creates an error message that prompts the user to try again when no match is found for their input
        # visibility is set to false for both messages, since only one message should appear on the screen at a time which would be decided by whether or not the selectedEvent variable is given a value. If yes then visibility of selectedEventMessage will be set to true and vice versa.
        page.add(selectedEventMessage)
        page.add(errorMessage)
    def OSDLButtonClicked(e):
        # This function is called when the Overall Sports day Leaderboard button is clicked
        page.controls.clear()
        page.scroll = None
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.update()
        # select the total amount of points bridges has acquired over sports day and store them for later
        selectbridgespoints = """SELECT sum(bridgespoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectbridgespoints)
        bridgespoints = cursor.fetchone()
        bridgespoints = bridgespoints[0]
        # select the total amount of points carew has acquired over sports day and store them for later
        selectcarewpoints = """SELECT sum(carewpoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectcarewpoints)
        carewpoints = cursor.fetchone()
        carewpoints = carewpoints[0]
        # select the total amount of points mandeville has acquired over sports day and store them for later
        selectmandevillepoints = """SELECT sum(mandevillepoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectmandevillepoints)
        mandevillepoints = cursor.fetchone()
        mandevillepoints = mandevillepoints[0]
        # select the total amount of points radcliffe has acquired over sports day and store them for later
        selectradcliffepoints = """SELECT sum(radcliffepoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectradcliffepoints)
        radcliffepoints = cursor.fetchone()
        radcliffepoints = radcliffepoints[0]
        # select the total amount of points ruskin has acquired over sports day and store them for later
        selectruskinpoints = """SELECT sum(ruskinpoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectruskinpoints)
        ruskinpoints = cursor.fetchone()
        ruskinpoints = ruskinpoints[0]
        # select the total amount of points woodcote has acquired over sports day and store them for later
        selectwoodcotepoints = """SELECT sum(woodcotepoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectwoodcotepoints)
        woodcotepoints = cursor.fetchone()
        woodcotepoints = woodcotepoints[0]
        # create a list with these retrieved results
        houseANDpoints = ["Bridges", bridgespoints, "Carew", carewpoints, "Mandeville", mandevillepoints, "Radcliffe", radcliffepoints, "Ruskin", ruskinpoints, "Woodcote", woodcotepoints]
        houseANDpoints = bubbleSort(houseANDpoints) # sort the list
        create_leaderboard(houseANDpoints) # create a leaderboard for the results contained within this list
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = SDRclicked) # create a button that leads the user to the previous page.
        page.add(backButton)
    def EEBclicked(e):
        # This function is called when the event entry button is clicked.
        # This function handles the event forms through which the results are collected.
        page.scroll = None
        def EEBClickedPostLogin():
            # This page should only be accessible after a successful login.
            page.scroll = None
            page.session.set("logged_in", True)
            page.controls.clear()
            page.vertical_alignment = flet.MainAxisAlignment.CENTER
            page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
            page.update()
            backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage) # Creates a button that allows user to go back to the previous page
            sportsDayButton = flet.ElevatedButton(text = "Sports Day", width = 400, height = 100, on_click = sportsDayButtonClicked) # Creates a button that when clicked leads the user to the sports day event entry form
            houseEventsButton = flet.ElevatedButton(text = "House Events", width = 400, height = 100, on_click = houseEventsButtonClicked) # Creates a button that when clicked leads the user to the normal Cock House Cup event entry form
            page.add(
                sportsDayButton,
                houseEventsButton
            )
            page.add(
                backButton
                )
        if page.session.get("logged_in") == True:
            # if the user has logged in successfully then call the function above so that the user can select what type of event they want to enter the result of.
            EEBClickedPostLogin()
        else:
            # if the user is not logged in yet then they will need to login first
            page.controls.clear()
            page.update()
            login_page(page, on_success= EEBClickedPostLogin, on_back= leaderboardpage) # calls the login function from login.py which will be used to authenticate the user. 
            # on_success defines that when the login is successful then EEBClickedPostLogin function should be called
            # on_back defines that when the user clicks the back button the leaderboardpage function should be called which just leads the user back to the previous page.
    def sportsDayButtonClicked(e):
        # This is the function for the sports day event form
        page.controls.clear()
        page.session.set("event", "")
        # Initialises the event variable that will store the event that the user selects. Each instance of the page gets its own personal event via session - this is so that if multiple users interact with this functionality then the different inputs of different users will overwrite each other which is not ideal. Having the personal version of event prevents this.
        page.scroll = flet.ScrollMode.AUTO
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.theme_mode= flet.ThemeMode.DARK
        page.add(flet.Text(value = "Enter Sports Day Event results", color = "Red", size = 50))
        # fetch all of the sports day events and store them to the list options which will then contain all the events but in tuple format
        select = """ SELECT event FROM sports_day_events; """
        cursor.execute(select)
        fetch = cursor.fetchall()
        options = fetch
        optionsCleaned = []
        for i in range(0, len(options)):
            # extracts the event name from the tuple format and adds it to a new "cleaned" list
            optionsCleaned.append(options[i][0])
        timeEvents = ["100m", "200m", "300m", "400m", "800m", "1500m", "Relay"] # identifiers/keywords that identify the event to be time based
        distanceEvents = ["Javelin", "Discus", "Shotput", "Long Jump", "Triple Jump", "High Jump"]# identifiers/keywords that identify the event to be distance based
        def searchBar(optionsCleaned):
            # Function that creates a search bar for the user to input the event they want to enter the result for.
            def dropdown(e):
                bpos = bridgesdd.value
                cpos = carewdd.value
                mpos = mandevilledd.value
                rapos = radcliffedd.value
                rupos = ruskindd.value
                wpos = woodcotedd.value
                rank = [bpos, cpos, mpos, rapos, rupos, wpos]
                # fetches the data input by the user in the dropdown forms which will be the position of each house in the event and adds them to the list ranked
                if None in rank:
                    # presence check - if when the values in the dropdown form are retrieved and added to rank, the value none is contained within ranked the user has not entered the positions of the house's completely hence will be prompted to do so by toggling the visibilty of the presencemessage1 to true.
                    presenceMessage1.visible = True
                    page.update()
                    return # prevents the next sequence of instructions from being executed as some of the neccessary data is missing and needs to be input first. 
                if searchbar.value == "":
                    # presence check - if when the value in the searchbar is retrieved the value is "" the user has not searched for an event to enter the result for hence will be prompted to do so by toggling the visibilty of the presencemessage0 to true.
                    presenceMessage0.visible = True
                    page.update()
                    return
                if "Tug of War" not in (page.session.get("event") or ""):
                    # if the event is not a tug of war event then a list with all the inputted results from the user including player names and times is created
                    list = [bridgesplayer.value, bridgesplayertime.value, carewplayer.value, carewplayertime.value,
                            mandevilleplayer.value, mandevilleplayertime.value, radcliffeplayer.value, radcliffeplayertime.value,
                            ruskinplayer.value, ruskinplayertime.value, woodcoteplayer.value, woodcoteplayertime.value]
                    if None in list or "" in list:
                        # another presence check to make sure that all the data needed is input by the user, if not the presencemessage2's visibility is toggled to true to prompt the user to enter all the relevant details.
                        presenceMessage2.visible = True
                        page.update()
                        return # prevents the next sequence of instructions from being executed as some of the neccessary data is missing and needs to be input first. 
                colonrequired = ["800m", "1500m", "Relay"] # these are the keywords/identifiers for events that need the time to be entered in a specific format.
                for item in colonrequired:
                    if item in (page.session.get("event") or ""):
                        # if the event contains one of the keywords from the colon required list then I will need to do a format check to make sure that the time has been entered in the correct format
                        checks = [bridgesplayertime.value, carewplayertime.value, mandevilleplayertime.value, radcliffeplayertime.value, ruskinplayertime.value, woodcoteplayertime.value]
                        for item in checks:
                            if ":" not in item:
                                # checking that there is a colon to seperate the time into min:secs
                                colonmessage.visible = True # toggles visibility of the error message so that the user is prompted to enter the data in the correct format
                                page.update()
                                return # prevents the next sequence of instructions from being executed as some of the neccessary data is not in the correct format and needs to be input correctly first. 
                point = []
                for i in range(0, len(rank)):
                    # by taking the position of the houses in the event, the respective amount of points are allocated.
                    point.append(7 - int(rank[i]))
                if "Relay" in (page.session.get("event") or ""):
                    # if the event is the relay race then I need to account for the event being weighted so there is a score multiplier of 2 which applied iteratively by doubling the value at each index of the list point
                    for i in range(0, len(point)):
                        point[i] = point[i]*2
                timebool = False # variable to hold whether the event is time based or not
                distancebool = False # variable to hold whether the event is distance based or not
                for i in range(0,len(timeEvents)):
                    if timeEvents[i] in (page.session.get("event") or ""):
                        # Iterates through the list of timebased event identifiers and if the keywords are in the event name then the variable holding whether or not the event is timebased is toggled to true:
                        timebool = True
                for i in range(0, len(distanceEvents)):
                    if distanceEvents[i] in (page.session.get("event") or ""):
                        distancebool = True
                        # Iterates through the list of distancebased event identifiers and if the keywords are in the event name then the variable holding whether or not the event is distancebased is toggled to true:
                # updates/inserts the points for bridges house into the database
                insertBridges = """UPDATE "sports_day_events"
                                SET "bridgespoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertBridges,(point[0], (page.session.get("event") or "")))
                connection.commit()
                # updates/inserts the points for carew house into the database
                insertCarew = """UPDATE "sports_day_events"
                                SET "carewpoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertCarew,(point[1],(page.session.get("event") or "")))
                connection.commit()
                # updates/inserts the points for mandeville house into the database
                insertMandeville = """UPDATE "sports_day_events"
                                SET "mandevillepoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertMandeville,(point[2],(page.session.get("event") or "")))
                connection.commit()
                # updates/inserts the points for radcliffe house into the database
                insertRadcliffe = """UPDATE "sports_day_events"
                                SET "radcliffepoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertRadcliffe,(point[3],(page.session.get("event") or "")))
                connection.commit()
                # updates/inserts the points for ruskin house into the database
                insertRuskin = """UPDATE "sports_day_events"
                                SET "ruskinpoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertRuskin,(point[4],(page.session.get("event") or "")))
                connection.commit()
                # updates/inserts the points for woodcite house into the database
                insertWoodcote = """UPDATE "sports_day_events"
                                SET "woodcotepoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertWoodcote,(point[5],(page.session.get("event") or "")))
                connection.commit()
                # These series of queries update the table in the database that contains only the event name and the number of points each house was awarded in the event. 
                # I now need to insert the player names and times into either the sports_day_times or sports_day_distances tables based on whether the event is time or distance based.
                if timebool == True:
                    # if it is a time based event
                    updateplayerbridges = """UPDATE "sports_day_times"
                                SET "player_bridges" = %s,
                                    "player_bridges_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerbridges, (bridgesplayer.value, bridgesplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the bridges player's time and name
                    updateplayercarew = """UPDATE "sports_day_times"
                                SET "player_carew" = %s,
                                    "player_carew_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayercarew, (carewplayer.value, carewplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the carew player's time and name
                    updateplayermandeville = """UPDATE "sports_day_times"
                                SET "player_mandeville" = %s,
                                    "player_mandeville_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayermandeville, (mandevilleplayer.value, mandevilleplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the mandeville player's time and name
                    updateplayerradcliffe = """UPDATE "sports_day_times"
                                SET "player_radcliffe" = %s,
                                    "player_radcliffe_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerradcliffe, (radcliffeplayer.value, radcliffeplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the radcliffe player's time and name
                    updateplayerruskin = """UPDATE "sports_day_times"
                                SET "player_ruskin" = %s,
                                    "player_ruskin_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerruskin, (ruskinplayer.value, ruskinplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the woodcote player's time and name
                    updateplayerwoodcote = """UPDATE "sports_day_times"
                                SET "player_woodcote" = %s,
                                    "player_woodcote_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerwoodcote, (woodcoteplayer.value, woodcoteplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                if distancebool == True:
                    # if it is a distance based event
                    updateplayerbridges = """UPDATE "sports_day_distances"
                                SET "player_bridges" = %s,
                                    "player_bridges_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerbridges, (bridgesplayer.value, bridgesplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the bridges player's distance and name
                    updateplayercarew = """UPDATE "sports_day_distances"
                                SET "player_carew" = %s,
                                    "player_carew_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayercarew, (carewplayer.value, carewplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the carew player's distance and name
                    updateplayermandeville = """UPDATE "sports_day_distances"
                                SET "player_mandeville" = %s,
                                    "player_mandeville_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayermandeville, (mandevilleplayer.value, mandevilleplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the mandeville player's distance and name
                    updateplayerradcliffe = """UPDATE "sports_day_distances"
                                SET "player_radcliffe" = %s,
                                    "player_radcliffe_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerradcliffe, (radcliffeplayer.value, radcliffeplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the radcliffe player's distance and name
                    updateplayerruskin = """UPDATE "sports_day_distances"
                                SET "player_ruskin" = %s,
                                    "player_ruskin_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerruskin, (ruskinplayer.value, ruskinplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the ruskin player's distance and name
                    updateplayerwoodcote = """UPDATE "sports_day_distances"
                                SET "player_woodcote" = %s,
                                    "player_woodcote_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerwoodcote, (woodcoteplayer.value, woodcoteplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the woodcote player's distance and name
                def split(event):
                    # function to split the event into the event type and age category
                    events = ["100m", "200m", "300m","400m", "800m", "1500m", "Discus", "Shotput", "Long Jump", "High Jump", "Javelin", "Triple Jump", "200m Relay", "Relay"] # list of event types
                    ageCat = ["Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Senior", "Girls"] # list of age categories
                    eventName = "" # variable to hold the corresponding event
                    ageCategory = "" # variable to hold the corresponding age category
                    for i in range(0, len(events)):
                        if events[i] in event:
                            # if the event type is in event then it is stored to eventName
                            eventName = events[i]
                    for i in range(0,len(ageCat)):
                        if ageCat[i] in event:
                            # if the age category is in the event then it is stored to ageCategory
                            ageCategory = ageCat[i]
                    return eventName, ageCategory
                if "Tug of War" not in (page.session.get("event") or ""):
                    # if the event is not tug of war
                    splittedEvent = split((page.session.get("event") or ""))# split the event into its respective event type and age category
                    event_name = splittedEvent[0] #extract the event type
                    age_category = splittedEvent[1] # extract the event age category
                    times = [bridgesplayer.value, timeToSeconds(bridgesplayertime.value), carewplayer.value, timeToSeconds(carewplayertime.value), mandevilleplayer.value, timeToSeconds(mandevilleplayertime.value), radcliffeplayer.value, timeToSeconds(radcliffeplayertime.value), ruskinplayer.value, timeToSeconds(ruskinplayertime.value), woodcoteplayer.value, timeToSeconds(woodcoteplayertime.value)]
                    # creates a list with all the player names and their respective times
                    sortedtimes = bubbleSort(times) # sorts this list
                    if timebool == True:
                        # taking 1st place - last 2 indexes so that I can check whether a record has been broken
                        recordcheck = sortedtimes[len(sortedtimes)-1]
                        recordcheckplayer = sortedtimes[len(sortedtimes)-2]
                    if distancebool == True:
                        # taking 1st place - first 2 indexes so that I can check whether a record has been broken 
                        recordcheck = sortedtimes[1]
                        recordcheckplayer = sortedtimes[0]
                    ageCategories = ["Year 7", "Year 8", "Year 9", "Year 10", "Senior", "Girls"]
                    # in the table in the database, the column names are similiar but not exactly the age category. I need to translate the fact that the year7 agecategory means updating the year7time, year7date,year7player columns.
                    columnEquivalentsTime = ["year7time", "year8time", "year9time", "year10time", "seniortime", "girlstime"]
                    columnEquivalentsDate = ["year7date", "year8date", "year9date", "year10date", "seniordate", "girlsdate"]
                    columnEquivalentsPlayer = ["year7player", "year8player", "year9player", "year10player", "seniorplayer", "girlsplayer"]
                    columnTime = "" # will hold the translated column name
                    columnDate = "" # will hold the translated column name
                    columnTime = "" # will hold the translated column name
                    for i in range (0, len(ageCategories)):
                        if ageCategories[i] == age_category:
                            #iterates through the list and assigns the translated column names to the respective variables
                            columnTime = columnEquivalentsTime[i]
                            columnDate = columnEquivalentsDate[i]
                            columnPlayer = columnEquivalentsPlayer[i]
                    if age_category == "Year 11":
                        # special case scenario where year 11s are counted as seniors
                            columnTime = "seniortime"
                            columnDate = "seniordate"
                            columnPlayer = "seniorplayer"
                            if columnTime == "":
                                # presence check - if the columns did not manage to be translated then the user is directed back to the leaderboard page.
                                leaderboardpage(e)
                                return # prevents the next instructions from being executed and hence preventing any errors
                    select = f"""SELECT {columnTime} FROM "school_records"
                                    WHERE "event" = %s; """
                    cursor.execute(select, (event_name,))
                    # selects the current record
                    currentrecord = cursor.fetchone()
                    print(currentrecord)
                    if currentrecord is None:
                        # presence check - if no record was selected then the next instructions need to be skipped to prevent errors.
                        leaderboardpage(e)
                        return
                    currentrecord = timeToSeconds(currentrecord[0]) # converts the current record to seconds so that it can be compared correctly, note that if it is a distance based event nothing actually happens to the score as it will just be return back without any changes
                    recordchecktime = date.today().year # gets the current year, that way when the form is submitted it will retrieve the current year and hence the year in which the record was broken.
                    if timebool == True:
                        # if it is a timebased event then the better results is the result that took less time as opposed to if it was a distance based event in which case the greater distance is the better result.
                        if recordcheck < currentrecord:
                            # if the record is broken then the new time, player and date are updated
                            updateTimeRecord = f"""UPDATE "school_records"
                                                  SET  {columnPlayer} = %s,
                                                       {columnDate} = %s,
                                                       {columnTime} = %s
                                                  WHERE event = %s;  """
                            cursor.execute(updateTimeRecord, (recordcheckplayer, recordchecktime, secondsToDisplay(recordcheck), event_name))
                            connection.commit()
                    if distancebool == True:
                        if recordcheck > currentrecord:
                            # if the record is broken then the new time, player and date are updated
                            updateDistanceRecord = f"""UPDATE "school_records"
                                                  SET  {columnPlayer} = %s,
                                                       {columnDate} = %s,
                                                       {columnTime} = %s
                                                  WHERE event = %s;  """
                            cursor.execute(updateDistanceRecord, (recordcheckplayer, recordchecktime,recordcheck, event_name))
                            connection.commit()
                leaderboardpage(e)
                # after the records have been checked and results entered into the respectives tables in the database the user is led back to the original page - leaderboardpage
            def searchFunction(e): 
                # function to search for the event that the user inputs
                value = searchbar.value # retrieves the inputted event
                index = -1 # initialises the index variable which will store the index at which the event the user searched for can be found
                page.session.set("event", "") # resets the event variable to "" so that any previous values it had are cleaned and the results are not accidentally written to the old event value.
                for i in range (0,len(optionsCleaned)):
                    current = optionsCleaned[i]
                    # iterates through the list 1 by 1
                    if value.lower() in current.lower():
                        #if the user input and event name match then this index at which the match occurs is stored for later
                        index = i
                    if index != -1:
                        # if a match was found then the index is used to assign event the eventname
                        page.session.set("event", optionsCleaned[index])
                    else:
                        # if no match was found then event is set to ""
                        page.session.set("event", "")
                if index == -1:
                    # if no index/match was found that means the user has not input a valid event and will be prompted to do so - validation check
                    invalid.visible = True
                    Event.visible = False
                    page.update()
                else:
                    # if an index/match was found then the user is notified of the event that they have slected via:
                    Event.value = "You have selected event: " + (page.session.get("event") or "")
                    Event.visible = True
                    invalid.visible = False
                    page.update()

            # defines text that goes on screen which instruct the user on how to use the form
            instruction1 = flet.Text(value = "This is the event entry form which you can use to record the results of the Sports Day events!", color = "Green", size = 20)
            instruction2 = flet.Text(value = "1. Type in the event you would like to record a result for and press submit, to select a different event simply re-type and submit again!", color = "Green", size = 20)
            instruction3 = flet.Text(value = "2. You should search for the event in this format: 'Year 7 100m A'", color = "Green", size = 20)
            instruction4 = flet.Text(value = "3. Select the position of the houses via the dropdown form, if there was a tie simply allocate the same position!", color = "Green", size = 20)
            instruction5 = flet.Text(value = "4. If the event is Tug of War the leave the player name and time/distance empty!", color = "Green", size = 20)
            instruction6 = flet.Text(value = "5. For the 800m, 1500m and Relay events enter the time as min:secs like 1:08 and for all other events keep the time in seconds!", color = "Green", size = 20)
            page.add(instruction1)
            page.add(instruction2)
            page.add(instruction3)
            page.add(instruction4)
            page.add(instruction5)
            page.add(instruction6)
            #creates a searchbar that the user is able to input the event they want to select, into
            searchbar = flet.TextField(
                label = "Search for event ...",
            )
            page.add(searchbar)
            submit = flet.ElevatedButton(text = "Submit", width = 200, height = 50, on_click = searchFunction) # creates a submit button that calls searchFunction when clicked which will select the event that the user has searched for.
            invalid = flet.Text("Invalid event try again", visible = False, color = "Red") # creates an error message whose visibilty can be toggled to True or False depending on whether the validation checks are passed or not.
            page.add(invalid)
            Event = flet.Text("You have selected event: ", visible = False, color = "Green")# creates message letting the user know what event the have selected, visibilty is toggled based on whether validation checks are passed or not.
            page.add(Event)
            page.add(submit)
            # creates dropdown to gather the position of bridges in the event
            bridgesdd = flet.Dropdown(
                    label = "Bridges Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # creates dropdown to gather the position of carew in the event
            carewdd = flet.Dropdown(
                    label = "Carew Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # creates dropdown to gather the position of mandeville in the event
            mandevilledd = flet.Dropdown(
                    label = "Mandeville's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # creates dropdown to gather the position of radcliffe in the event
            radcliffedd = flet.Dropdown(
                    label = "Radcliffe's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # creates dropdown to gather the position of ruskin in the event
            ruskindd = flet.Dropdown(
                    label = "Ruskin's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # creates dropdown to gather the position of woodcote in the event
            woodcotedd = flet.Dropdown(
                    label = "Woodcote's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            page.add(flet.Row(controls = [
                bridgesdd,
                carewdd,
                mandevilledd,
                radcliffedd,
                ruskindd,
                woodcotedd
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            ))
            # Creates a textbox for each respective house to gather the names of all the athletes who competed in the event:
            bridgesplayer = flet.TextField(
                label = "Enter the Bridges player's name ...", width = 200
            )
            carewplayer = flet.TextField(
                label = "Enter the Carew player's name ...", width = 200
            )
            mandevilleplayer = flet.TextField(
                label = "Enter the Mandeville player's name ...", width = 200
            )
            radcliffeplayer = flet.TextField(
                label = "Enter the Radcliffe player's name ...", width = 200
            )
            ruskinplayer = flet.TextField(
                label = "Enter the Ruskin player's name ...", width = 200
            )
            woodcoteplayer = flet.TextField(
                label = "Enter the Woodcote player's name ...", width = 200
            )
            page.add(flet.Row(controls = [ 
                bridgesplayer,
                carewplayer,
                mandevilleplayer,
                radcliffeplayer,
                ruskinplayer,
                woodcoteplayer
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            ))
            # Creates a textbox for each respective house to gather the times/distances of all the athletes who competed in the event:
            bridgesplayertime = flet.TextField(
                label = "Enter the Bridges player's time/distance  ...", width = 200
            )
            carewplayertime = flet.TextField(
                label = "Enter the Carew player's time/distance ...", width = 200
            )
            mandevilleplayertime = flet.TextField(
                label = "Enter the Mandeville player's time/distance ...", width = 200
            )
            radcliffeplayertime = flet.TextField(
                label = "Enter the Radcliffe player's time/distance ...", width = 200
            )
            ruskinplayertime = flet.TextField(
                label = "Enter the Ruskin player's time/distance ...", width = 200
            )
            woodcoteplayertime = flet.TextField(
                label = "Enter the Woodcote player's time/distance ...", width = 200
            )
            page.add(flet.Row(controls = [ 
                bridgesplayertime,
                carewplayertime,
                mandevilleplayertime,
                radcliffeplayertime,
                ruskinplayertime,
                woodcoteplayertime
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            ))
            submit = flet.ElevatedButton(text = "Submit results!", width = 300, height = 100, on_click = dropdown) # adds a submit button that when clicked will go ahead and update the relevant tables and check the athletics records and update them if need be
            page.add(submit)
        searchBar(optionsCleaned) # creates a searchbar for the user to search for the event
        presenceMessage0 = flet.Text("Please make sure to select an event!", color = "red", visible = False) # message to prompt the user to enter the relevant details as a result of a presence check
        page.add(presenceMessage0)
        presenceMessage1 = flet.Text("Please make sure each House is allocated a position via the dropdowns!", color = "red", visible = False)# message to prompt the user to enter the relevant details as a result of a presence check
        page.add(presenceMessage1)
        presenceMessage2 = flet.Text("Please make sure each House's representative's name and time/distance are entered!", color = "red", visible = False)# message to prompt the user to enter the relevant details as a result of a presence check
        page.add(presenceMessage2)
        colonmessage = flet.Text("For the 800m, 1500m and Relay events enter the time as min:secs like 1:08 and for all other events keep the time in seconds!", color = "red", visible = False)# message to prompt the user to enter the relevant details in the correct format as a result of a format check
        page.add(colonmessage)
        BACKBUTTON1 = backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = EEBclicked) # Creates a button that allows user to go back to the previous page
        page.add(BACKBUTTON1)
    def houseEventsButtonClicked(e):
        # This is the function called when the user opts to enter event results for a normal Cock House Cup event rather than a sports day event
        page.controls.clear()
        page.session.set("event", "") # resets the event variable to "" so that any previous values it had are cleaned and the results are not accidentally written to the old event value.
        page.scroll = flet.ScrollMode.AUTO
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = EEBclicked) # Creates a button that allows user to go back to the previous page
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        # selects all the hoouse events from the database
        select = """ SELECT house_event FROM house_event_list ; """
        cursor.execute(select)
        fetch = cursor.fetchall()
        options = fetch # stores the fetched house events to the options list which is currently in a tuple format
        optionsCleaned = []
        for i in range(0, len(options)):
            # "Cleans" the list extracting the event name from the tuple
            optionsCleaned.append(options[i][0])
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.theme_mode= flet.ThemeMode.DARK
        page.add(flet.Text(value = "Enter Event results", color = "Red", size = 50))
        def searchBar(optionsCleaned):
            # This function creates a searchbar for the user to input the event they would like to enter the result for, called when the submit button is clicked.
            def dropdown(e):
                # This function inserts the results that the user enters, called when the submit results button is clicked
                bpos = bridgesdd.value
                cpos = carewdd.value
                mpos = mandevilledd.value
                rapos = radcliffedd.value
                rupos = ruskindd.value
                wpos = woodcotedd.value
                rank = [bpos, cpos, mpos, rapos, rupos, wpos]
                # Retrieves all of the user's inputs for the position of the houses and adds them to a list called rank
                if None in rank:
                    # presence check making sure that the user has allocated a position for every single house
                    presenceMessage.visible = True
                    page.update()
                    return
                if searchbar.value == "":
                    # presence check making sure that the user has selected an event to enter the results for
                    presenceMessage.visible = True
                    page.update()
                    return
                point = []
                weightedEvents = ["House Music", "House Drama"] # identifiers/keywords that will be found in the event's name if the event is weighted
                if weightedEvents[0] not in (page.session.get("event") or "") and weightedEvents[1] not in (page.session.get("event") or ""):
                    # if it is not a weighted event then:
                    for i in range(0, len(rank)):
                        # Iteratively adds the number of points each house should get
                        point.append(7 - int(rank[i]))
                    # updates/inserts the results for bridges, writes the number of points awarded from the event
                    insertBridges = """UPDATE "bridges_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s;"""
                    cursor.execute(insertBridges,(point[0],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the results for carew, writes the number of points awarded from the event
                    insertCarew = """UPDATE "carew_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertCarew,(point[1],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the results for mandeville, writes the number of points awarded from the event
                    insertMandeville = """UPDATE "mandeville_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertMandeville,(point[2],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the results for radcliffe, writes the number of points awarded from the event
                    insertRadcliffe = """UPDATE "radcliffe_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRadcliffe,(point[3],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the results for ruskin, writes the number of points awarded from the event
                    insertRuskin = """UPDATE "ruskin_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRuskin,(point[4],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the results for woodcote, writes the number of points awarded from the event
                    insertWoodcote = """UPDATE "woodcote_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertWoodcote,(point[5],(page.session.get("event") or "")))
                    connection.commit()
                else:
                    # If it is a weighted event then:
                    weightedrank = ["1", "2", "3", "4", "5", "6"]
                    weightedpoints = ["9", "7", "5", "3", "2", "1"]
                    # Iteratively adds the points each house should be allocated based on the position of the house.
                    # The position of the house is found in the weighted rank list and the index at which it is found is the same index where the weighted point score for the respective position can be found
                    for i in range (0, len(weightedrank)):
                        for j in range(0, 6):
                            if rank[i] == weightedrank[j]:
                                point.append(weightedpoints[j])    
                    # updates/inserts the weighted results for bridges, writes the number of points awarded from the event
                    insertBridges = """UPDATE "bridges_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s;"""
                    cursor.execute(insertBridges,(point[0],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the weighted results for carew, writes the number of points awarded from the event
                    insertCarew = """UPDATE "carew_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertCarew,(point[1],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the weighted results for mandeville, writes the number of points awarded from the event
                    insertMandeville = """UPDATE "mandeville_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertMandeville,(point[2],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the weighted results for radcliffe, writes the number of points awarded from the event
                    insertRadcliffe = """UPDATE "radcliffe_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRadcliffe,(point[3],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the weighted results for ruskin, writes the number of points awarded from the event
                    insertRuskin = """UPDATE "ruskin_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRuskin,(point[4],(page.session.get("event") or "")))
                    connection.commit()
                    # updates/inserts the weighted results for woodcote, writes the number of points awarded from the event
                    insertWoodcote = """UPDATE "woodcote_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertWoodcote,(point[5],(page.session.get("event") or "")))
                    connection.commit()
                # After the results have been submitted and updated in the database the user is lead back to the homepgae/leaderboardpage
                leaderboardpage(e)
            def searchFunction(e): 
                # Function that pairs the user's input with the appropriate event.
                value = searchbar.value # retrieves value input by the user
                index = -1 # initialises the index variable which will store the index at which the event the user searched for can be found
                page.session.set("event", "")  # resets the event variable to "" so that any previous values it had are cleaned and the results are not accidentally written to the old event value.
                for i in range (0,len(optionsCleaned)):
                    # iterates through the list 1 by 1
                    current = optionsCleaned[i]
                    if value.lower() in current.lower():
                        index = i
                        #if the user input and event name match then this index at which the match occurs is stored for later
                    if index != -1:
                        # if a match was found then the index is used to assign event the eventname
                        page.session.set("event", optionsCleaned[index])
                    else:
                        # if no match was found then event is set to ""
                        page.session.set("event", "")
                if index == -1:
                    # if no index/match was found that means the user has not input a valid event and will be prompted to do so - validation check
                    invalid.visible = True
                    Event.visible = False
                    page.update()
                else:
                    # if an index/match was found then the user is notified of the event that they have slected via:
                    Event.value = "You have selected event: " + (page.session.get("event") or "")
                    Event.visible = True
                    invalid.visible = False
                    page.update()
            # defines text that goes on screen which instruct the user on how to use the form
            instruction1 = flet.Text(value = "This is the event entry form which you can use to record the results of events.", color = "Green", size = 20)
            instruction2 = flet.Text(value = "1. Type in the event you would like to record a result for and press submit, to select a different event simply re-type and submit again!", color = "Green", size = 20)
            instruction3 = flet.Text(value = "2. Select the position of the houses via the dropdown form, if there was a tie simply allocate the same position!", color = "Green", size = 20)
            page.add(instruction1)
            page.add(instruction2)
            page.add(instruction3)
            # add a searchbar for the user to input the event they want to submit the result for
            searchbar = flet.TextField(
                label = "Search for event ...",
            )
            page.add(searchbar)
            submit = flet.ElevatedButton(text = "Submit", width = 200, height = 50, on_click = searchFunction) # submit button that when clicked will go and retrieve/match the userinput with the full eventname
            page.add(submit)
            invalid = flet.Text("Invalid event try again", visible = False, color = "Red") # Prompts use to enter a valid event when no match is found - validation checks are not passed, displayed via toggling visibility between true and false when validation checks are passed or not
            page.add(invalid)
            Event = flet.Text("You have selected event: ", visible = False, color = "Green") # Tells the user what event they have selected after all validation checks have been passed, displayed via toggling visibility between truue and false when validation checks are passed or not
            page.add(Event)
            # Creates a dropdown where the user can allocate the position of bridges in the event
            bridgesdd = flet.Dropdown(
                    label = "Bridges Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # Creates a dropdown where the user can allocate the position of carew in the event
            carewdd = flet.Dropdown(
                    label = "Carew Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # Creates a dropdown where the user can allocate the position of mandeville in the event
            mandevilledd = flet.Dropdown(
                    label = "Mandeville's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # Creates a dropdown where the user can allocate the position of radcliffe in the event
            radcliffedd = flet.Dropdown(
                    label = "Radcliffe's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # Creates a dropdown where the user can allocate the position of ruskin in the event
            ruskindd = flet.Dropdown(
                    label = "Ruskin's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            # Creates a dropdown where the user can allocate the position of woodcote in the event
            woodcotedd = flet.Dropdown(
                    label = "Woodcote's Position",
                    options = [
                        flet.dropdown.Option(1),
                        flet.dropdown.Option(2),
                        flet.dropdown.Option(3),
                        flet.dropdown.Option(4),
                        flet.dropdown.Option(5),
                        flet.dropdown.Option(6)
                    ],
                    width = 200
                )
            page.add(flet.Row(controls = [
                bridgesdd,
                carewdd,
                mandevilledd,
                radcliffedd,
                ruskindd,
                woodcotedd
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            ))
            submit = flet.ElevatedButton(text = "Submit results!", width = 300, height = 100, on_click = dropdown) # Creates a submit results button that when clicked will call the drop down function which will write the results to the database
            page.add(submit)
            presenceMessage = flet.Text("Please make sure all details are provided by filling all the boxes!", color = "red", visible = False) # Creates the error message that will be displayed when the presence check is failed, prompting the user to enter all the details needed.
            page.add(presenceMessage)
            successText = flet.Text("Results sucessfully submitted!", color = "green", visible = False) # Creates message that lets the user know that the resuls have been correctly submitted and written to the database
            page.add(successText)
            BACKBUTTON = backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = EEBclicked)# Creates a back button that when clicked leads the user back to the previous page
            page.add(BACKBUTTON)
            page.update()
        searchBar(optionsCleaned) # Calls the searchBar function which will display the form on the page for the user to input into.
    def individualResetButtonClicked(e):
        # This is the function called when the user clicks the individual event reset button.
        # This function will be used to deleted any entries about that specific event that the user inputs.
        page.controls.clear()
        page.update()
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.add(flet.Text(value = "Search for the event for which you would like to erase the result of!", color = "Blue", size = 50))
        # Creates searchbar for user to input the event they would like to reset the result of
        searchbar = flet.TextField(
                label = "Search for event ...",
            )
        page.add(searchbar)
        def submitButtonClicked(e):
            # This function is called when the submit button is clicked, which is the final check and verification before the system will actually go ahead and delete the result for that specfic event.
            selectnormalevents = """SELECT * FROM "house_event_list"; """ # selects all the house events from the database table - house_event_list
            cursor.execute(selectnormalevents)
            listnormal = cursor.fetchall() # stores these fetched house events to the list - listnormal
            selectsportsdayevents = """SELECT "event" FROM "sports_day_events";  """ # selects all of the sports day events
            cursor.execute(selectsportsdayevents)
            listsportsday = cursor.fetchall() # stores these fetched sports day events to the list - listsportsday
            eventList = [] # This will be a list of every single possible event including both the sportsday events as well as normal Cock House Cup events too!
            for i in range(0, len(listnormal)):
                # The events are all in tuple format which are iteratively extracted and appended to the eventList
                eventList.append(listnormal[i][0])
            for i in range(0, len(listsportsday)):
                # The events are all in tuple format which are iteratively extracted and appended to the eventList
                eventList.append(listsportsday[i][0])
            input = searchbar.value # retrieves the user's input in the searchbar
            index = -1 # initialises the index variable which will store the index at which the event the user searched for can be found
            event = ""
            for i in range (0,len(eventList)):
                current = eventList[i]
                # iterates through the list one by one
                if input.lower() in current.lower():
                    # if a match is found the current index is saved
                    index = i
                if index != -1:
                    # if a match was found then the full eventname that is found at that index is stored to event for later
                    event = eventList[index]
                else:
                    # if no match was found the event is set to ""
                    event = ""
            page.session.set("index", index) # because the index at which the userinput's match can be found, each user will need their own personal version of index so as to not overwrite each others indexes. 
            page.session.set("event", event) # the same goes for event where each user needs their own personal version of this variable to prevent inteference when multiple users are on the system
            if index == -1:
                # validation check - if no index was found the user's input was not valid and need to try again, which they will be prompted to do, by toggling the invalid message's visibilty to True
                invalid.visible = True
                Event.visible = False
                clearButton.visible = False # Removes the clear button from the screen as no event to clear has been selected yet.
                page.update()
            else:
                Event.value = "You have selected event: " + event # lets the user know what event they have selected
                Event.visible = True # visibility is toggled to true so that the user can see this message and therefore see what event they have selected and are about to reset the result of.
                invalid.visible = False
                clearButton.visible = True # The clear button is now added to the screen since now an event to reset has been selected.
                page.update()
        def clearButtonClicked(e):
            # When the user decides to click the clear button the event results will need to be reset in the database which this function will do.
            if (page.session.get("index") if page.session.get("index") is not None else -1) < 39:
                # The above selection statement says that if the session index < 39 then do :
                # But first it checks that index has a value which is not "None", but if the value is None use -1 instead to prevent errors from being caused.
                # The reason for checking whether the index is less than 39 is because all of the normal Cock House Cup events where appedended to the list first and there are 38 events. This differentiation of the type of event via the index of it will tell me which tables I need to update due to whether it is a normal house event or a sportsday event.
                # Resets the bridges for that specific event, indicated by the where clause of the query, points back to 0
                erasebridges = """UPDATE "bridges_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasebridges, ((page.session.get("event") or ""),))
                connection.commit()
                # Resets the carew points for that specific event, indicated by the where clause of the query, back to 0
                erasecarew = """UPDATE "carew_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasecarew, ((page.session.get("event") or ""),))
                connection.commit()
                # Resets the mandeville points for that specific event, indicated by the where clause of the query, back to 0
                erasemandeville = """UPDATE "mandeville_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasemandeville, ((page.session.get("event") or ""),))
                connection.commit()
                # Resets the radcliffe points for that specific event, indicated by the where clause of the query, back to 0
                eraseradcliffe = """UPDATE "radcliffe_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(eraseradcliffe, ((page.session.get("event") or ""),))
                connection.commit()
                # Resets the ruskin points for that specific event, indicated by the where clause of the query, back to 0
                eraseruskin = """UPDATE "ruskin_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(eraseruskin, ((page.session.get("event") or ""),))
                connection.commit()
                # Resets the woodcote points for that specific event, indicated by the where clause of the query, back to 0
                erasewoodcote = """UPDATE "woodcote_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasewoodcote, ((page.session.get("event") or ""),))
                connection.commit()
            if (page.session.get("index") if page.session.get("index") is not None else -1) > 38:
                # The above selection statement says that if the session index > 38 then do :
                # But first it checks that index has a value which is not "None", but if the value is None use -1 instead to prevent errors from being caused.
                # If the index is greater than 38 this means that it is a sports day event.
                erasesportsday = """UPDATE "sports_day_events"
                                            SET bridgespoints = 0,
                                              carewpoints = 0,
                                                mandevillepoints = 0,
                                                  radcliffepoints = 0,
                                                    ruskinpoints = 0,
                                                     woodcotepoints = 0
                                                     WHERE event = %s; """
                cursor.execute(erasesportsday, ((page.session.get("event") or ""),))
                connection.commit()
                # This query above will reset all the points each house was allocated for the event
                if "Tug of War" not in (page.session.get("event") or ""):
                    # Must check whether the event is tug of war since tug of war only stores data in this table and is not in any other table, so if the individual event to be reset was tug of war then the results has now completely been reset.
                    # if the event was not tug of war then the player name and time/distance still needs to be erased
                    timeEvents = ["100m", "200m", "300m", "400m", "800m", "1500m", "Relay"] # keywords/identifiers for time based events
                    distanceEvents = ["Javelin", "Discus", "Shotput", "Long Jump", "Triple Jump", "High Jump"] # keywords/identifiers for distance based events
                    timebool = False # Stores whether event is time based or not
                    distancebool = False # Stores whether event is distance based or not
                    for i in range(0,len(timeEvents)):
                        if timeEvents[i] in (page.session.get("event") or ""):
                            timebool = True # if keyword for time based events is in the event name then the event is time based - toggled to true
                    for i in range(0,len(distanceEvents)):
                        if distanceEvents[i] in (page.session.get("event") or ""):
                            distancebool = True # if keyword for distance based events is in the event name then the event is distance based - toggled to true
                    if timebool == True:
                        # if time based then the results need to be erased from the sports_day_times table
                        erasetimeplayer = """UPDATE "sports_day_times"
                                        SET player_bridges = NULL,
                                          player_bridges_time = NULL,
                                            player_carew = NULL,
                                              player_carew_time = NULL,
                                                player_mandeville = NULL,
                                                  player_mandeville_time = NULL,
                                                    player_radcliffe = NULL,
                                                      player_radcliffe_time = NULL,
                                                        player_ruskin = NULL,
                                                          player_ruskin_time = NULL,
                                                            player_woodcote = NULL,
                                                             player_woodcote_time = NULL
                                                             WHERE event = %s; """
                        cursor.execute(erasetimeplayer, ((page.session.get("event") or ""),))
                        connection.commit()
                        # resets all the columns for that row aside from the event and row_order column to null
                    if distancebool == True:
                        # if distance based then the results need to be erased from the sports_day_distances table
                        erasedistanceplayer = """UPDATE "sports_day_distances"
                                        SET player_bridges = NULL,
                                          player_bridges_distance = NULL,
                                            player_carew = NULL,
                                              player_carew_distance = NULL,
                                                player_mandeville = NULL,
                                                  player_mandeville_distance = NULL,
                                                    player_radcliffe = NULL,
                                                      player_radcliffe_distance = NULL,
                                                        player_ruskin = NULL,
                                                          player_ruskin_distance = NULL,
                                                            player_woodcote = NULL,
                                                             player_woodcote_distance = NULL
                                                             WHERE event = %s; """
                        cursor.execute(erasedistanceplayer, ((page.session.get("event") or ""),))
                        connection.commit()
                        # resets all the columns for that row aside from the event and row_order column to null
            # returns the user back to the leaderboard page or homepage once this is done
            leaderboardpage(e)
        submitButton = flet.ElevatedButton(text = "Submit", width = 150, height = 75, on_click = submitButtonClicked) # Creates the submit button that when clicked will search and select the appropriate event that the user wants to reset
        page.add(submitButton)
        invalid = flet.Text("Invalid event try again", visible = False, color = "Red") # Creates the error message that tells the user to enter a valid event, visibility is toggled to true when validation checks are not passed.
        page.add(invalid)
        Event = flet.Text("You have selected event: ", visible = False, color = "Green") # Creates message to let user know what event's result they are about to reset.
        page.add(Event)
        clearButton = flet.ElevatedButton(text = "Clear Results", visible = False, width = 150, height = 75, color = "Red",on_click = clearButtonClicked) # # Creates the submit button that when clicked will actually go ahead and reset the event's result
        page.add(clearButton)
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = adminButtonClicked) # Creates a back button that when clicked will lead the user back to the previous page
        page.add(backButton)
    def masterResetButtonClicked(e):
        # This is the function that when called will reset every single event result in the whole system
        page.controls.clear()
        page.update()
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        def yesButtonClicked(e):
            # This function is called after the user confirms that they want to reset the results of every single event in the system
            page.controls.clear()
            page.update()
            page.theme_mode= flet.ThemeMode.DARK
            page.vertical_alignment = flet.MainAxisAlignment.CENTER
            page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
            page.add(flet.Text(value = "All events have been reset successfully!", color = "green", size = 75)) # Creates a message letting the user know that all event results have been reset successfully.
            backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = adminButtonClicked) # Creates a back button that when clicked leads the user back to the previous page
            page.add(backButton)
            # Resets the entire points column in the bridges table
            reset_bridges_events = """UPDATE "bridges_events"
                                        SET points = '0';  """
            # Resets the entire points column in the carew table
            reset_carew_events = """UPDATE "carew_events"
                                        SET points = '0';  """
            # Resets the entire points column in the mandeville table
            reset_mandeville_events = """UPDATE "mandeville_events"
                                        SET points = '0';  """
            # Resets the entire points column in the radcliffe table
            reset_radcliffe_events = """UPDATE "radcliffe_events"
                                        SET points = '0';  """
            # Resets the entire points column in the ruskin table
            reset_ruskin_events = """UPDATE "ruskin_events"
                                        SET points = '0';  """
            # Resets the entire points column in the woodcote table
            reset_woodcote_events = """UPDATE "woodcote_events"
                                        SET points = '0';  """
            # Resets all the columns aside from event and row_order in the sports_day_distances table
            reset_sports_day_distances = """UPDATE "sports_day_distances"
                                        SET player_bridges = NULL,
                                          player_bridges_distance = NULL,
                                            player_carew = NULL,
                                              player_carew_distance = NULL,
                                                player_mandeville = NULL,
                                                  player_mandeville_distance = NULL,
                                                    player_radcliffe = NULL,
                                                      player_radcliffe_distance = NULL,
                                                        player_ruskin = NULL,
                                                          player_ruskin_distance = NULL,
                                                            player_woodcote = NULL,
                                                             player_woodcote_distance = NULL; """
            # Resets all the columns aside from event and row_order in the sports_day_events table
            reset_sports_day_events = """UPDATE "sports_day_events"
                                            SET bridgespoints = 0,
                                              carewpoints = 0,
                                                mandevillepoints = 0,
                                                  radcliffepoints = 0,
                                                    ruskinpoints = 0,
                                                     woodcotepoints = 0; """
            # Resets all the columns aside from event and row_order in the sports_day_times table
            reset_sports_day_times = """UPDATE "sports_day_times"
                                        SET player_bridges = NULL,
                                          player_bridges_time = NULL,
                                            player_carew = NULL,
                                              player_carew_time = NULL,
                                                player_mandeville = NULL,
                                                  player_mandeville_time = NULL,
                                                    player_radcliffe = NULL,
                                                      player_radcliffe_time = NULL,
                                                        player_ruskin = NULL,
                                                          player_ruskin_time = NULL,
                                                            player_woodcote = NULL,
                                                             player_woodcote_time = NULL; """
            #Executes all of these above queries
            cursor.execute(reset_bridges_events)
            connection.commit()
            cursor.execute(reset_carew_events)
            connection.commit()
            cursor.execute(reset_mandeville_events)
            connection.commit()
            cursor.execute(reset_radcliffe_events)
            connection.commit()
            cursor.execute(reset_ruskin_events)
            connection.commit()
            cursor.execute(reset_woodcote_events)
            connection.commit()
            cursor.execute(reset_sports_day_distances)
            connection.commit()
            cursor.execute(reset_sports_day_events)
            connection.commit()
            cursor.execute(reset_sports_day_times)
            connection.commit()
        instruction = flet.Text("Do you want to reset the results for every single event?") # Creates message asking user if they really want to reset the result of every event
        yesButton = flet.ElevatedButton(text = "Yes", color = "Green", width = 300, height = 100, on_click = yesButtonClicked) # If clicked then calls yesButtonClicked function which will go ahead and reset every single event result
        noButton = flet.ElevatedButton(text = "No", color = "Red", width = 300, height = 100, on_click = adminButtonClicked) # If clicked then user does not want to execute a master reset and hence will be lead back to the previous page by calling the adminButtonClicked function
        page.add(instruction)
        page.add(flet.Row(
            controls = [yesButton, noButton],
            alignment=flet.MainAxisAlignment.CENTER
        ))
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = adminButtonClicked) # Creates a back button that when clicked will lead the user back to the previous page
        page.add(backButton)
    def adminButtonClicked(e):
        # function called when the admin button is clicked
        def adminButtonClickedPostLogin():
            # function for when the user is actually logged in and hence can access the features of the admin section
            page.session.set("logged_in", True)
            page.controls.clear()
            page.update()
            page.theme_mode= flet.ThemeMode.DARK
            page.vertical_alignment = flet.MainAxisAlignment.CENTER
            page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
            masterResetButton = flet.ElevatedButton(text = "Master Reset", width = 300, height = 100, color = "red", on_click = masterResetButtonClicked) # Creates the master reset button that when clicked will lead the user to a page asking if they truly want to reset every single result. When clicked it calls the masterResetButtonClicked function.
            individualResetButton = flet.ElevatedButton(text = "Individual event reset", width = 300, height = 100, color = "red", on_click = individualResetButtonClicked) # Creates the individual reset button that when clicked will call the individualResetButtonClicked function which will allow the user to first search for the even that they would like to reset the result of.
            page.add(flet.Row(
                controls = [masterResetButton, individualResetButton],
                alignment=flet.MainAxisAlignment.CENTER
            ))
            backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage) # Creates a back button that when clicked will lead the user back to the previous page
            page.add(backButton)
        if page.session.get("logged_in") == True:
            # If user is logged in go straight to displaying the next page by calling the function below:
            adminButtonClickedPostLogin()
        else:
            # if the user is not logged in the must first login:
            page.controls.clear()
            page.update()
            login_page(page, on_success = adminButtonClickedPostLogin, on_back = leaderboardpage)
            # on_success defines that when the login is successful then adminButtonClickedPostLogin function should be called
            # on_back defines that when the user clicks the back button the leaderboardpage function should be called which just leads the user back to the previous page.
    def leaderboardpage(e):
        # This is the homepage function or the original screen
        page.controls.clear()
        page.scroll = None
        page.theme_mode= flet.ThemeMode.DARK
        standingsButton = flet.ElevatedButton(text = "Cock House Cup standings", width = 275, height = 100, on_click = CHCSclicked)    # Creates a button for the overall standings
        individualButton = flet.ElevatedButton(text = "Individual event results", width = 275, height = 100, on_click = IERclicked)   # Creates a button for the individual standing
        sportsdayButton = flet.ElevatedButton(text = "Sports day results", width = 275, height = 100, on_click = SDRclicked)          # Creates a button for sports day related features
        eventEntryButton = flet.ElevatedButton(text = "Event Score Entry", width = 275, height = 100, on_click = EEBclicked)          # Creates a button for the eventy entry forms
        adminButton = flet.ElevatedButton(text = "Admin", width = 275, height = 100, color = "red", on_click = adminButtonClicked)    # Creates a button for the admin section
        page.add(
            flet.Column(
                [
                    flet.Row(
                        controls=[
                            standingsButton,
                            individualButton,
                            sportsdayButton,
                            eventEntryButton,
                            adminButton
                        ],
                        alignment="center",   # aligns button to centre horizontally
                        spacing=15,
                        expand=True           # Row expands across width
                    )
                ],
                alignment="center",           # aligns button to centre vertically
                horizontal_alignment="center",
                expand=True                   # Column expands across height
            )
        )
        page.update()
        # The buttons have been added to the page and the page is displayed on screen by calling the function
    leaderboardpage(page)

if __name__ == "__main__":
    flet.app(main) # Creates the GUI
