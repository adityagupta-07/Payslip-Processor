// Opens file picker window and returns the file handle, or null if the user cancelled.
export async function pickExcelFile() {
  try {
    const [handle] = await window.showOpenFilePicker({
      types: [{
        description: "Excel files",
        accept: {
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
        },
      }],
    });
    return handle;
  } catch (error) {
    return handleCancel(error);
  }
}


// Opens file picker window and returns the folder handle, or null if the user cancelled.
export async function pickFolder(id) {
  try {
    return await window.showDirectoryPicker({mode: "readwrite" });
  } catch (error) {
    return handleCancel(error);
  }
}


function handleCancel(error) {
  if (error.name === "AbortError") {
    return null;
  }
  throw error;
}