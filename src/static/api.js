// Sends the Excel file to the server and returns the files it made.
export async function sendJob(excelFile, employeeFolders, year) {
    // employeeFolders are the folders that contain year folder like '2083-84'
    // here, excelFile return File instance with properties of the selected file
    // File {
    //     name: "your-spreadsheet.xlsx",     // The filename as a string
    //     size: 14235,                        // File size in bytes
    //     type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // MIME type
    //     lastModified: 1735161600000,        // Timestamp of last modification
    //     lastModifiedDate: Date ...          // (Deprecated) Date object
    // }

    const form = new FormData();
    form.append("excel", excelFile);
    form.append("folders", JSON.stringify(employeeFolders));
    form.append("year", year);

    const response = await fetch("/api/process", { method: "POST", body: form });
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error);
    }

    return data;
}