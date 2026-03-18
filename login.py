import os
import psycopg2
import flet
import time
from dotenv import load_dotenv
# This will import all of the libraries that will be used in the solution. This is neccessary for creating the GUI via flet, connecting and talking to my database via psycopg2 and using os and dotenv to load and use the credentials(allows me to connect to my database) to my database as well as the keyword for my login system.

load_dotenv()

def login(page, on_success = None, on_back = None):
    connection = psycopg2.connect(database = os.getenv("dbName"),
                              host = os.getenv("dbHost"),
                              user = os.getenv("dbUser"),
                              password = os.getenv("dbPassword"),
                              port = os.getenv("dbPort"))
# This establishes a connection to my database using the credentials stored in my dot env. (They have been stored in my dot env so that my real credentials cannot be found in the source code maintaining security)
    cursor = connection.cursor()
    # cursor will be used to execute queries on the database.
    page.theme_mode= flet.ThemeMode.DARK
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    def createAccount(e):
        #This function is called when the user decides to create an account. 
        page.session.set("createAccountClicked", True)
        # This is used so that I can recognise in the system that the user has decided to create an account and hence should be led to this page.
        def registerAccount(e):
            insert = """INSERT INTO "userlogins" ("usernames", "userpassword") 
                        VALUES (%s, %s);"""
            #SQL query that inserts the username and password specified by the user into the table userlogins inside my database.
            if Keyword.value == os.getenv("signupkeyword") and Email.value != "" and Password.value != "":
                #This actually excutes the insert query
                cursor.execute(insert, (Email.value,Password.value))
                connection.commit()
                accountSuccess = flet.Text(value = "Account created sucessfully return to Login and sign in!")
                page.add(accountSuccess)
                # Adds the accountSuccess message onto the screen letting the user know they have successfully created and registered the account.
                time.sleep(0.01)
                accountSuccess.visible = False
            elif Email.value == "" and Password.value == "" and Keyword.value == "":
                # When all 3 input boxes have been left blank by the user an error message, as part of the presence check validation method, must be displayed.
                EmailandPasswordandKeywordError = flet.Text(value = "Please enter an email, password and keyword!", color = "red")
                page.add(EmailandPasswordandKeywordError)
                time.sleep(0.01)
                EmailandPasswordandKeywordError.visible = False
            elif Email.value == "" and Password.value == "":
                # Another presence check prompting the user to enter an email and password
                EmailandPasswordError = flet.Text(value = "Please enter an email and password!", color = "red")
                page.add(EmailandPasswordError)
                time.sleep(0.01)
                EmailandPasswordError.visible = False
            elif Email.value == "" and Password.value != "":
                # Another presence check prompting the user to enter an email
                EmailError = flet.Text(value = "Please enter an email!", color = "red")
                page.add(EmailError)
                time.sleep(0.01)
                EmailError.visible = False
            elif Email.value != "" and Password.value == "":
                # Another presence check prompting the user to enter a password
                PasswordError = flet.Text(value = "Please enter a password!", color = "red")
                page.add(PasswordError)
                time.sleep(0.01)
                PasswordError.visible = False
            elif Keyword.value == "":
                # Another presence check prompting the user to enter a keyword
                KeywordError = flet.Text(value = "Please enter a Keyword!", color = "red")
                page.add(KeywordError)
                time.sleep(0.01)
                KeywordError.visible = False
            else:
                # This is now an authentication check that verifies if the keyword input by the user was correct or not, if not then the user is prompted to try again.
                keywordError = flet.Text(value = "Wrong keyword please try again!", color = "red")
                page.add(keywordError)
                time.sleep(0.01)
                keywordError.visible = False
        
        #This clears the page
        page.controls.clear()
        page.update()
        # This creates 3 textboxes where the user can input the relevant details
        Email = flet.TextField(label = "Enter email", color = "red")
        Password = flet.TextField(label = "Enter password", color = "red")
        Keyword = flet.TextField(label = "Enter keyword", color = "red")
        # This adds the 3 textboxes onto the page so that the user can actually input into the system
        page.add(
            Email,
            Password,
            Keyword,
            flet.Row(controls = [
                flet.ElevatedButton(text = "Create Account", on_click = registerAccount),
                flet.ElevatedButton(text = "Back to login", on_click = Login)
            ])
        )
    def Login(e):
        if page.session.get("createAccountClicked") == True:
            # This is the case when the user has just created an account and now returned to the login page. Calling login normally will cause an error since you would be adding the textboxes onto the page again. Instead the page must be cleared first then login can be called normally.
            page.controls.clear()
            page.update()
            login(page, on_success)
            page.session.set("createAccountClicked", False)
        elif email.value != "" and password.value != "":
            # When an email and password have both been entered then the username and password are searched for and retrieved from the database.
            select = """ SELECT "usernames", "userpassword" FROM "userlogins" WHERE "usernames" = %s AND "userpassword" = %s; """
            cursor.execute(select,(email.value,password.value))
            result = cursor.fetchone()
            # If nothing is fetched from the database the result will have value none. If and when nothing is fetched, this would indicate that there were no matches for the username and password combination. Therefore using the same logic if something is retrieved then
            # that means there was a successful match and hence the user has entered the correct details and hence should be able to login successfully.
            if result != None:
                page.add(flet.Text(value = "Login Successful", color = "green"))
                if on_success:
                    on_success()
            else:
                # in the event that the result is not not none or in other words none then there was no successful match and this is relayed to the user via the following message
                wrongDetailsError = flet.Text(value = "Login Unsuccessful, please check your credentials again", color = "red")
                page.add(wrongDetailsError)
                time.sleep(0.01)
                wrongDetailsError.visible = False
        else:
            if email.value == "" and password.value == "":
                # Presence check to make sure that the user enters an email and password
                emailandpassworderror = flet.Text(value = "Please enter an email and password!",color = "red")
                page.add(emailandpassworderror)
                time.sleep(0.01)
                emailandpassworderror.visible = False
            if email.value == "" and password.value != "":
                # Presence check to make sure that the user enters an email
                emailError = flet.Text(value = "Please enter an email!",color = "red")
                page.add(emailError)
                time.sleep(0.01)
                emailError.visible = False
            if email.value != "" and password.value == "":
                # Presence check to make sure that the user enters a password
                passwordError = flet.Text(value = "Please enter a password!",color = "red")
                page.add(passwordError)
                time.sleep(0.01)
                passwordError.visible = False
                
    # creates the 2 textboxes in which the user can enter the username and password
    email = flet.TextField(label = "Enter email", color = "red")
    password = flet.TextField(label = "Enter password", color = "red")
    # Creates a button that when clicked will "log" the user in by calling the login function to make sure the user's details are correct.
    loginButton = flet.ElevatedButton(text = "Login", on_click = Login)
    # Creates a button that when clicked will lead the user to another page where the user will be able to create an account.
    createAccountButton = flet.ElevatedButton(text = "Create Account", on_click = createAccount)
    # Add these textboxes and buttons onto the page so that the user can interact with them.
    page.add(
        flet.Column(controls = [
            email,
            password,
            flet.Row(controls = [
                loginButton,
                createAccountButton,
                # Adds a button that when clicked will take the user back to the homepage or leaderboardpage as the function is called.
                flet.ElevatedButton(text = "←", width = 50, height = 50, on_click = on_back)
            ])
        ])
    )

if __name__ == "__main__":
    flet.app(login)
