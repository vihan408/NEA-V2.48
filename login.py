import os
import psycopg2
import flet
import time
from dotenv import load_dotenv

load_dotenv()

def login(page, on_success = None, on_back = None):
    connection = psycopg2.connect(database = os.getenv("dbName"),
                              host = os.getenv("dbHost"),
                              user = os.getenv("dbUser"),
                              password = os.getenv("dbPassword"),
                              port = os.getenv("dbPort"))

    cursor = connection.cursor()
    page.theme_mode= flet.ThemeMode.DARK
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    def createAccount(e):
        page.session.set("createAccountClicked", True)
        def registerAccount(e):
            insert = """INSERT INTO "userlogins" ("usernames", "userpassword") 
                        VALUES (%s, %s);"""
            if Keyword.value == os.getenv("signupkeyword") and Email.value != "" and Password.value != "":
                cursor.execute(insert, (Email.value,Password.value))
                connection.commit()
                accountSuccess = flet.Text(value = "Account created sucessfully return to Login and sign in!")
                page.add(accountSuccess)
                time.sleep(0.01)
                accountSuccess.visible = False
            elif Email.value == "" and Password.value == "" and Keyword.value == "":
                EmailandPasswordandKeywordError = flet.Text(value = "Please enter an email, password and keyword!", color = "red")
                page.add(EmailandPasswordandKeywordError)
                time.sleep(0.01)
                EmailandPasswordandKeywordError.visible = False
            elif Email.value == "" and Password.value == "":
                EmailandPasswordError = flet.Text(value = "Please enter an email and password!", color = "red")
                page.add(EmailandPasswordError)
                time.sleep(0.01)
                EmailandPasswordError.visible = False
            elif Email.value == "" and Password.value != "":
                EmailError = flet.Text(value = "Please enter an email!", color = "red")
                page.add(EmailError)
                time.sleep(0.01)
                EmailError.visible = False
            elif Email.value != "" and Password.value == "":
                PasswordError = flet.Text(value = "Please enter a password!", color = "red")
                page.add(PasswordError)
                time.sleep(0.01)
                PasswordError.visible = False
            elif Keyword.value == "":
                KeywordError = flet.Text(value = "Please enter a Keyword!", color = "red")
                page.add(KeywordError)
                time.sleep(0.01)
                KeywordError.visible = False
            else:
                keywordError = flet.Text(value = "Wrong keyword please try again!", color = "red")
                page.add(keywordError)
                time.sleep(0.01)
                keywordError.visible = False
        page.controls.clear()
        page.update()
        Email = flet.TextField(label = "Enter email", color = "red")
        Password = flet.TextField(label = "Enter password", color = "red")
        Keyword = flet.TextField(label = "Enter keyword", color = "red")
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
            page.controls.clear()
            page.update()
            login(page, on_success)
            page.session.set("createAccountClicked", False)
        elif email.value != "" and password.value != "":
            select = """ SELECT "usernames", "userpassword" FROM "userlogins" WHERE "usernames" = %s AND "userpassword" = %s; """
            cursor.execute(select,(email.value,password.value))
            result = cursor.fetchone()
            if result != None:
                page.add(flet.Text(value = "Login Successful", color = "green"))
                if on_success:
                    on_success()
            else:
                wrongDetailsError = flet.Text(value = "Login Unsuccessful, please check your credentials again", color = "red")
                page.add(wrongDetailsError)
                time.sleep(0.01)
                wrongDetailsError.visible = False
        else:
            if email.value == "" and password.value == "":
                emailandpassworderror = flet.Text(value = "Please enter an email and password!",color = "red")
                page.add(emailandpassworderror)
                time.sleep(0.01)
                emailandpassworderror.visible = False
            if email.value == "" and password.value != "":
                emailError = flet.Text(value = "Please enter an email!",color = "red")
                page.add(emailError)
                time.sleep(0.01)
                emailError.visible = False
            if email.value != "" and password.value == "":
                passwordError = flet.Text(value = "Please enter a password!",color = "red")
                page.add(passwordError)
                time.sleep(0.01)
                passwordError.visible = False
                

    email = flet.TextField(label = "Enter email", color = "red")
    password = flet.TextField(label = "Enter password", color = "red")
    loginButton = flet.ElevatedButton(text = "Login", on_click = Login)
    createAccountButton = flet.ElevatedButton(text = "Create Account", on_click = createAccount)
    page.add(
        flet.Column(controls = [
            email,
            password,
            flet.Row(controls = [
                loginButton,
                createAccountButton,
                flet.ElevatedButton(text = "←", width = 50, height = 50, on_click = on_back)
            ])
        ])
    )

if __name__ == "__main__":
    flet.app(login)