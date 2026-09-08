"use client";

import { useState } from "react";

export default function Home() {
  const [status, setStatus] = useState("Not checked");

  async function checkBackend(){
    try {
      const response = await fetch("http://localhost:8000/health");

      const data= await response.json();

      setStatus(`${data.service}: ${data.status}`);
    }
    catch {
      setStatus("Backend unavailable")
    }
  }
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold">
        SupportFlow AI
      </h1>

      <p className="mt-4 text-gray-600">
        AI-powered customer support platform
      </p>

      <div className="mt-8 rounded-lg border p-6">
        <h2 className="text-xl font-semibold">
          System Status
        </h2>

        <p className="mt-3">
          Backend: {status}
        </p>

        <button
          onClick={checkBackend}
          className="mt-4 rounded bg-black px-4 py-2 text-white"
        >
          Check Backend
        </button>
      </div>
    </main>
  );
}