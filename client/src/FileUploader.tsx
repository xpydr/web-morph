
import { Icon } from "@iconify/react";
import { useEffect, useState } from "react";
import Dropzone from "react-dropzone";

function FileUploader() {
  const [files, setFiles] = useState<File[]>([]);
  const [convertTo, setConvertTo] = useState("");
  const [formats, setFormats] = useState<string[]>([]);
  const [downloadUrl, setDownloadUrl] = useState<string>("");

  // const serverUrl = "http://127.0.0.1:8000" // dev
  const serverUrl = "https://webmorph-server-605ae8044504.herokuapp.com" // prod

  useEffect(() => {
    fetch(serverUrl + "/files/supported-formats")
      .then(res => res.json())
      .then(data => {
        setFormats(data.formats);
        setConvertTo(data.formats[0]);
      });
  }, []); 

  const handleUpload = async () => {
    if (files.length === 0) {
      alert("Select at least one file");
      return;
    }

    if (!convertTo) console.log("Using default conversion to JPG")
    if (!convertTo) setConvertTo("jpg")

    const formData = new FormData();

    formData.append("convert_to", convertTo);
    files.forEach(f => { if (f) formData.append("files", f) });

    console.log(formData)
    console.log(files)
    console.log(convertTo)

    try {
      const response = await fetch(serverUrl + `/files/upload?convert_to=${convertTo}`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        console.log(response);
        alert("Conversion failed");
        return;
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      setDownloadUrl(url);

    } catch (err) {
      console.error(err);
      setDownloadUrl("");
      alert("File conversion failed");
    }
  }

  const handleDelete = (index: number) => {
    const newFiles = files.filter((_, i) => {
      if (i !== index) return true;
    });
    setFiles(newFiles);
  }

  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="text-3xl m-8 underline underline-offset-8">
        File Converter
      </h1>

      <div className="flex flex-col gap-4">
        <div className="flex items-center border rounded p-2 m-2">
          <span>Convert to: </span>
          <select
            value={convertTo}
            onChange={(e) => setConvertTo(e.target.value)}
            className="bg-black"
          >
            {formats.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>
        </div>
        <button onClick={handleUpload} className="border rounded p-2 m-2 bg-cyan-700">Convert</button>
      </div>
      <Dropzone onDrop={(acceptedFiles) => setFiles(acceptedFiles)}>
        {({ getRootProps, getInputProps }) => (
          <section className="border box-border rounded m-24 min-w-xl">
            <div {...getRootProps()}>
              <input {...getInputProps()} />
              <p className="p-24">Drag & drop files here, or click to select</p>
            </div>
          </section>
        )}
      </Dropzone>

      {downloadUrl && (
        <div className="mt-4">
          <a href={downloadUrl} download="converted_files.zip">
            Click here to download your files
          </a>
        </div>
      )}

      <div className="border rounded min-w-xl">
        {files && (
          <ul>
            {files.map((file, i) => (
              <li className="p-1 flex gap-2" key={`${file.name}-${file.lastModified}-${file.size}`}>
                {file?.name}
                <Icon icon="typcn:delete-outline" width="24" height="24" className="hover:cursor-pointer hover:text-red-700"
                  onClick={() => handleDelete(i)} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default FileUploader;
