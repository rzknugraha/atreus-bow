from dotenv import load_dotenv
import shutil
import datetime
import os
import sys
import time
import subprocess


load_dotenv()



def move_files( year, month, target_path, source_path, type_report,bic,index_bic,total_bic):
    # Create a date range for the whole month
    index_bic += 1
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month + 1, 1) if month < 12 else datetime.date(year + 1, 1, 1)
   
    print("target_path dir", target_path)
    print("type report  : " + type_report)

    current_date = start_date
    while current_date < end_date:
        source_files = source_path + type_report + "\\" + bic + "\\" +str(current_date.strftime("%Y")) + "\\" + str(current_date.strftime("%B") + "\\" + str(current_date.strftime("%d")) )
        print(source_files)

# source
# D:\Document\Bank Indonesia\Operasional BIFAST - Documents\PORTAL REPORTS BACKUP\RejectedCreditTransfer\AGTBIDJA\2024\August\01

#/opt/aci/ciportal/GeneratedReport/Reports/BICNIDJA/02032024/
        try:

            # Ensure the destination folder exists
            os.makedirs(source_path, exist_ok=True)

            # Get a list of all files in the source folder
            files_to_move = [f for f in os.listdir(source_files)]
                             
            # Total number of files to move
            total_files = len(files_to_move)
            print(f"Total Files in {current_date.strftime("%d")} {current_date.strftime("%B")} {current_date.strftime("%Y")} for {bic}  {index_bic}/{total_bic} : {total_files} Files")

            # List files in the remote directory
            files = os.listdir(source_files)
            index = 0
            for file in files:
                    # else:
                if file.startswith(type_report): 
                    source = f"{source_files}/{file}"
                    # print(f"Get source file :  {source}")
                    
                    target_specific_dir = target_path + type_report + "\\" +str(current_date.strftime("%Y")) + "\\" + str(current_date.strftime("%B") + "\\" + str(current_date.strftime("%d")) ) + "\\" +  bic 
                  
                    # Check if the local directory exists, and create it if it doesn't
                    if not os.path.exists(target_specific_dir):
                        os.makedirs(target_specific_dir)
                        # print(f"Created local directory: {target_specific_dir}")

                    local_file = target_specific_dir + "\\" + file
                    # Check if it's a file (not a directory)
                    if os.path.isfile(source):

                        # process = subprocess.Popen(['python', '-c', f"import shutil; shutil.move('{source}', '{local_file}')"])
                        # time_limit_s = 10
                        # try:
                        #     process.wait(timeout=time_limit_s)
                        #     if process.returncode != 0:
                        #         print(f"Failed to copy {source} to {local_file}.")
                        # except subprocess.TimeoutExpired:
                        #     process.kill()
                        #     print(f"Timeout! The copy operation for {source} exceeded {time_limit_s} seconds and was terminated.")


                        shutil.move(source, local_file)
                        # print(f"SuccessMoved {source} to {local_file}")
                    else:
                        print(f"Failed Copied {source} to {local_file}")
                    
                    index += 1
                    print_progress_bar(index, total_files)
        except FileNotFoundError:
            print(f"No files found in remote for date: {source_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        #Move to the next day
        current_date += datetime.timedelta(days=1)

        


def validate_input(input_value, field_name, min_length):
    if len(str(input_value)) < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters long.")

# Function to print a simple progress bar
def print_progress_bar(iteration, total, length=40):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent}% Complete')
    sys.stdout.flush()


# Remote and local directories
source_path = os.getenv("LOCAL_PATH")
target_path = os.getenv("TARGET_MOVE_PATH")

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

banks = [
    "BNIAIDJA", "BNINIDJA", "BRINIDJA", "BSDRIDJA", "BSMDIDJA", "BTANIDJA", 
    "CENAIDJA", "CITIIDJX", "DBSBIDJA", "FASTIDJA", "MEGAIDJA", "NISPIDJA", 
    "BBBAIDJA", "BBIJIDJA", "BDINIDJA", "BMRIIDJA", "SBJKIDJA", "SYNAIDJ1", 
    "SYBBIDJ1", "SYBDIDJ1", "SYBTIDJ1", "SYCAIDJ1", "SYJGIDJ1", "SYJTIDJ1", 
    "SYTBIDJ1", "ABALIDBS", "SIHBIDJ1", "BMSEIDJA", "BDIPIDJ1", "PDIJIDJ1", 
    "PDJBIDJA", "PDJGIDJ1", "PDJTIDJ1", "PDNTIDJA", "PINBIDJA", "BBLUIDJA", 
    "GNESIDJA", "HNBNIDJA", "HRDAIDJ1", "HSBCIDJA", "IAPTIDJA", "KSEIIDJ1", 
    "LFIBIDJ1", "MASDIDJ1", "MEDHIDS1", "NANOIDJ1", "SYJBIDJ1", "BDKIIDJA", 
    "SYDKIDJA", "ARTGIDJA", "AGTBIDJA", "ATOSIDJ1", "BBAIIDJA", "PDRIIDJA", 
    "BCIAIDJA", "INDOIDJA", "BSSPIDSP", "BUMIIDJA", "CTCBIDJA", "IBBKIDJA", 
    "ICBKIDJA", "JSABIDJ1", "SSPIIDJA", "MAYAIDJA", "MAYOIDJA", "MUABIDJA", 
    "PDKBIDJ1", "PDKSIDJ1", "PDSBIDJ1", "PDYKIDJ1", "BIDXIDJA", "SUNIIDJA", 
    "SYATIDJ1", "SYBKIDJ1", "SYKBIDJ1", "SYKSIDJ1", "SYSBIDJ1", "SYSSIDJ1", 
    "SYYKIDJ1", "YUDBIDJ1", "AWANIDJA", "BKCHIDJA", "BOFAID2X", "BOTKIDJX", 
    "BPIAIDJA", "BUTGIDJ1", "IBKOIDJA", "MCORIDJA", "NETBIDJA", "PDBBIDJ1", 
    "PDBKIDJ1", "PDJMIDJ1", "PDKGIDJ1", "PDKTIDJ1", "PDMLIDJ1", "PDNBIDJ1", 
    "PDSUIDJ1", "PDWRIDJ1", "PDWSIDJA", "PDWUIDJ1", "PUBAIDJ1", "SCBLIDJX", 
    "SYACIDJ1", "SYJMIDJ1", "SYKTIDJ1", "SYONIDJ1", "SYSUIDJ1", "SYWSIDJ1", 
    "VICTIDJ1", "ANZBIDJX", "APIDIDJ1", "ARFAIDJ1", "BBUKIDJA", "BICNIDJA", 
    "BNPAIDJA", "CHASIDJX", "CICTIDJA", "DANAIDJ1", "LMANIDJ1", "PDWGIDJ1", 
    "PDLPIDJ1", "SDOBIDJ1", "MHCCIDJA", "LOMAIDJ1", "MEEKIDJ1", "DEUTIDJA"
]


total_bic = len(banks)


start_time = time.time()

for index_bic, bic in enumerate(banks):
    try:
        move_files( year, month, target_path, source_path, "CreditTransferRecapitulation",bic,index_bic,total_bic)
      
    except ValueError as error:
        print(error)

end_time = time.time()


# Calculate the duration in minutes
duration_seconds = end_time - start_time
duration_minutes = duration_seconds / 60

print(f"Job Start Time: {start_time}")
print(f"Job End Time: {end_time}")
print(f"Job Duration: {duration_minutes:.2f} minutes")

# RejectedCreditTransfer
# CreditTransferRecapitulation