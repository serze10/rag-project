import { Send } from "lucide-react";

import styles from "../styles/chat.module.css";

interface ChatInputProps {
  question: string;
  loading: boolean;
  onQuestionChange: (question: string) => void;
  onSubmit: () => void;
}

export function ChatInput({
  question,
  loading,
  onQuestionChange,
  onSubmit,
}: ChatInputProps) {
  return (
    <div className={styles.inputContainer}>
      <div className={styles.inputWrapper}>
        <textarea
          value={question}
          onChange={(event) =>
            onQuestionChange(event.target.value)
          }
          placeholder="Kysy dokumenteistasi..."
          className={styles.textarea}
          onKeyDown={(event) => {
            if (
              event.key === "Enter" &&
              !event.shiftKey
            ) {
              event.preventDefault();
              onSubmit();
            }
          }}
        />

        <button
          onClick={onSubmit}
          disabled={loading}
          className={styles.sendButton}
        >
          <Send />
        </button>
      </div>
    </div>
  );
}
