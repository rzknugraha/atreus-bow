from repositories.trn_log_daily import fetch_all_data

def get_data():
    data = fetch_all_data()
    # Process data
    print("Data processed and business logic executed.")
    return data


execute_data = get_data()

if not execute_data:
        print("No data found.")
        

    # Print each row (assuming the database returns rows as tuples)
print("Fetched Data:")
for row in execute_data:
        print(row)
    
    # Example of structured output:
    # Assuming the columns are 'id', 'name', 'value', adjust according to your schema
print("\nStructured Output:")
for row in execute_data:
        sum_tot = row
        print(f"Total: {sum_tot}")

print("\nData processed and business logic executed.")
