import { useEffect, useState } from "react";

function FileUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [convertTo, setConvertTo] = useState("");
  const [formats, setFormats] = useState<string[]>([]);
  const [downloadUrl, setDownloadUrl] = useState<string>("");
  // const serverUrl = "http://127.0.0.1:8000" // dev
  const serverUrl = "https://webmorph-server-605ae8044504.herokuapp.com" // prod

  useEffect(() => {
    fetch(serverUrl + "files/supported-formats")
      .then(res => res.json())
      .then(data => {
        setFormats(data.formats);
        setConvertTo(data.formats[0]);
      });
  }, []);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("convert_to", convertTo);

    try {
      const response = await fetch(serverUrl + "/files/upload", {
        method: "POST",
        body: formData
      });

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url); // store the URL for a clickable link
    } catch (err) {
      console.error(err);
      setDownloadUrl("");
      alert("File conversion failed");
    }
  }

  return (
    <div>
      <h1>File Converter</h1>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <div>
        <span>Convert to:</span>
        <select value={convertTo} onChange={(e) => setConvertTo(e.target.value)}>
          {formats.map((f) => (
            <option key={f} value={f}>{f}</option>
          ))}
        </select>
      </div>
      <button onClick={handleUpload}>Upload & Convert</button>

      {downloadUrl && (
        <div>
          <a href={downloadUrl} download={`converted.${convertTo}`}>
            Click here to download your file
          </a>
        </div>
      )}
    </div>
  );
}

export default FileUploader;
