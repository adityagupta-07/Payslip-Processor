import { pickExcelFile, pickFolder } from "./pickers.js";
import { findEmployeeFolders, writeFiles } from "./folders.js";
import { sendJob } from "./api.js";

const chosen = { excel: null, output: null, sharepoint: null };

const yearInput = document.getElementById("year-input");
const processButton = document.getElementById("process-button");
const statusText = document.getElementById("status");

const messageList = document.getElementById("messages");

const buttons = [
    {
        id: "excel-button",
        key: "excel",
        text: "Select Excel File",
        pick: pickExcelFile
    },
    {
        id: "output-button",
        key: "output",
        text: "Select Output Folder",
        pick: pickFolder
    },
    {
        id: "sharepoint-button",
        key: "sharepoint",
        text: "Select SharePoint Payslips Folder (contains the 'Emp_...' folders)",
        pick: pickFolder
    },
];


function showMessages(messages) {
  messageList.innerHTML = "";

  for (const text of messages) {
    const item = document.createElement("li");
    item.textContent = text;
    messageList.appendChild(item);
  }
}


function setupButton(info) {
  const button = document.getElementById(info.id);
  
  button.onclick = async () => {
    const handle = await info.pick();

    if (handle) {
      chosen[info.key] = handle;
      updatePage();
    }
  };
}


function updatePage() {
    for (const info of buttons) {
        const button = document.getElementById(info.id);
        const handle = chosen[info.key];
        button.textContent = handle 
            ? `✓ ${handle.name} (click to change)` 
            : info.text;
        button.classList.toggle("selected", Boolean(handle));
    }

    processButton.disabled = !(
    chosen.excel && chosen.output && chosen.sharepoint && yearInput.value.trim()
    );
}


async function runProcess() {
  processButton.disabled = true;
  showMessages([]);

  try {
    const year = yearInput.value.trim();

    statusText.textContent = "Looking for employee folders...";
    const folders = await findEmployeeFolders(chosen.sharepoint, year);

    statusText.textContent = "Processing payslips...";
    const excelFile = await chosen.excel.getFile();
    const result = await sendJob(excelFile, folders, year);

    statusText.textContent = "Saving files...";
    await writeFiles(chosen.output, result.output);
    await writeFiles(chosen.sharepoint, result.sharepoint);

    showMessages(result.messages);

    statusText.textContent =
      `Processed! Saved ${result.output.length} files to the output folder ` +
      `and ${result.sharepoint.length} PDFs to SharePoint.`;
  } catch (error) {
    statusText.textContent = "Failed: " + error.message;
  }

  updatePage();
}


for (const info of buttons){
    setupButton(info)
}
yearInput.oninput = updatePage;
processButton.onclick = runProcess;
updatePage();