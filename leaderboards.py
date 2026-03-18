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
            # retrieve the user's input for what event they want to see the result of:
            userinput = sportsDaySearchBar.value
            selectedEvent = ""
            for i in range(0,len(sportsDayEventsCleaned)):
                iterateEvent = sportsDayEventsCleaned[i]
                if userinput.lower() in iterateEvent.lower():
                    selectedEvent = sportsDayEventsCleaned[i]
            selectedEventMessage = flet.Text(value = ("You have selected event: " + selectedEvent), visible = False, color = "Green")
            page.add(selectedEventMessage)
            if selectedEvent == "":
                errorMessage.visible = True
                selectedEventMessage.visible = False
                page.update()
                return
            else:
                selectedEventMessage.visible = True
                errorMessage.visible = False
                page.update()
            page.update()
            selectPoints = """SELECT "bridgespoints", "carewpoints", "mandevillepoints", "radcliffepoints", "ruskinpoints", "woodcotepoints"
                                FROM "sports_day_events"
                                WHERE "event" = %s;  """
            cursor.execute(selectPoints, (selectedEvent,))
            points = cursor.fetchall()
            houseANDpoints = ["Bridges", 0, "Carew", 0, "Mandeville", 0, "Radcliffe", 0, "Ruskin", 0, "Woodcote", 0]
            for i in range(1, 7):
                houseANDpoints[(2*i)-1] = points[0][i-1]
            bubbleSort(houseANDpoints)
            page.controls.clear()
            page.update()
            page.add(flet.Text(selectedEvent, color = "Red", size = 50))
            create_leaderboard(houseANDpoints)
            back = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = ISDLclicked)
            page.add(back)
        page.controls.clear()
        page.update()
        select_sports_day_events = """SELECT "event" FROM "sports_day_events";  """
        cursor.execute(select_sports_day_events)
        global sportsDayEvents
        sportsDayEvents = cursor.fetchall()
        sportsDayEventsCleaned = []
        for i in range(0, len(sportsDayEvents)):
            sportsDayEventsCleaned.append(sportsDayEvents[i][0])
        sportsDaySearchBar = flet.TextField(label = "Enter event you would like to see the leaderboard for...")
        page.add(sportsDaySearchBar)
        SUBMIT = flet.ElevatedButton(text = "Search", on_click = sportsDaySearch, width = 150, height = 60)
        page.add(SUBMIT)
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = SDRclicked)
        page.add(backButton)
        selectedEvent = ""
        selectedEventMessage = flet.Text(value = ("You have selected event: " + selectedEvent), visible = False, color = "green")
        errorMessage = flet.Text("Please enter an actual event!", visible = False, color = "Red")
        page.add(selectedEventMessage)
        page.add(errorMessage)
    def OSDLButtonClicked(e):
        page.controls.clear()
        page.scroll = None
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.update()
        selectbridgespoints = """SELECT sum(bridgespoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectbridgespoints)
        bridgespoints = cursor.fetchone()
        bridgespoints = bridgespoints[0]
        selectcarewpoints = """SELECT sum(carewpoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectcarewpoints)
        carewpoints = cursor.fetchone()
        carewpoints = carewpoints[0]
        selectmandevillepoints = """SELECT sum(mandevillepoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectmandevillepoints)
        mandevillepoints = cursor.fetchone()
        mandevillepoints = mandevillepoints[0]
        selectradcliffepoints = """SELECT sum(radcliffepoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectradcliffepoints)
        radcliffepoints = cursor.fetchone()
        radcliffepoints = radcliffepoints[0]
        selectruskinpoints = """SELECT sum(ruskinpoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectruskinpoints)
        ruskinpoints = cursor.fetchone()
        ruskinpoints = ruskinpoints[0]
        selectwoodcotepoints = """SELECT sum(woodcotepoints)
                            FROM "sports_day_events";"""
        cursor.execute(selectwoodcotepoints)
        woodcotepoints = cursor.fetchone()
        woodcotepoints = woodcotepoints[0]
        houseANDpoints = ["Bridges", bridgespoints, "Carew", carewpoints, "Mandeville", mandevillepoints, "Radcliffe", radcliffepoints, "Ruskin", ruskinpoints, "Woodcote", woodcotepoints]
        houseANDpoints = bubbleSort(houseANDpoints)
        create_leaderboard(houseANDpoints)
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = SDRclicked)
        page.add(backButton)
    def EEBclicked(e):
        page.scroll = None
        def EEBClickedPostLogin():
            page.scroll = None
            page.session.set("logged_in", True)
            page.controls.clear()
            page.vertical_alignment = flet.MainAxisAlignment.CENTER
            page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
            page.update()
            backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage) # Creates a button that allows user to go back to the previous page
            sportsDayButton = flet.ElevatedButton(text = "Sports Day", width = 400, height = 100, on_click = sportsDayButtonClicked)
            houseEventsButton = flet.ElevatedButton(text = "House Events", width = 400, height = 100, on_click = houseEventsButtonClicked)
            page.add(
                sportsDayButton,
                houseEventsButton
            )
            page.add(
                backButton
                )
        if page.session.get("logged_in") == True:
            EEBClickedPostLogin()
        else:
            page.controls.clear()
            page.update()
            login_page(page, on_success= EEBClickedPostLogin, on_back= leaderboardpage)
    def sportsDayButtonClicked(e):
        page.controls.clear()
        page.session.set("event", "")
        page.scroll = flet.ScrollMode.AUTO
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.theme_mode= flet.ThemeMode.DARK
        page.add(flet.Text(value = "Enter Sports Day Event results", color = "Red", size = 50))
        select = """ SELECT event FROM sports_day_events; """
        cursor.execute(select)
        fetch = cursor.fetchall()
        options = fetch
        optionsCleaned = []
        for i in range(0, len(options)):
            optionsCleaned.append(options[i][0])
        timeEvents = ["100m", "200m", "300m", "400m", "800m", "1500m", "Relay"]
        distanceEvents = ["Javelin", "Discus", "Shotput", "Long Jump", "Triple Jump", "High Jump"]
        def searchBar(optionsCleaned):
            def dropdown(e):
                bpos = bridgesdd.value
                cpos = carewdd.value
                mpos = mandevilledd.value
                rapos = radcliffedd.value
                rupos = ruskindd.value
                wpos = woodcotedd.value
                rank = [bpos, cpos, mpos, rapos, rupos, wpos]
                if None in rank:
                    presenceMessage1.visible = True
                    page.update()
                    return
                if searchbar.value == "":
                    presenceMessage0.visible = True
                    page.update()
                    return
                if "Tug of War" not in (page.session.get("event") or ""):
                    list = [bridgesplayer.value, bridgesplayertime.value, carewplayer.value, carewplayertime.value,
                            mandevilleplayer.value, mandevilleplayertime.value, radcliffeplayer.value, radcliffeplayertime.value,
                            ruskinplayer.value, ruskinplayertime.value, woodcoteplayer.value, woodcoteplayertime.value]
                    if None in list or "" in list:
                        presenceMessage2.visible = True
                        page.update()
                        return
                colonrequired = ["800m", "1500m", "Relay"]
                for item in colonrequired:
                    if item in (page.session.get("event") or ""):
                        checks = [bridgesplayertime.value, carewplayertime.value, mandevilleplayertime.value, radcliffeplayertime.value, ruskinplayertime.value, woodcoteplayertime.value]
                        for item in checks:
                            if ":" not in item:
                                colonmessage.visible = True
                                page.update()
                                return
                point = []
                for i in range(0, len(rank)):
                    point.append(7 - int(rank[i]))
                if "Relay" in (page.session.get("event") or ""):
                    for i in range(0, len(point)):
                        point[i] = point[i]*2
                timebool = False
                distancebool = False
                for i in range(0,len(timeEvents)):
                    if timeEvents[i] in (page.session.get("event") or ""):
                        timebool = True
                for i in range(0, len(distanceEvents)):
                    if distanceEvents[i] in (page.session.get("event") or ""):
                        distancebool = True
                insertBridges = """UPDATE "sports_day_events"
                                SET "bridgespoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertBridges,(point[0], (page.session.get("event") or "")))
                connection.commit()
                insertCarew = """UPDATE "sports_day_events"
                                SET "carewpoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertCarew,(point[1],(page.session.get("event") or "")))
                connection.commit()
                insertMandeville = """UPDATE "sports_day_events"
                                SET "mandevillepoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertMandeville,(point[2],(page.session.get("event") or "")))
                connection.commit()
                insertRadcliffe = """UPDATE "sports_day_events"
                                SET "radcliffepoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertRadcliffe,(point[3],(page.session.get("event") or "")))
                connection.commit()
                insertRuskin = """UPDATE "sports_day_events"
                                SET "ruskinpoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertRuskin,(point[4],(page.session.get("event") or "")))
                connection.commit()
                insertWoodcote = """UPDATE "sports_day_events"
                                SET "woodcotepoints" = %s
                                WHERE "event" = %s;"""
                cursor.execute(insertWoodcote,(point[5],(page.session.get("event") or "")))
                connection.commit()
                if timebool == True:
                    updateplayerbridges = """UPDATE "sports_day_times"
                                SET "player_bridges" = %s,
                                    "player_bridges_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerbridges, (bridgesplayer.value, bridgesplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    
                    updateplayercarew = """UPDATE "sports_day_times"
                                SET "player_carew" = %s,
                                    "player_carew_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayercarew, (carewplayer.value, carewplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayermandeville = """UPDATE "sports_day_times"
                                SET "player_mandeville" = %s,
                                    "player_mandeville_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayermandeville, (mandevilleplayer.value, mandevilleplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayerradcliffe = """UPDATE "sports_day_times"
                                SET "player_radcliffe" = %s,
                                    "player_radcliffe_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerradcliffe, (radcliffeplayer.value, radcliffeplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayerruskin = """UPDATE "sports_day_times"
                                SET "player_ruskin" = %s,
                                    "player_ruskin_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerruskin, (ruskinplayer.value, ruskinplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayerwoodcote = """UPDATE "sports_day_times"
                                SET "player_woodcote" = %s,
                                    "player_woodcote_time" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerwoodcote, (woodcoteplayer.value, woodcoteplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                if distancebool == True:
                    updateplayerbridges = """UPDATE "sports_day_distances"
                                SET "player_bridges" = %s,
                                    "player_bridges_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerbridges, (bridgesplayer.value, bridgesplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayercarew = """UPDATE "sports_day_distances"
                                SET "player_carew" = %s,
                                    "player_carew_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayercarew, (carewplayer.value, carewplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayermandeville = """UPDATE "sports_day_distances"
                                SET "player_mandeville" = %s,
                                    "player_mandeville_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayermandeville, (mandevilleplayer.value, mandevilleplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayerradcliffe = """UPDATE "sports_day_distances"
                                SET "player_radcliffe" = %s,
                                    "player_radcliffe_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerradcliffe, (radcliffeplayer.value, radcliffeplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayerruskin = """UPDATE "sports_day_distances"
                                SET "player_ruskin" = %s,
                                    "player_ruskin_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerruskin, (ruskinplayer.value, ruskinplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                    updateplayerwoodcote = """UPDATE "sports_day_distances"
                                SET "player_woodcote" = %s,
                                    "player_woodcote_distance" = %s
                                WHERE "event" = %s; """
                    cursor.execute(updateplayerwoodcote, (woodcoteplayer.value, woodcoteplayertime.value, (page.session.get("event") or "")))
                    connection.commit()
                def split(event):
                    events = ["100m", "200m", "300m","400m", "800m", "1500m", "Discus", "Shotput", "Long Jump", "High Jump", "Javelin", "Triple Jump", "200m Relay", "Relay"]
                    ageCat = ["Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Senior", "Girls"]
                    eventName = ""
                    ageCategory = ""
                    for i in range(0, len(events)):
                        if events[i] in event:
                            eventName = events[i]
                    for i in range(0,len(ageCat)):
                        if ageCat[i] in event:
                            ageCategory = ageCat[i]
                    return eventName, ageCategory
                if "Tug of War" not in (page.session.get("event") or ""):
                    splittedEvent = split((page.session.get("event") or ""))
                    event_name = splittedEvent[0]
                    age_category = splittedEvent[1]
                    times = [bridgesplayer.value, timeToSeconds(bridgesplayertime.value), carewplayer.value, timeToSeconds(carewplayertime.value), mandevilleplayer.value, timeToSeconds(mandevilleplayertime.value), radcliffeplayer.value, timeToSeconds(radcliffeplayertime.value), ruskinplayer.value, timeToSeconds(ruskinplayertime.value), woodcoteplayer.value, timeToSeconds(woodcoteplayertime.value)]
                    sortedtimes = bubbleSort(times)
                    if timebool == True:
                        recordcheck = sortedtimes[len(sortedtimes)-1]
                        recordcheckplayer = sortedtimes[len(sortedtimes)-2]
                    if distancebool == True:
                        recordcheck = sortedtimes[1]
                        recordcheckplayer = sortedtimes[0]
                    ageCategories = ["Year 7", "Year 8", "Year 9", "Year 10", "Senior", "Girls"]
                    columnEquivalentsTime = ["year7time", "year8time", "year9time", "year10time", "seniortime", "girlstime"]
                    columnEquivalentsDate = ["year7date", "year8date", "year9date", "year10date", "seniordate", "girlsdate"]
                    columnEquivalentsPlayer = ["year7player", "year8player", "year9player", "year10player", "seniorplayer", "girlsplayer"]
                    columnTime = ""
                    columnDate = ""
                    columnTime = ""
                    for i in range (0, len(ageCategories)):
                        if ageCategories[i] == age_category:
                            columnTime = columnEquivalentsTime[i]
                            columnDate = columnEquivalentsDate[i]
                            columnPlayer = columnEquivalentsPlayer[i]
                    if age_category == "Year 11":
                            columnTime = "seniortime"
                            columnDate = "seniordate"
                            columnPlayer = "seniorplayer"
                            if columnTime == "":
                                leaderboardpage(e)
                                return
                    select = f"""SELECT {columnTime} FROM "school_records"
                                    WHERE "event" = %s; """
                    cursor.execute(select, (event_name,))
                    currentrecord = cursor.fetchone()
                    print(currentrecord)
                    if currentrecord is None:
                        leaderboardpage(e)
                        return
                    currentrecord = timeToSeconds(currentrecord[0])
                    recordchecktime = date.today().year
                    if timebool == True:
                        if recordcheck < currentrecord:
                            updateTimeRecord = f"""UPDATE "school_records"
                                                  SET  {columnPlayer} = %s,
                                                       {columnDate} = %s,
                                                       {columnTime} = %s
                                                  WHERE event = %s;  """
                            cursor.execute(updateTimeRecord, (recordcheckplayer, recordchecktime, secondsToDisplay(recordcheck), event_name))
                            connection.commit()
                    if distancebool == True:
                        if recordcheck > currentrecord:
                            updateDistanceRecord = f"""UPDATE "school_records"
                                                  SET  {columnPlayer} = %s,
                                                       {columnDate} = %s,
                                                       {columnTime} = %s
                                                  WHERE event = %s;  """
                            cursor.execute(updateDistanceRecord, (recordcheckplayer, recordchecktime,recordcheck, event_name))
                            connection.commit()
                leaderboardpage(e)
            def searchFunction(e): 
                value = searchbar.value
                index = -1
                page.session.set("event", "")
                for i in range (0,len(optionsCleaned)):
                    current = optionsCleaned[i]
                    if value.lower() in current.lower():
                        index = i
                    if index != -1:
                        page.session.set("event", optionsCleaned[index])
                    else:
                        page.session.set("event", "")
                if index == -1:
                    invalid.visible = True
                    Event.visible = False
                    page.update()
                else:
                    Event.value = "You have selected event: " + (page.session.get("event") or "")
                    Event.visible = True
                    invalid.visible = False
                    page.update()
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
            searchbar = flet.TextField(
                label = "Search for event ...",
            )
            page.add(searchbar)
            submit = flet.ElevatedButton(text = "Submit", width = 200, height = 50, on_click = searchFunction)
            invalid = flet.Text("Invalid event try again", visible = False, color = "Red")
            page.add(invalid)
            Event = flet.Text("You have selected event: ", visible = False, color = "Green")
            page.add(Event)
            page.add(submit)
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
            submit = flet.ElevatedButton(text = "Submit results!", width = 300, height = 100, on_click = dropdown)
            page.add(submit)
        searchBar(optionsCleaned)
        presenceMessage0 = flet.Text("Please make sure to select an event!", color = "red", visible = False)
        page.add(presenceMessage0)
        presenceMessage1 = flet.Text("Please make sure each House is allocated a position via the dropdowns!", color = "red", visible = False)
        page.add(presenceMessage1)
        presenceMessage2 = flet.Text("Please make sure each House's representative's name and time/distance are entered!", color = "red", visible = False)
        page.add(presenceMessage2)
        colonmessage = flet.Text("For the 800m, 1500m and Relay events enter the time as min:secs like 1:08 and for all other events keep the time in seconds!", color = "red", visible = False)
        page.add(colonmessage)
        BACKBUTTON1 = backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = EEBclicked)
        page.add(BACKBUTTON1)
    def houseEventsButtonClicked(e):
        page.controls.clear()
        page.session.set("event", "")
        page.scroll = flet.ScrollMode.AUTO
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = EEBclicked) # Creates a button that allows user to go back to the previous page
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        select = """ SELECT house_event FROM house_event_list ; """
        cursor.execute(select)
        fetch = cursor.fetchall()
        options = fetch
        optionsCleaned = []
        for i in range(0, len(options)):
            optionsCleaned.append(options[i][0])
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.theme_mode= flet.ThemeMode.DARK
        page.add(flet.Text(value = "Enter Event results", color = "Red", size = 50))
        def searchBar(optionsCleaned):
            def dropdown(e):
                bpos = bridgesdd.value
                cpos = carewdd.value
                mpos = mandevilledd.value
                rapos = radcliffedd.value
                rupos = ruskindd.value
                wpos = woodcotedd.value
                rank = [bpos, cpos, mpos, rapos, rupos, wpos]
                if None in rank:
                    presenceMessage.visible = True
                    page.update()
                    return
                if searchbar.value == "":
                    presenceMessage.visible = True
                    page.update()
                    return
                point = []
                weightedEvents = ["House Music", "House Drama"]
                if weightedEvents[0] not in (page.session.get("event") or "") and weightedEvents[1] not in (page.session.get("event") or ""):
                    for i in range(0, len(rank)):
                        point.append(7 - int(rank[i]))
                    insertBridges = """UPDATE "bridges_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s;"""
                    cursor.execute(insertBridges,(point[0],(page.session.get("event") or "")))
                    connection.commit()
                    insertCarew = """UPDATE "carew_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertCarew,(point[1],(page.session.get("event") or "")))
                    connection.commit()
                    insertMandeville = """UPDATE "mandeville_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertMandeville,(point[2],(page.session.get("event") or "")))
                    connection.commit()
                    insertRadcliffe = """UPDATE "radcliffe_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRadcliffe,(point[3],(page.session.get("event") or "")))
                    connection.commit()
                    insertRuskin = """UPDATE "ruskin_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRuskin,(point[4],(page.session.get("event") or "")))
                    connection.commit()
                    insertWoodcote = """UPDATE "woodcote_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertWoodcote,(point[5],(page.session.get("event") or "")))
                    connection.commit()
                else:
                    weightedrank = ["1", "2", "3", "4", "5", "6"]
                    weightedpoints = ["9", "7", "5", "3", "2", "1"]
                    for i in range (0, len(weightedrank)):
                        for j in range(0, 6):
                            if rank[i] == weightedrank[j]:
                                point.append(weightedpoints[j])                        
                    insertBridges = """UPDATE "bridges_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s;"""
                    cursor.execute(insertBridges,(point[0],(page.session.get("event") or "")))
                    connection.commit()
                    insertCarew = """UPDATE "carew_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertCarew,(point[1],(page.session.get("event") or "")))
                    connection.commit()
                    insertMandeville = """UPDATE "mandeville_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertMandeville,(point[2],(page.session.get("event") or "")))
                    connection.commit()
                    insertRadcliffe = """UPDATE "radcliffe_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRadcliffe,(point[3],(page.session.get("event") or "")))
                    connection.commit()
                    insertRuskin = """UPDATE "ruskin_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertRuskin,(point[4],(page.session.get("event") or "")))
                    connection.commit()
                    insertWoodcote = """UPDATE "woodcote_events"
                                        SET "points" = %s 
                                        WHERE "event" = %s; """
                    cursor.execute(insertWoodcote,(point[5],(page.session.get("event") or "")))
                    connection.commit()
                leaderboardpage(e)
            def searchFunction(e): 
                value = searchbar.value
                index = -1
                page.session.set("event", "")
                for i in range (0,len(optionsCleaned)):
                    current = optionsCleaned[i]
                    if value.lower() in current.lower():
                        index = i
                    if index != -1:
                        page.session.set("event", optionsCleaned[index])
                    else:
                        page.session.set("event", "")
                if index == -1:
                    invalid.visible = True
                    Event.visible = False
                    page.update()
                else:
                    Event.value = "You have selected event: " + (page.session.get("event") or "")
                    Event.visible = True
                    invalid.visible = False
                    page.update()
            
            instruction1 = flet.Text(value = "This is the event entry form which you can use to record the results of events.", color = "Green", size = 20)
            instruction2 = flet.Text(value = "1. Type in the event you would like to record a result for and press submit, to select a different event simply re-type and submit again!", color = "Green", size = 20)
            instruction3 = flet.Text(value = "2. Select the position of the houses via the dropdown form, if there was a tie simply allocate the same position!", color = "Green", size = 20)
            page.add(instruction1)
            page.add(instruction2)
            page.add(instruction3)
            searchbar = flet.TextField(
                label = "Search for event ...",
            )
            page.add(searchbar)
            submit = flet.ElevatedButton(text = "Submit", width = 200, height = 50, on_click = searchFunction)
            page.add(submit)
            invalid = flet.Text("Invalid event try again", visible = False, color = "Red")
            page.add(invalid)
            Event = flet.Text("You have selected event: ", visible = False, color = "Green")
            page.add(Event)
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
            submit = flet.ElevatedButton(text = "Submit results!", width = 300, height = 100, on_click = dropdown)
            page.add(submit)
            presenceMessage = flet.Text("Please make sure all details are provided by filling all the boxes!", color = "red", visible = False)
            page.add(presenceMessage)
            successText = flet.Text("Results sucessfully submitted!", color = "green", visible = False)
            page.add(successText)
            BACKBUTTON = backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = EEBclicked)
            page.add(BACKBUTTON)
            page.update()
        searchBar(optionsCleaned)
    def individualResetButtonClicked(e):
        page.controls.clear()
        page.update()
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        page.add(flet.Text(value = "Search for the event for which you would like to erase the result of!", color = "Blue", size = 50))
        searchbar = flet.TextField(
                label = "Search for event ...",
            )
        page.add(searchbar)
        def submitButtonClicked(e):
            selectnormalevents = """SELECT * FROM "house_event_list"; """
            cursor.execute(selectnormalevents)
            listnormal = cursor.fetchall()
            selectsportsdayevents = """SELECT "event" FROM "sports_day_events";  """
            cursor.execute(selectsportsdayevents)
            listsportsday = cursor.fetchall()
            eventList = []
            for i in range(0, len(listnormal)):
                eventList.append(listnormal[i][0])
            for i in range(0, len(listsportsday)):
                eventList.append(listsportsday[i][0])
            input = searchbar.value
            index = -1
            event = ""
            for i in range (0,len(eventList)):
                current = eventList[i]
                if input.lower() in current.lower():
                    index = i
                if index != -1:
                    event = eventList[index]
                else:
                    event = ""
            page.session.set("index", index)
            page.session.set("event", event)
            if index == -1:
                invalid.visible = True
                Event.visible = False
                clearButton.visible = False
                page.update()
            else:
                Event.value = "You have selected event: " + event
                Event.visible = True
                invalid.visible = False
                clearButton.visible = True
                page.update()
        def clearButtonClicked(e):
            if (page.session.get("index") if page.session.get("index") is not None else -1) < 39:
                erasebridges = """UPDATE "bridges_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasebridges, ((page.session.get("event") or ""),))
                connection.commit()
                erasecarew = """UPDATE "carew_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasecarew, ((page.session.get("event") or ""),))
                connection.commit()
                erasemandeville = """UPDATE "mandeville_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasemandeville, ((page.session.get("event") or ""),))
                connection.commit()
                eraseradcliffe = """UPDATE "radcliffe_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(eraseradcliffe, ((page.session.get("event") or ""),))
                connection.commit()
                eraseruskin = """UPDATE "ruskin_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(eraseruskin, ((page.session.get("event") or ""),))
                connection.commit()
                erasewoodcote = """UPDATE "woodcote_events" SET "points" = '0' WHERE event = %s; """
                cursor.execute(erasewoodcote, ((page.session.get("event") or ""),))
                connection.commit()
            if (page.session.get("index") if page.session.get("index") is not None else -1) > 38:
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
                if "Tug of War" not in (page.session.get("event") or ""):
                    timeEvents = ["100m", "200m", "300m", "400m", "800m", "1500m", "Relay"]
                    distanceEvents = ["Javelin", "Discus", "Shotput", "Long Jump", "Triple Jump", "High Jump"]
                    timebool = False
                    distancebool = False
                    for i in range(0,len(timeEvents)):
                        if timeEvents[i] in (page.session.get("event") or ""):
                            timebool = True
                    for i in range(0,len(distanceEvents)):
                        if distanceEvents[i] in (page.session.get("event") or ""):
                            distancebool = True
                    if timebool == True:
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
                    if distancebool == True:
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
            leaderboardpage(e)
        submitButton = flet.ElevatedButton(text = "Submit", width = 150, height = 75, on_click = submitButtonClicked)
        page.add(submitButton)
        invalid = flet.Text("Invalid event try again", visible = False, color = "Red")
        page.add(invalid)
        Event = flet.Text("You have selected event: ", visible = False, color = "Green")
        page.add(Event)
        clearButton = flet.ElevatedButton(text = "Clear Results", visible = False, width = 150, height = 75, color = "Red",on_click = clearButtonClicked)
        page.add(clearButton)
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = adminButtonClicked)
        page.add(backButton)
    def masterResetButtonClicked(e):
        page.controls.clear()
        page.update()
        page.theme_mode= flet.ThemeMode.DARK
        page.vertical_alignment = flet.MainAxisAlignment.CENTER
        page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        def yesButtonClicked(e):
            page.controls.clear()
            page.update()
            page.theme_mode= flet.ThemeMode.DARK
            page.vertical_alignment = flet.MainAxisAlignment.CENTER
            page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
            page.add(flet.Text(value = "All events have been reset successfully!", color = "green", size = 75))
            backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = adminButtonClicked)
            page.add(backButton)
            reset_bridges_events = """UPDATE "bridges_events"
                                        SET points = '0';  """
            reset_carew_events = """UPDATE "carew_events"
                                        SET points = '0';  """
            reset_mandeville_events = """UPDATE "mandeville_events"
                                        SET points = '0';  """
            reset_radcliffe_events = """UPDATE "radcliffe_events"
                                        SET points = '0';  """
            reset_ruskin_events = """UPDATE "ruskin_events"
                                        SET points = '0';  """
            reset_woodcote_events = """UPDATE "woodcote_events"
                                        SET points = '0';  """
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
            reset_sports_day_events = """UPDATE "sports_day_events"
                                            SET bridgespoints = 0,
                                              carewpoints = 0,
                                                mandevillepoints = 0,
                                                  radcliffepoints = 0,
                                                    ruskinpoints = 0,
                                                     woodcotepoints = 0; """
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
        instruction = flet.Text("Do you want to reset the results for every single event?")
        yesButton = flet.ElevatedButton(text = "Yes", color = "Green", width = 300, height = 100, on_click = yesButtonClicked)
        noButton = flet.ElevatedButton(text = "No", color = "Red", width = 300, height = 100, on_click = adminButtonClicked)
        page.add(instruction)
        page.add(flet.Row(
            controls = [yesButton, noButton],
            alignment=flet.MainAxisAlignment.CENTER
        ))
        backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = adminButtonClicked)
        page.add(backButton)
    def adminButtonClicked(e):
        def adminButtonClickedPostLogin():
            page.session.set("logged_in", True)
            page.controls.clear()
            page.update()
            page.theme_mode= flet.ThemeMode.DARK
            page.vertical_alignment = flet.MainAxisAlignment.CENTER
            page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
            masterResetButton = flet.ElevatedButton(text = "Master Reset", width = 300, height = 100, color = "red", on_click = masterResetButtonClicked)
            individualResetButton = flet.ElevatedButton(text = "Individual event reset", width = 300, height = 100, color = "red", on_click = individualResetButtonClicked)
            page.add(flet.Row(
                controls = [masterResetButton, individualResetButton],
                alignment=flet.MainAxisAlignment.CENTER
            ))
            backButton = flet.ElevatedButton(text = "←", color = "white", width = 50, height = 50, on_click = leaderboardpage)
            page.add(backButton)
        if page.session.get("logged_in") == True:
            adminButtonClickedPostLogin()
        else:
            page.controls.clear()
            page.update()
            login_page(page, on_success = adminButtonClickedPostLogin, on_back = leaderboardpage)
    def leaderboardpage(e):
        page.controls.clear()
        page.scroll = None
        page.theme_mode= flet.ThemeMode.DARK
        standingsButton = flet.ElevatedButton(text = "Cock House Cup standings", width = 275, height = 100, on_click = CHCSclicked)    # Creates a button
        individualButton = flet.ElevatedButton(text = "Individual event results", width = 275, height = 100, on_click = IERclicked)   # Creates a button 
        sportsdayButton = flet.ElevatedButton(text = "Sports day results", width = 275, height = 100, on_click = SDRclicked)          # Creates a button 
        eventEntryButton = flet.ElevatedButton(text = "Event Score Entry", width = 275, height = 100, on_click = EEBclicked)
        adminButton = flet.ElevatedButton(text = "Admin", width = 275, height = 100, color = "red", on_click = adminButtonClicked)
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
    leaderboardpage(page)

if __name__ == "__main__":
    flet.app(main)
