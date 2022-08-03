import re
import json



def check_id_in_file(ui_emailid):

    try:
        with open('emailid_database.json', 'r+') as file:
            
            try:
                file_data = json.load(file)
                if ui_emailid in file_data:
                    return True
                else:
                    return False
            except json.decoder.JSONDecodeError:
                return 'no_data'
    except FileNotFoundError:
        filecreation = open('emailid_database.json', 'a')
        filecreation.close()
        return check_id_in_file(ui_emailid)

#Update the data in exiting file 


def update_data(new_data=None, key=None, filename='emailid_database.json'):


    with open(filename, 'r+') as file:
    
        if new_data is not None:
            try:
                file_data = json.load(file)
                file_data.update(new_data)
                file.seek(0)
                json.dump(file_data, file)
      
            except json.decoder.JSONDecodeError:
                with open('emailid_database.json', 'a') as file2:
                    json.dump(new_data, file2)
       
        if key is not None:
            file_data = json.load(file)
            file_data[key] = check_passwordformat(input('Enter new password : '))
            file.seek(0)
            json.dump(file_data, file)

#step1:- validation of email

def check_emailidformat(mailid):

    regex = r'[A-Za-z].+@[A-Za-z0-9-]+\.[A-Za-z]+'
    regex1 = r'[A-Za-z]+@[A-Za-z0-9-]+\.[A-Za-z]+'
    if re.fullmatch(regex, mailid):
        return mailid
    elif re.fullmatch(regex1, mailid):
        return mailid
    else:
        print("Invalid Email")
        check_emailidformat(input('Re-enter emailid : '))

#step2:- Validation of Password

def check_passwordformat(password):


    chars = set(string.punctuation)
    if 5 < len(password) <= 16: 
        if any(i in chars for i in password):
            if bool(re.search(r'\d', password)):
                if bool(re.search(r'[A-Z]', password)): 
                    if bool(re.search(r'[a-z]', password)): 
                        return password
                else:
                    print('password should contain atleast one small and capital letter')
                    return check_passwordformat(input('Re enter password : '))
            else:
                print('password should contain atleast one number')
                return check_passwordformat(input('Re enter password : '))
        else:
            print('password should contain atleast one special character')
            return check_passwordformat(input('Re enter password : '))
    else:
        print('length should be more than 16')
        return check_passwordformat(input('Re enter password : '))

# If user forget password 

def forgot_password_option(ui_mailid):

    with open('emailid_database.json', 'r+') as file:
        file_data = json.load(file)
    print('Enter 1 to retrive password\nEnter 2 to update password')
    options3 = input()
    if options3 == '1':  
        print(f'registered password : {file_data[ui_mailid]}')
    if options3 == '2':  
        update_data(key=ui_mailid)

#step3:- Login 

def password_login(ui_mailid):

    print('Enter 1 to Enter password\nEnter 2 if forgot password')
    options2 = input()

    with open('emailid_database.json', 'r+') as file:
        file_data = json.load(file)

    if options2 == '1':  
        ui_password2 = input('Enter password : ')
        if ui_password2 == file_data[ui_mailid]:
            print('login successfull')
        else:
            print('incorrect password')
            password_login(ui_mailid)

    if options2 == '2':  # forgot password
        forgot_password_option(ui_mailid)

#step4:- Registration option  

def registration():

    # email part
    ui_mailid = check_emailidformat(input('Enter email id : '))
    id_exists = check_id_in_file(ui_mailid)
    if id_exists == True:
        print('Entered emailid already exists\nEnter 1 for re-enter emailid \nEnter 2 for login')
        input1 = input()
        if input1 == '1':
            return registration()
        if input1 == '2':
            return login()
  
    ui_password = check_passwordformat(input('Enter password : '))
    new_data = {ui_mailid: ui_password}
    update_data(new_data=new_data)
    print('registration successful')
    start_program()

#step5:- Login option

def login():

    ui_mailid = check_emailidformat(input('Enter email id : '))
    id_exists = check_id_in_file(ui_mailid)
    if id_exists == 'no_data':
        print('no data found  in the database\nDirecting to registration')
        return registration()
    if id_exists == False:
        print('Entered emailid doesn\'t exists\nEnter 1 for re-enter emailid \nEnter 2 for registration')
        print('')
        input1 = input()
        if input1 == '1':
            return login()
        if input1 == '2':
            return registration()
    password_login(ui_mailid)
    start_program()

#step6:- creation of program to choose the registration or login option 

def start_program():
   
    print('\nEnter 1 for registration\nEnter 2 for login\nEnter 0 to exit ')
    user_input1 = input()
    if user_input1 == '1':
        registration()
    if user_input1 == '2':
        login()
    if user_input1 == '0':
        exit()

start_program()