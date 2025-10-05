"use client";
import { useState } from "react";
import Link from "next/link";
import "./SideBar.css";

export default function SideBar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Fondo oscuro detrás del menú */}
      {isOpen && (
        <div
          className="menu-overlay open"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        ></div>
      )}

      {/* Botón hamburguesa */}
      {!isOpen && (
        <button
          className="open-menu-btn"
          onClick={() => setIsOpen(true)}
          aria-label="Abrir menú lateral"
          aria-expanded={isOpen}
        >
          ☰
        </button>
      )}

      {/* Sidebar */}
      <aside
        className={`container-menu ${isOpen ? "open" : ""}`}
        aria-hidden={!isOpen}
      >
        <img className="logoSpace" src="/logo.png" alt="logo SpaceApps" />
        <button
          className="close-menu"
          onClick={() => setIsOpen(false)}
          aria-label="Cerrar menú lateral"
        >
          <img className="close-icon" src="/close.png" alt="Cerrar menú" />
        </button>

        <div className="menu-links">
          <Link href="/">
            Ir a la página principal
          </Link>

          <Link href="/info">Predicciones</Link>
        </div>
      </aside>
      
    </>
  );
}
