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

def download_files_for_month(sftp, year, month, remote_dir, local_dir, bic ,type_report):
    # Create a date range for the whole month
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month + 1, 1) if month < 12 else datetime.date(year + 1, 1, 1)
   
    print("remoted dir", remote_dir)
    print("type report  : " + type_report)

    current_date = start_date
    while current_date < end_date:
        folder_name = current_date.strftime("%d%m%Y")
        remote_path = remote_dir +  bic + "/"+ folder_name 
        print(remote_path)

#/opt/aci/ciportal/GeneratedReport/Reports/BICNIDJA/02032024/
        try:
            # List files in the remote directory
            files = sftp.listdir(remote_path)
            for file in files:
                if file.startswith(type_report):
                    remote_file = f"{remote_path}/{file}"
                    # print("remote file  :", remote_file)

                    local_specific_dir = local_dir + type_report + "\\" + bic + "\\" +str(current_date.strftime("%Y")) + "\\" + str(current_date.strftime("%B") + "\\" + str(current_date.strftime("%d")) )
                  
                    # Check if the local directory exists, and create it if it doesn't
                    if not os.path.exists(local_specific_dir):
                        os.makedirs(local_specific_dir)
                        print(f"Created local directory: {local_specific_dir}")

                    local_file = local_specific_dir + "\\" + file
                    sftp.get(remote_file, local_file)
                    print(f"Downloaded {remote_file} to {local_file}")
        except FileNotFoundError:
            print(f"No files found for date: {remote_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        #Move to the next day
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
        validate_input(month, "month", 1)

        # If both inputs are valid, break out of the loop
        break

    except ValueError as error:
        print(error)
        # Optionally, you can choose to re-prompt for all inputs or just the one that failed


print(year)
print(month)

banks = ["BNIAIDJA", "BNINIDJA", "BRINIDJA", "BSDRIDJA", "BSMDIDJA", "BTANIDJA", "CENAIDJA", "CITIIDJX", "DBSBIDJA", "FASTIDJA", "MEGAIDJA", "NISPIDJA", "BBBAIDJA", "BBIJIDJA", "BDINIDJA", "BMRIIDJA", "SBJKIDJA", "SYNAIDJ1", "SYBBIDJ1", "SYBDIDJ1", "SYBTIDJ1", "SYCAIDJ1", "SYJGIDJ1", "SYJTIDJ1", "SYTBIDJ1", "ABALIDBS", "SIHBIDJ1", "BMSEIDJA", "BDIPIDJ1", "PDIJIDJ1", "PDJBIDJA", "PDJGIDJ1", "PDJTIDJ1", "PDNTIDJA", "PINBIDJA", "BBLUIDJA", "GNESIDJA", "HNBNIDJA", "HRDAIDJ1", "HSBCIDJA", "IAPTIDJA", "KSEIIDJ1", "LFIBIDJ1", "MASDIDJ1", "MEDHIDS1", "NANOIDJ1", "SYJBIDJ1", "BDKIIDJ1", "SYDKIDJ1", "ARTGIDJA", "AGTBIDJA", "ATOSIDJ1", "BBAIIDJA", "PDRIIDJA", "BCIAIDJA", "INDOIDJA", "BSSPIDSP", "BUMIIDJA", "CTCBIDJA", "IBBKIDJA", "ICBKIDJA", "JSABIDJ1", "SSPIIDJA", "MAYAIDJA", "MAYOIDJA", "MUABIDJA", "PDKBIDJ1", "PDKSIDJ1", "PDSBIDJ1", "PDYKIDJ1", "BIDXIDJA", "SUNIIDJA", "SYATIDJ1", "SYBKIDJ1", "SYKBIDJ1", "SYKSIDJ1", "SYSBIDJ1", "SYSSIDJ1", "SYYKIDJ1", "YUDBIDJ1", "AWANIDJA", "BKCHIDJA", "BOFAID2X", "BOTKIDJX", "BPIAIDJA", "BUTGIDJ1", "IBKOIDJA", "MCORIDJA", "NETBIDJA", "PDBBIDJ1", "PDBKIDJ1", "PDJMIDJ1", "PDKGIDJ1", "PDKTIDJ1", "PDMLIDJ1", "PDNBIDJ1", "PDSUIDJ1", "PDWRIDJ1", "PDWSIDJA", "PDWUIDJ1", "PUBAIDJ1", "SCBLIDJX", "SYACIDJ1", "SYJMIDJ1", "SYKTIDJ1", "SYONIDJ1", "SYSUIDJ1", "SYWSIDJ1", "VICTIDJ1", "ANZBIDJX", "APIDIDJ1", "ARFAIDJ1", "BBUKIDJA", "BICNIDJA", "BNPAIDJA", "CHASIDJX", "CICTIDJA", "DANAIDJ1", "LMANIDJ1", "PDWGIDJ1", "PDLPIDJ1", "SDOBIDJ1", "MHCCIDJA", "LOMAIDJ1", "MEEKIDJ1", "DEUTIDJA"]


sftp = create_sftp_client(host, port, username, password)
print(sftp)

for bic in banks:
    try:
        download_files_for_month(sftp, year, month, remote_dir, local_dir,bic, "RejectedCreditTransfer")
    except ValueError as error:
        print(error)



sftp.close()


# RejectedCreditTransfer
# CreditTransferRecapitulation