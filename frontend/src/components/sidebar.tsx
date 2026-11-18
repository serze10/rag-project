import { FileText, Upload } from "lucide-react";

import styles from "../styles/chat.module.css";

export function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.sidebarHeader}>
        <h1 className={styles.sidebarTitle}>
          PDF Assistant
        </h1>

      </div>

      <div className={styles.uploadSection}>
        <button className={styles.uploadButton}>
          <Upload size={18} />
          Add PDF
        </button>
      </div>

      <div className={styles.documents}>
        <h2 className={styles.documentsTitle}>
          Documents
        </h2>

        <div className={styles.documentItem}>
          <FileText size={18} />
          Canaries.pdf
        </div>
      </div>
    </aside>
  );
}
