'use client';
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <div style={{ 
        width: '193vh', 
        height: '1000px',
        display: 'flex',
        marginTop: '85vh'
      }}>
        <iframe
          src="/data/mapa.html"
          style={{
            width: '100%',
            height: '100%',
            border: 'none'
          }}
          title="Mapa Interactivo"
        />
      </div>
      
    </div>
  );
}