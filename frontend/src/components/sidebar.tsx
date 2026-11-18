import { FileText, Upload } from "lucide-react";
import { useRef } from "react";

import styles from "../styles/chat.module.css";

interface SidebarProps {
  documents: string[];
  uploading: boolean;
  onUpload: (files: File[]) => void;
}

export function Sidebar({
  documents,
  uploading,
  onUpload,
}: SidebarProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <aside className={styles.sidebar}>
      <div className={styles.sidebarHeader}>
        <h1 className={styles.sidebarTitle}>
          PDF Assistant
        </h1>

      </div>

      <div className={styles.uploadSection}>
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf,.pdf"
          multiple
          hidden
          onChange={(event) => {
            const files = Array.from(
              event.target.files ?? []
            );
            if (files.length > 0) {
              onUpload(files);
            }
            event.target.value = "";
          }}
        />
        <button
          className={styles.uploadButton}
          type="button"
          disabled={uploading}
          onClick={() =>
            fileInputRef.current?.click()
          }
        >
          <Upload size={18} />
          {uploading ? "Adding..." : "Add PDF"}
        </button>
      </div>

      <div className={styles.documents}>
        <h2 className={styles.documentsTitle}>
          Documents
        </h2>

        {documents.map((document) => (
          <div
            key={document}
            className={styles.documentItem}
          >
            <FileText size={18} />
            {document}
          </div>
        ))}
      </div>
    </aside>
  );
}
