"use client";
import { useState } from "react";

export default function UrlShortener() {
  const [longUrl, setLongUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleShorten = async () => {
    if (!longUrl) return;
    setLoading(true);
    setShortUrl("");

    try {
      const res = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
        }/api/shorten`,
        {
          method: "POST",
          body: new URLSearchParams({ long_url: longUrl }),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      const data = await res.json();
      setShortUrl(data.short_url);
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", textAlign: "center" }}>
      <h2 className="mb-2">🔗 Shorten your URL</h2>
      <input
        type="text"
        placeholder="Paste your long URL here..."
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
        style={{
          width: "100%",
          padding: 12,
          fontSize: 16,
          borderRadius: 8,
          border: "1px solid #ccc",
        }}
      />
      <button
        onClick={handleShorten}
        className="px-4 py-2 border border-gray-400 rounded-md hover:bg-gray-500 transition-colors duration-150"
        style={{ marginTop: 16, padding: "10px 20px", fontSize: 16 }}
        disabled={loading}
      >
        {loading ? "Generating..." : "Shorten"}
      </button>

      {shortUrl && (
        <div style={{ marginTop: 24 }}>
          <p>
            <span>{`✅ Here's your short link:`}</span>
            <br />
            <a href={shortUrl} target="_blank" rel="noreferrer">
              {shortUrl}
            </a>
          </p>
        </div>
      )}
    </div>
  );
}
