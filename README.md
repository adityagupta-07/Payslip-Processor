# Payslip Processor

This program is a tool that generates a separate password protected PDF payslip for each employee, a master PDF containing the individual payslips of all employees and password protected PDFs in a separate folder which can be accessed by their own PAN number.

## Project structure

```
├── Payslip_Processor
│   ├── src
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── delete_contents.py
│   │   ├── directories.py
│   │   ├── docx_generator.py
│   │   ├── employee_parser.py
│   │   ├── excel_reader.py
│   │   ├── gui.py
│   │   ├── password_protect_pdf.py
│   │   ├── pdf_converter.py
│   │   └── pipeline.py
│   ├── templates
│   │   └── docx
│   │       ├── template_id.docx
│   │       └── template_no_id.docx
│   └── Dockerfile
├── README.md
└── requirements.txt
```

## Installation

Pull the image:

```
docker pull aadityagupta077/payslip-processor:latest
```

## Usage

Run the container with the following command: 

```
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $HOME:/host_home:ro \
  -v "/path/to/your/output_folder_on_host":"/app/Payslip_Processor":rw \
  aadityagupta077/payslip-processor:latest
```

Just replace `/path/to/your/output_folder_on_host` with the local folder on your machine where you want the container to write output files & folders.

Once the GUI opens, click **Browse**, choose your Excel file and let it process the payslips. When it finishes, click **Show File Location** to see where the output has been saved.

## Output

Everything gets stored inside `/path/to/your/output_folder_on_host` (i.e. the mounted local folder of host):

- *`docx/` stores the generated Word files per employee.*
- *`pdf/individual_pdfs/` stores the converted and unprotected PDFs per employee.*
- *`pdf/protected_individual_pdfs/` stores the same PDFs but password protected with their respective PAN numbers.*
- *`pdf/master_pdf/` stores a single combined PDF of all the employees.*