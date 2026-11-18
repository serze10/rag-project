"use client";

import { useEffect, useState } from "react";

import styles from "../styles/chat.module.css";
import { ChatInput } from "../components/chat-input";
import { ChatMessages } from "../components/chat-messages";
import type { Message } from "../components/chat-types";
import { Sidebar } from "../components/sidebar";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    async function loadDocuments() {
      try {
        const response = await fetch(
          "http://localhost:8000/documents"
        );
        if (!response.ok) return;
        const data = await response.json();
        setDocuments(data.documents);
      } catch {
        setDocuments([]);
      }
    }

    loadDocuments();
  }, []);

  async function uploadDocuments(files: File[]) {
    setUploading(true);

    try {
      const formData = new FormData();
      files.forEach((file) =>
        formData.append("files", file)
      );

      const response = await fetch(
        "http://localhost:8000/documents",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setDocuments((previous) => {
        const names = new Set([
          ...previous,
          ...data.uploaded,
        ]);
        return Array.from(names).sort((a, b) =>
          a.localeCompare(b)
        );
      });
    } catch {
      window.alert(
        "PDF documents could not be uploaded."
      );
    } finally {
      setUploading(false);
    }
  }
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
      <Sidebar
        documents={documents}
        uploading={uploading}
        onUpload={uploadDocuments}
      />

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