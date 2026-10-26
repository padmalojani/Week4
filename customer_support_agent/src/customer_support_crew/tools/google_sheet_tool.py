import os
import json
import gspread
from crewai.tools import tool

@tool("Google Sheet Logger Tool")
def log_to_google_sheet(agent_output_context: str) -> str:
    """Useful to log the customer interactions and final resolution directly into the Google Sheet master log file."""
    try:
        # Determine root folder path dynamically to find credentials.json
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        cred_path = os.path.join(base_path, "credentials.json")
        
        if not os.path.exists(cred_path):
            return f"Error: credentials.json not found at {cred_path}"
            
        # Initialize Google Sheets connection
        gc = gspread.service_account(filename=cred_path)
        
        # OPEN VIA EXACT SPREADSHEET KEY ID
        spreadsheet_id = "1JH_0aByr6WBOtk-ueski4dpkg4FGBjHapoINP2sihZ8"
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.get_worksheet(0) # Selects the first sheet/tab
        
        # Determine source by scanning the context text
        context_lower = agent_output_context.lower()
        if "web" in context_lower or "serper" in context_lower or "google search" in context_lower:
            source = "Web Search"
        else:
            source = "Internal Knowledge Base (RAG)"
            
        # Append the context data cleanly to the sheet
        row_data = ["Customer Support Request", agent_output_context.strip(), source]
        worksheet.append_row(row_data)
        
        print(f"--> [DEBUG] Successfully wrote row: {row_data}")
        return "SUCCESS: Row successfully appended to Google Sheet log."
        
    except Exception as e:
        error_msg = f"CRITICAL SHEET ERROR: {str(e)}"
        print(f"--> [DEBUG] {error_msg}")
        return error_msg
