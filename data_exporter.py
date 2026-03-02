import pandas as pd
import os

def export_to_excel(data: list[dict], filename: str):
    """
    Exports a list of dictionaries to an Excel file.
    Expected keys: First Name, Full Name, Email, Department/Research Area, University, Source/Link
    """
    columns = ["First Name", "Full Name", "Email", "Department/Research Area", "University", "Source/Link"]
    
    if not data:
        print("No data extracted during this run. Creating empty files.")
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(data)
    
    # Ensure columns match requirements even if some are missing in some records
    columns = ["First Name", "Full Name", "Email", "Department/Research Area", "University", "Source/Link"]
    for col in columns:
        if col not in df.columns:
            df[col] = "" # Add missing columns filled with empty strings
            
    df = df[columns] # Reorder to match requirements
    
    try:
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Data successfully exported to {os.path.abspath(filename)}")
        
        # Also export as CSV as a fallback so it can be viewed in the IDE
        csv_filename = filename.replace('.xlsx', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"Data also available in CSV format at {os.path.abspath(csv_filename)}")
        
    except Exception as e:
        print(f"Error exporting data: {e}")
