import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a DOCX file.");
      setIsError(true);
      setTimeout(() => {
      setMessage("");
      }, 3000);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/redact",
        formData,
        {
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      );

      const link = document.createElement("a");

      link.href = url;
      link.download = "redacted.docx";

      document.body.appendChild(link);

      link.click();

      link.remove();

      window.URL.revokeObjectURL(url);

      setMessage("✅ Document redacted successfully!");
      setIsError(false);
      setTimeout(() => {
        setMessage("");
      }, 3000);
      setFile(null);
    } catch (error) {
      console.error(error);
      setMessage("Something went wrong.");

      setTimeout(() => {
       setMessage("");
       }, 3000);
      setIsError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">

        <h1>🛡️ PiiDactor</h1>

        <p>
          Upload a DOCX document and automatically detect
          and redact sensitive information.
        </p>

        <label className="upload-box">

          <input
            type="file"
            accept=".docx"
            hidden
            onChange={(e) => setFile(e.target.files[0])}
          />

          <div className="upload-content">

            <div className="upload-icon">📄</div>

            <h3>
              {file ? file.name : "Choose a DOCX File"}
            </h3>

            <p>
              Click here to browse your computer
            </p>

          </div>

        </label>

        <button
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "⏳ Redacting Document..." : "🛡️ Redact Document"}
        </button>
         {message && (
         <div className={isError ? "error-message" : "success-message"}>
           {message}
           </div>
           )}
      </div>
    </div>
  );
}

export default App;