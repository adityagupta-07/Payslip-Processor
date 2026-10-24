// Returns true if the folder has a subfolder with this name.
async function hasSubfolder(folder, name) {
  try {
    await folder.getDirectoryHandle(name);
    return true;
  } catch (error) {
    return false;
  }
}


// Returns the names of employee folders that contain the year folder.
export async function findEmployeeFolders(payslipsFolder, year) {
  const names = [];

  for await (const entry of payslipsFolder.values()) {
    if (entry.kind === "directory" && (await hasSubfolder(entry, year))) {
      names.push(entry.name);
    }
  }

  return names;
}


// Turns the text sent by the server back into file bytes.
function base64ToBytes(text) {
  const binary = atob(text);
  const bytes = new Uint8Array(binary.length);

  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }

  return bytes;
}


// Opens "Emp_11 - Name/2083-84/May.pdf" by creating folders as needed.
async function getFileHandle(rootFolder, relativePath) {
  const parts = relativePath.split("/");
  const fileName = parts.pop();

  let folder = rootFolder;
  for (const part of parts) {
    folder = await folder.getDirectoryHandle(part, { create: true });
  }

  return await folder.getFileHandle(fileName, { create: true });
}


// Saves every file into the folder. Existing files are overwritten.
export async function writeFiles(rootFolder, files) {
  for (const file of files) {
    const handle = await getFileHandle(rootFolder, file.path);
    const writable = await handle.createWritable();

    await writable.write(base64ToBytes(file.data));
    await writable.close();
  }
}