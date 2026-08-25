"use client";

import { FormEvent, useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type ApiResponse = {
  response?: unknown;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL 
console.log("NEXT_PUBLIC_API_URL =", process.env.NEXT_PUBLIC_API_URL);

const suggestions = [
  "My card payment failed but money was deducted.",
  "Please check transaction TXN1001.",
  "I don't recognize a transaction.",
  "My issue is still unresolved.",
];

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
          return String(
            (item as { text: unknown }).text
          );
        }

        return "";
      })
      .filter(Boolean)
      .join("\n");
  }

  if (
    typeof response === "object" &&
    response !== null
  ) {
    if ("text" in response) {
      return String(
        (response as { text: unknown }).text
      );
    }

    return JSON.stringify(response);
  }

  return String(response ?? "");
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(
    event?: FormEvent<HTMLFormElement>,
    customMessage?: string
  ) {
    event?.preventDefault();

    const userMessage =
      customMessage ?? input.trim();

    if (!userMessage || loading) {
      return;
    }

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
        `${API_URL}/chat`,
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
        throw new Error(
          `AI agent returned ${response.status}`
        );
      }

      const data: ApiResponse =
        await response.json();

      const responseText =
        normalizeResponse(data.response);

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
      console.error("AI Agent Error:", error);

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
    <main className="min-h-screen bg-[#f5f7fb] text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-7xl">

        {/* Sidebar */}
        <aside className="hidden w-72 flex-col border-r border-slate-200 bg-white p-6 lg:flex">
          <div>

            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-xl font-bold text-white">
                AI
              </div>

              <div>
                <h2 className="font-bold">
                  BankAssist AI
                </h2>

                <p className="text-xs text-slate-500">
                  Customer Resolution Agent
                </p>
              </div>
            </div>

            <div className="mt-8">
              <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
                Agent capabilities
              </p>

              <div className="space-y-2">
                <Capability
                  icon="🔎"
                  title="Knowledge Search"
                  text="Banking policies"
                />

                <Capability
                  icon="💳"
                  title="Transaction Lookup"
                  text="Real-time tool access"
                />

                <Capability
                  icon="🎫"
                  title="Support Tickets"
                  text="Automated case creation"
                />

                <Capability
                  icon="👤"
                  title="Human Escalation"
                  text="Specialist handoff"
                />
              </div>
            </div>
          </div>

          <div className="mt-auto rounded-xl bg-slate-50 p-4">
            <p className="text-xs font-semibold text-slate-700">
              Security
            </p>

            <p className="mt-2 text-xs leading-5 text-slate-500">
              Never share your OTP, PIN, password,
              CVV or full card number with an AI
              assistant.
            </p>
          </div>
        </aside>

        {/* Main */}
        <section className="flex min-h-screen flex-1 flex-col">

          {/* Header */}
          <header className="border-b border-slate-200 bg-white px-5 py-4 sm:px-8">
            <div className="flex items-center justify-between">

              <div>
                <p className="text-xs font-semibold tracking-wider text-blue-600">
                  APAC GENAI ACADEMY · COHORT 3 · TRACK 1
                </p>

                <h1 className="mt-1 text-xl font-bold sm:text-2xl">
                  Customer Resolution Agent
                </h1>

                <p className="mt-1 text-xs text-slate-400">
                  AI-powered banking customer support
                </p>
              </div>

              <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-2 text-xs font-medium text-emerald-700">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                Agent Online
              </div>

            </div>
          </header>

          {/* Chat */}
          <div className="flex flex-1 flex-col">
            <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col px-5 py-8 sm:px-8">

              {messages.length === 0 ? (

                <div className="flex flex-1 flex-col items-center justify-center">

                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-600 text-2xl font-bold text-white shadow-lg">
                    AI
                  </div>

                  <h2 className="mt-5 text-center text-3xl font-bold">
                    How can I help you?
                  </h2>

                  <p className="mt-2 max-w-xl text-center text-slate-500">
                    Ask about payments, transactions,
                    banking policies, unresolved issues
                    or request human assistance.
                  </p>

                  <div className="mt-8 grid w-full max-w-2xl gap-3 sm:grid-cols-2">

                    {suggestions.map(
                      (suggestion) => (
                        <button
                          key={suggestion}
                          type="button"
                          onClick={() =>
                            sendMessage(
                              undefined,
                              suggestion
                            )
                          }
                          disabled={loading}
                          className="rounded-xl border border-slate-200 bg-white p-4 text-left text-sm shadow-sm transition hover:border-blue-300 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
                        >
                          <span className="text-slate-700">
                            {suggestion}
                          </span>
                        </button>
                      )
                    )}

                  </div>
                </div>

              ) : (

                <div className="flex-1 space-y-5 overflow-y-auto pb-6">

                  {messages.map(
                    (message, index) => (
                      <div
                        key={index}
                        className={`flex ${
                          message.role === "user"
                            ? "justify-end"
                            : "justify-start"
                        }`}
                      >
                        <div
                          className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-5 py-4 text-sm leading-6 ${
                            message.role === "user"
                              ? "bg-blue-600 text-white"
                              : "border border-slate-200 bg-white text-slate-700 shadow-sm"
                          }`}
                        >
                          {message.content}
                        </div>
                      </div>
                    )
                  )}

                  {loading && (
                    <div className="flex justify-start">
                      <div className="rounded-2xl border border-slate-200 bg-white px-5 py-4 text-sm text-slate-500 shadow-sm">
                        <div className="flex items-center gap-2">
                          <span className="h-2 w-2 animate-pulse rounded-full bg-blue-500" />
                          <span>
                            Agent is analyzing your request...
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                </div>
              )}

              {/* Input */}
              <form
                onSubmit={sendMessage}
                className="mt-5"
              >
                <div className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-2 shadow-lg">

                  <input
                    value={input}
                    onChange={(event) =>
                      setInput(event.target.value)
                    }
                    placeholder="Ask your banking question..."
                    className="flex-1 bg-transparent px-4 py-3 text-sm outline-none"
                    disabled={loading}
                  />

                  <button
                    type="submit"
                    disabled={
                      loading ||
                      !input.trim()
                    }
                    className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    {loading
                      ? "Thinking..."
                      : "Send"}
                  </button>

                </div>

                <p className="mt-3 text-center text-xs text-slate-400">
                  AI-generated responses may require
                  verification. Never share sensitive
                  credentials.
                </p>
              </form>

            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

function Capability({
  icon,
  title,
  text,
}: {
  icon: string;
  title: string;
  text: string;
}) {
  return (
    <div className="flex items-center gap-3 rounded-xl p-3 transition hover:bg-slate-50">

      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100">
        {icon}
      </div>

      <div>
        <p className="text-sm font-medium text-slate-700">
          {title}
        </p>

        <p className="text-xs text-slate-400">
          {text}
        </p>
      </div>

    </div>
  );
}