import React, { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [label, setLabel] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append("image", image);

    try {
      console.log(image);
      setLoading(true);
      const response = await axios.post(
        "http://localhost:5000/api/predict",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log("Response from backend:", response.data);
      if (response.data && response.data.label) {
        setLabel(response.data.label);
      } else {
        setLabel("No prediction available.");
      }
    } catch (error) {
      console.error("Error predicting image:", error);
      setLabel("Error while predicting.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Traffic Sign Recognition</h1>
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="input-file"
          />
          {previewUrl && (
            <img src={previewUrl} alt="Preview" className="preview-image" />
          )}
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? "Predicting..." : "Predict"}
          </button>
        </form>

        {label && (
          <div
            className={`prediction ${
              label.includes("Error") || label.includes("No prediction")
                ? "error"
                : "success"
            }`}
          >
            <strong>Prediction:</strong> {label}
          </div>
        )}
      </div>
    </div>
  );
}
