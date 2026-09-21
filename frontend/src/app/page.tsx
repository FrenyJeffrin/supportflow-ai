"use client";

import {
  useEffect,
  useState,
} from "react";


type Message = {
  role: "user" | "assistant";
  content: string;
};


export default function Home() {

  const [sessionId, setSessionId] = useState<string | null>(null);

  const [messages, setMessages] = useState<Message[]>([]);

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);

  const [ready, setReady] = useState(false);


  useEffect(() => {

    async function initializeSession() {

      try {

        const savedSessionId =
          localStorage.getItem(
            "supportflow_session_id"
          );


        if (savedSessionId) {

          setSessionId(savedSessionId);

          const historyResponse =
            await fetch(
              `http://localhost:8000/api/v1/sessions/${savedSessionId}/messages`
            );


          if (historyResponse.ok) {

            const history =
              await historyResponse.json();


            setMessages(
              history.map(
                (item: {
                  role: "user" | "assistant";
                  content: string;
                }) => ({
                  role: item.role,
                  content: item.content,
                })
              )
            );

            setReady(true);

            return;
          }


          localStorage.removeItem(
            "supportflow_session_id"
          );
        }


        const response = await fetch(
          "http://localhost:8000/api/v1/sessions",
          {
            method: "POST",
          }
        );


        if (!response.ok) {
          throw new Error(
            "Could not create session"
          );
        }


        const session = await response.json();


        localStorage.setItem(
          "supportflow_session_id",
          session.id
        );


        setSessionId(session.id);

      } catch (error) {

        console.error(
          "Session initialization failed",
          error
        );

      } finally {

        setReady(true);
      }

    }


    initializeSession();

  }, []);


  async function sendMessage() {

    const cleanMessage =
      message.trim();


    if (
      !cleanMessage ||
      !sessionId ||
      loading
    ) {
      return;
    }


    const userMessage: Message = {
      role: "user",
      content: cleanMessage,
    };


    setMessages(
      (previous) => [
        ...previous,
        userMessage,
      ]
    );


    setMessage("");
    setLoading(true);


    try {

      const result = await fetch(
        "http://localhost:8000/api/v1/chat",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            session_id: sessionId,
            message: cleanMessage,
          }),
        }
      );


      if (!result.ok) {

        throw new Error(
          "Chat request failed"
        );
      }


      const data = await result.json();


      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      };


      setMessages(
        (previous) => [
          ...previous,
          assistantMessage,
        ]
      );

    } catch (error) {

      setMessages(
        (previous) => [
          ...previous,
          {
            role: "assistant",
            content:
              "Sorry, I couldn't process that request.",
          },
        ]
      );

    } finally {

      setLoading(false);

    }
  }


  if (!ready) {

    return (
      <main className="min-h-screen p-8">
        Loading SupportFlow AI...
      </main>
    );

  }


  return (
    <main className="min-h-screen bg-gray-50 p-8">

      <div className="mx-auto max-w-3xl">

        <h1 className="text-3xl font-bold">
          SupportFlow AI
        </h1>

        <p className="mt-2 text-gray-600">
          AI Customer Support Agent
        </p>


        <div className="mt-8 rounded-xl bg-white shadow">


          <div className="h-[500px] overflow-y-auto p-6">

            {messages.length === 0 && (

              <p className="text-gray-400">
                Ask me about orders,
                refunds, shipping,
                or payments.
              </p>

            )}


            <div className="space-y-4">

              {messages.map(
                (item, index) => (

                  <div
                    key={index}
                    className={
                      item.role === "user"
                        ? "ml-auto max-w-[80%] rounded-xl bg-black p-4 text-white"
                        : "mr-auto max-w-[80%] rounded-xl bg-gray-100 p-4 text-gray-900"
                    }
                  >

                    <p className="mb-1 text-xs font-semibold">

                      {item.role === "user"
                        ? "You"
                        : "SupportFlow AI"}

                    </p>


                    <p className="whitespace-pre-wrap">
                      {item.content}
                    </p>

                  </div>

                )
              )}


              {loading && (

                <div className="mr-auto rounded-xl bg-gray-100 p-4 text-gray-500">

                  SupportFlow AI
                  is thinking...

                </div>

              )}

            </div>

          </div>


          <div className="border-t p-4">

            <div className="flex gap-3">

              <input
                value={message}

                onChange={(event) =>
                  setMessage(
                    event.target.value
                  )
                }

                onKeyDown={(event) => {

                  if (
                    event.key === "Enter" &&
                    !event.shiftKey
                  ) {
                    sendMessage();
                  }

                }}

                placeholder="Ask a question..."

                className="flex-1 rounded-lg border p-3 outline-none"
              />


              <button
                onClick={sendMessage}
                disabled={
                  loading ||
                  !sessionId
                }

                className="rounded-lg bg-black px-5 py-3 text-white disabled:opacity-50"
              >

                {loading
                  ? "Thinking..."
                  : "Send"}

              </button>

            </div>

          </div>

        </div>

      </div>

    </main>
  );
}