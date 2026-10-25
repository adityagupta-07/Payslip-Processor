import os
from dotenv import load_dotenv, dotenv_values
from office365.sharepoint.client_context import ClientContext

load_dotenv()

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

site_url = "https://ut365.sharepoint.com/sites/UT-Nepal"

CTX = ClientContext(site_url).with_username_and_password(tenant_id, client_id, username, password)


def direct_upload_pdf_to_sharepoint(pdf_path, filename, target_url, CTX):
    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    target_folder = CTX.web.get_folder_by_server_relative_url(target_url)

    target_file = target_folder.upload_file(filename, pdf_content)

    CTX.execute_query()

    print(filename, "has been uploaded to URL:", target_file.serverRelativeUrl)


pdf_path = r"C:\Coding\Python\try\data\input\Ultra Payslips\pdf\protected_individual_pdfs\Bindu_Shrestha_May_2026_06.pdf"
filename = "Bindu_Shrestha_May_2026_06.pdf"

target_url = "/sites/UT-Nepal/Shared Documents/Territory/Admin"

direct_upload_pdf_to_sharepoint(pdf_path, filename, target_url, CTX)

