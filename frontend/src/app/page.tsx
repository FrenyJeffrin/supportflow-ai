"use client";

import { useState } from "react";


export default function Home() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);


  async function sendMessage() {

    if (!message.trim()) {
      return;
    }

    setLoading(true);
    setResponse("");

    try {

      const result = await fetch(
        "http://localhost:8000/api/v1/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            message,
          }),
        }
      );

      if (!result.ok) {
        throw new Error(
          "Request failed"
        );
      }

      const data = await result.json();

      setResponse(data.response);

    } catch (error) {

      setResponse(
        "Sorry, something went wrong."
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <main className="min-h-screen bg-gray-50 p-8">

      <div className="mx-auto max-w-3xl">

        <h1 className="text-3xl text-gray-400 font-bold">
          SupportFlow AI
        </h1>

        <p className="mt-2 text-gray-600">
          AI Customer Support Agent
        </p>


        <div className="mt-8 rounded-xl bg-white p-6 shadow">

          <div className="min-h-40 rounded-lg border  border-gray-300 p-4">

            {response ? (
              <div>
                <p className="text-sm font-semibold text-gray-300">
                  SupportFlow AI
                </p>

                <p className="mt-2 whitespace-pre-wrap text-gray-400">
                  {response}
                </p>
              </div>
            ) : (
              <p className="text-gray-400">
                Ask me about orders, refunds,
                shipping, or payments.
              </p>
            )}

          </div>


          <div className="mt-4 flex gap-3">

            <input
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
              placeholder="Ask a question..."
              className="flex-1 rounded-lg border border-gray-300 p-3 text-gray-400 placeholder:text-gray-300 outline-none"
            />

            <button
              onClick={sendMessage}
              disabled={loading}
              className="rounded-lg bg-black px-5 py-3 text-white disabled:opacity-50"
            >
              {loading
                ? "Thinking..."
                : "Send"}
            </button>

          </div>

        </div>

      </div>

    </main>
  );
}