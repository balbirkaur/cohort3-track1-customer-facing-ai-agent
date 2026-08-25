"use client";

import { FormEvent, useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type ApiResponse = {
  response?: unknown;
};

function normalizeResponse(response: unknown): string {
  if (typeof response === "string") {
    return response;
  }

  if (Array.isArray(response)) {
    return response
      .map((item) => {
        if (
          typeof item === "object" &&
          item !== null &&
          "text" in item
        ) {
          return String((item as { text: unknown }).text);
        }

        return "";
      })
      .filter(Boolean)
      .join("\n");
  }

  if (typeof response === "object" && response !== null) {
    if ("text" in response) {
      return String((response as { text: unknown }).text);
    }

    return JSON.stringify(response);
  }

  return String(response ?? "");
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm your Banking Customer Support Agent. How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!input.trim() || loading) {
      return;
    }

    const userMessage = input.trim();

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Unable to contact AI agent");
      }

      const data: ApiResponse = await response.json();

      const responseText = normalizeResponse(data.response);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            responseText ||
            "I couldn't generate a response. Please try again.",
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the customer support agent. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col px-4 py-8">
        <header className="mb-6">
          <p className="text-sm font-medium text-blue-400">
            COHORT 3 · TRACK 1
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Banking Customer Resolution Agent
          </h1>

          <p className="mt-2 text-slate-400">
            AI-powered customer support with RAG, transaction
            tools and human escalation.
          </p>
        </header>

        <section className="flex flex-1 flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl">
          <div className="flex-1 space-y-4 overflow-y-auto p-6">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-slate-800 text-slate-100"
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="rounded-2xl bg-slate-800 px-4 py-3 text-slate-400">
                  Agent is thinking...
                </div>
              </div>
            )}
          </div>

          <form
            onSubmit={sendMessage}
            className="border-t border-slate-800 p-4"
          >
            <div className="flex gap-3">
              <input
                value={input}
                onChange={(event) =>
                  setInput(event.target.value)
                }
                placeholder="Ask about a payment, transaction or banking issue..."
                className="flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-blue-500"
              />

              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="rounded-xl bg-blue-600 px-6 py-3 font-medium hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Send
              </button>
            </div>
          </form>
        </section>

        <footer className="mt-4 text-center text-xs text-slate-500">
          AI responses are informational. Sensitive credentials
          such as OTP, PIN and CVV should never be shared.
        </footer>
      </div>
    </main>
  );
}