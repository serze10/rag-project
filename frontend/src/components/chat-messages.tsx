import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";

import styles from "../styles/chat.module.css";
import type { Message } from "./chat-types";

interface ChatMessagesProps {
  messages: Message[];
  loading: boolean;
}

export function ChatMessages({
  messages,
  loading,
}: ChatMessagesProps) {
  return (
    <div className={styles.chatMessages}>
      {messages.length === 0 && (
        <div className={styles.emptyState}>
          <h2 className={styles.emptyTitle}>
            Ask about your documents
          </h2>

          <p className={styles.emptyText}>
            Ask questions about your documents
          </p>
        </div>
      )}

      <div className={styles.messages}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={`${styles.message} ${
              message.role === "assistant"
                ? styles.assistantMessage
                : ""
            }`}
          >
            <div>
              {message.role === "user" ? (
                <User />
              ) : (
                <Bot />
              )}
            </div>

            <div className={styles.messageContent}>
              <ReactMarkdown>
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}

        {loading && (
          <div className={styles.loading}>
            Thinking...
          </div>
        )}
      </div>
    </div>
  );
}
