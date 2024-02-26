from dotenv import load_dotenv
import paramiko
import datetime
import os

load_dotenv()

def create_sftp_client(host, port, username, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)
    return client.open_sftp()

def download_files_for_month(sftp, year, month, remote_dir, local_dir):
    # Create a date range for the whole month
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month + 1, 1) if month < 12 else datetime.date(year + 1, 1, 1)
    bic = "BCIAIDJA"
    print("remoted dir", remote_dir)
    current_date = start_date
    while current_date < end_date:
        folder_name = current_date.strftime("%Y%m%d")
        remote_path = os.path.join(remote_dir,bic)
        print(remote_path)

        # try:
        #     # List files in the remote directory
        #     files = sftp.listdir(remote_path)
        #     for file in files:
        #         remote_file = os.path.join(remote_path, file)
        #         local_file = os.path.join(local_dir, file)
        #         sftp.get(remote_file, local_file)
        #         print(f"Downloaded {remote_file} to {local_file}")
        # except FileNotFoundError:
        #     print(f"No files found for date: {folder_name}")

        # Move to the next day
        current_date += datetime.timedelta(days=1)


def validate_input(input_value, field_name, min_length):
    if len(str(input_value)) < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters long.")



# SFTP server credentials
host = os.getenv("REP_HOST")
port = os.getenv("REP_PORT")  # default SFTP port
username = os.getenv("REP_USER")
password = os.getenv("REP_PASS")

# Remote and local directories
remote_dir = os.getenv("REP_PATH")
local_dir = os.getenv("LOCAL_PATH")

# Year and month you want to download files for


while True:
    try:
        # Get year
        year = int(input("Enter a year number (4 digits YYYY): "))
        validate_input(year, "year", 4)

        # Get month
        month = int(input("Enter a month number (2 digits MM): "))
        validate_input(month, "month", 2)

        # If both inputs are valid, break out of the loop
        break

    except ValueError as error:
        print(error)
        # Optionally, you can choose to re-prompt for all inputs or just the one that failed


print(year)
print(month)

sftp = create_sftp_client(host, port, username, password)
download_files_for_month(sftp, year, month, remote_dir, local_dir)
print(sftp)
sftp.close()
