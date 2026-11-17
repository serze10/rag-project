"use client";

import { useState } from "react";

import styles from "../styles/chat.module.css";
import { ChatInput } from "../components/chat-input";
import { ChatMessages } from "../components/chat-messages";
import type { Message } from "../components/chat-types";
import { Sidebar } from "../components/sidebar";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  async function askQuestion() {
    if (!question.trim()) {
      return;
    }

    const currentQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            question: currentQuestion,
          }),
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Virhe yhteydessä palvelimeen.",
        },
      ]);
    }

    setLoading(false);
  }

  return (
    <main className={styles.page}>
      <Sidebar />

      <section className={styles.chatContainer}>
        <ChatMessages
          messages={messages}
          loading={loading}
        />
        <ChatInput
          question={question}
          loading={loading}
          onQuestionChange={setQuestion}
          onSubmit={askQuestion}
        />
      </section>
    </main>
  );
}