"use client";
import { useState } from "react";
import "./SideBar.css";

export default function SideBar() {
  const [isOpen, setIsOpen] = useState(false);
  const [submenuOpen, setSubmenuOpen] = useState(false);

  return (
    <>
      {/* Botón hamburguesa */}
      {!isOpen && (
        <button
          className="open-menu-btn"
          onClick={() => setIsOpen(true)}
          aria-label="Abrir menú"
        >
          ☰
        </button>
      )}

      {/* Sidebar */}
      <div className={`container-menu ${isOpen ? "open" : ""}`} aria-hidden={!isOpen}>
          {/* Botón cerrar */}
          <button className="close-menu" onClick={() => setIsOpen(false)}>
            <img src="/close.png" alt="close button" />
          </button>
        <div className="cont-menu" role="dialog" aria-label="Menú lateral">
          <nav>
            <a href="/Biografia">Biografía</a>
            <a href="/Habilidades">Habilidades</a>

            <a href="/Portafolio">Portafolio</a>
          </nav>
        </div>
      </div>
    </>
  );
}
