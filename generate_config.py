
import configparser

config_file = configparser.ConfigParser()
config_file.add_section("SMTPlogin")

# Add settings to section
# Here you need to modify the values of last parameter of set function

config_file.set("SMTPlogin", "sender_address", "n19dcat045@student.ptithcm.edu.vn")
config_file.set("SMTPlogin", "receiver_address", "fcvtieulongg12@gmail.com")
config_file.set("SMTPlogin", "mailtrap_user", "d0aee913bd3afb")
config_file.set("SMTPlogin", "mailtrap_password", "23845b8edb6bb3")
# Saving config file as configurations.ini
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")
