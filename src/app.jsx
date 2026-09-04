const { useState, useEffect, useCallback, useRef } = React;

// ── GITHUB CONFIG ──────────────────────────────────────────────────────────
// Set these to your repo. Leave POSTS_PATH as "posts" to use a /posts folder.
const GH_CONFIG = {
  owner: "MetroMcD",
  repo:  "sage-news",
  branch: "main",
  postsPath: "posts"
};

// ── TWEAK DEFAULTS ─────────────────────────────────────────────────────────
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accentColor": "#ffd22e",
  "cardRadius": 14,
  "postsPerPage": 8,
  "showSidebar": false,
  "headerStyle": "banner"
}/*EDITMODE-END*/;

// ── FALLBACK SAMPLE POSTS (shown when GitHub is not configured) ────────────
const SAMPLE_POSTS = [
  {
    id: "sample-1",
    slug: "sage-100-release",
    title: "Sage 100 v9.0.3 – Was das neue Release bringt",
    summary: "Das März-Update bringt überarbeitete Buchungsmasken, verbesserte DATEV-Schnittstelle und Korrekturen bei der Umsatzsteuer-Voranmeldung.",
    category: "Sage 100", tag: "Release", date: "28. Apr 2026", readTime: "4 min", featured: true,
    body: ""
  },
  {
    id: "sample-2",
    slug: "sage-x3-self-service",
    title: "Sage X3 People: HR-Modul bekommt Self-Service-Portal",
    summary: "Ab Version 12.1 können Mitarbeitende Urlaubsanträge, Zeitkorrekturen und Gehaltsabrechnungen direkt im Browser bearbeiten.",
    category: "Sage X3", tag: "Neu", date: "22. Apr 2026", readTime: "5 min", featured: false,
    body: ""
  },
  {
    id: "sample-3",
    slug: "sage-operations-ki",
    title: "Sage Operations: Produktionsplanung jetzt mit KI-Unterstützung",
    summary: "Sage Operations erhält eine Kapazitätsplanung mit KI-gestützten Vorschlägen für Maschinenauslastung und Schichtplanung.",
    category: "Sage Operations", tag: "KI", date: "18. Apr 2026", readTime: "6 min", featured: true,
    body: ""
  },
  {
    id: "sample-4",
    slug: "gobd-2026",
    title: "GoBD 2026: Was Sage-Anwender jetzt prüfen müssen",
    summary: "Die aktualisierte GoBD-Fassung stellt neue Anforderungen an die Unveränderbarkeit von Belegen. Checkliste für Sage 100 und X3.",
    category: "Sage 100", tag: "Compliance", date: "14. Apr 2026", readTime: "7 min", featured: false,
    body: ""
  },
  {
    id: "sample-5",
    slug: "sage-x3-cloud-frankfurt",
    title: "Sage X3 Cloud: Verfügbarkeit in deutschen Rechenzentren",
    summary: "Sage bestätigt: X3 läuft ab Q3 2026 in AWS Frankfurt mit DSGVO-konformer Datenhaltung.",
    category: "Sage X3", tag: "Cloud", date: "10. Apr 2026", readTime: "5 min", featured: false,
    body: ""
  },
  {
    id: "sample-6",
    slug: "sage-intact-deutschland",
    title: "Sage Intact: Was der Einstieg in Deutschland bedeutet",
    summary: "Sage Intact ist in den USA ein etabliertes Mid-Market-ERP. Ein erster Überblick zur perspektivischen Deutschland-Einführung.",
    category: "Sage Intact", tag: "Perspektive", date: "5. Apr 2026", readTime: "8 min", featured: false,
    body: ""
  }
];

// ── MARKDOWN FRONTMATTER PARSER ────────────────────────────────────────────
function parseFrontmatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) return { meta: {}, body: raw };
  const meta = {};
  match[1].split("\n").forEach(line => {
    const sep = line.indexOf(":");
    if (sep < 0) return;
    const k = line.slice(0, sep).trim();
    const v = line.slice(sep + 1).trim().replace(/^["']|["']$/g, "");
    meta[k] = v;
  });
  return { meta, body: match[2].trim() };
}

function parseGermanDate(dateStr) {
  if (!dateStr) return null;
  const months = {
    januar: 0, februar: 1, maerz: 2, märz: 2, april: 3, mai: 4, juni: 5,
    juli: 6, august: 7, september: 8, oktober: 9, november: 10, dezember: 11
  };
  const match = dateStr.trim().toLowerCase().match(/^(\d{1,2})\.\s*([a-zäöü]+)\s+(\d{4})$/i);
  if (!match) return null;
  const day = Number(match[1]);
  const month = months[match[2]];
  const year = Number(match[3]);
  if (month === undefined) return null;
  return new Date(year, month, day);
}

function isFeaturedActive(post) {
  if (!post.featured) return false;
  const postDate = parseGermanDate(post.date);
  if (!postDate) return true;
  const now = new Date();
  const diffDays = (now - postDate) / (1000 * 60 * 60 * 24);
  return diffDays >= 0 && diffDays < 7;
}

// ── POSTS MANIFEST LOADER ───────────────────────────────────────────────────
async function loadPostsFromManifest() {
  const manifestUrl = `./posts-manifest.json?v=${Date.now()}`;
  const res = await fetch(manifestUrl, { cache: "no-store" });
  if (!res.ok) throw new Error(`Manifest ${res.status}`);
  const manifest = await res.json();
  return { posts: manifest.posts || [], source: "manifest" };
}

// ── BRAND COLORS ───────────────────────────────────────────────────────────
const CATEGORY_META = {
  "Alle":             { color: "#0a3b93", bg: "#dceeff" },
  "Sage 100":         { color: "#0a3b93", bg: "#dceeff" },
  "Sage X3":          { color: "#1a6b3a", bg: "#d4f0e0" },
  "Sage Operations":  { color: "#7b3a00", bg: "#fde8cc" },
  "Sage Intact":      { color: "#5a1d8a", bg: "#ede0f8" }
};
const TAG_COLORS = {
  "Release":    { bg: "#e8f0fe", color: "#1a56db" },
  "Neu":        { bg: "#d4f0e0", color: "#1a6b3a" },
  "KI":         { bg: "#fde8cc", color: "#7b3a00" },
  "Cloud":      { bg: "#e0f0ff", color: "#0a5a99" },
  "Compliance": { bg: "#fde8e8", color: "#9b1c1c" },
  "Perspektive":{ bg: "#ede0f8", color: "#5a1d8a" },
  "Tool":       { bg: "#f0f0f0", color: "#374151" },
  "API":        { bg: "#e8fce8", color: "#1a6b3a" },
  "News":       { bg: "#f0f4ff", color: "#3730a3" }
};

// ── BADGE COMPONENTS ───────────────────────────────────────────────────────
function CategoryBadge({ category, small }) {
  const meta = CATEGORY_META[category] || CATEGORY_META["Alle"];
  return (
    <span style={{
      display: "inline-block", background: meta.bg, color: meta.color,
      fontWeight: 700, fontSize: small ? "11px" : "12px",
      letterSpacing: "0.03em", padding: small ? "2px 8px" : "3px 10px",
      borderRadius: "999px", whiteSpace: "nowrap"
    }}>{category}</span>
  );
}

function TagBadge({ tag }) {
  const meta = TAG_COLORS[tag] || { bg: "#f0f0f0", color: "#374151" };
  return (
    <span style={{
      display: "inline-block", background: meta.bg, color: meta.color,
      fontWeight: 600, fontSize: "11px", padding: "2px 8px",
      borderRadius: "999px", whiteSpace: "nowrap"
    }}>{tag}</span>
  );
}

// ── LOGO SVG ───────────────────────────────────────────────────────────────
function LogoSVG() {
  return (
    <svg width="130" height="38" viewBox="0 0 130 38" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: "block" }}>
      {/* "sage" block */}
      <rect x="0" y="3" width="58" height="32" rx="7" fill="#082b6f"/>
      <rect x="0.75" y="3.75" width="56.5" height="30.5" rx="6.25" stroke="white" strokeWidth="1.5" strokeOpacity="0.18"/>
      <text x="29" y="24.5" textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight="900" fontSize="16" letterSpacing="-0.5" fill="white">sage</text>
      {/* "news" text */}
      <text x="66" y="25" fontFamily="Inter, sans-serif" fontWeight="900" fontSize="18" letterSpacing="-0.7" fill="#38a9f5">news</text>
      {/* dot accent */}
      <circle cx="123" cy="10" r="4" fill="#ffc82e"/>
    </svg>
  );
}

// ── HEADER ─────────────────────────────────────────────────────────────────
function Header({ page, setPage, accentColor }) {
  const [menuOpen, setMenuOpen] = useState(false);
  // href = echte, crawlbare URL. spa:true faengt den Klick clientseitig ab
  // (siehe NavItem), die Seite laedt dann nicht neu.
  //
  // Die Bereiche sind bewusst NICHT clientseitig: sie zeigten sonst eine
  // zweite, eigene Ansicht mit nur 8 Beitraegen, waehrend derselbe Menuepunkt
  // auf einer Beitragsseite — die kein app.js laedt — zur vollstaendigen
  // Kategorieseite fuehrte. Ein Menuepunkt, zwei Ergebnisse. Jetzt fuehren
  // beide Wege auf dieselbe Seite.
  const navItems = [
    { id: "home",        label: "Alle News",       href: "/", spa: true },
    { id: "sage100",     label: "Sage 100",        href: "/kategorie/sage-100/" },
    { id: "sagex3",      label: "Sage X3",         href: "/kategorie/sage-x3/" },
    { id: "operations",  label: "Sage Operations", href: "/kategorie/sage-operations/" },
    { id: "systemcheck", label: "Systemcheck",    href: "/systemcheck", spa: true },
    { id: "info",        label: "Info",           href: "/#info", spa: true }
  ];

  function handleNav(id) { setPage(id); setMenuOpen(false); }

  return (
    <header style={{
      background: "var(--sn-blue-950)",
      borderBottom: "1.5px solid rgba(255,255,255,0.08)",
      position: "sticky", top: 0, zIndex: 100
    }}>
      <div style={{ maxWidth: "1140px", margin: "0 auto", padding: "0 16px" }}>
        {/* Top bar */}
        <div style={{ display: "flex", alignItems: "center", height: "64px", gap: "16px" }}>

          {/* Logo */}
          <button onClick={() => handleNav("home")} style={{
            background: "none", border: "none", cursor: "pointer",
            padding: 0, flexShrink: 0, lineHeight: 0
          }} title="Zur Startseite">
            <img src="assets/sage-news_logo_3.png" alt="sage news"
              style={{ height: "52px", width: "auto", display: "block", mixBlendMode: "lighten" }} />
          </button>

          {/* Divider — hidden on mobile */}
          <div style={{ width: "1px", height: "28px", background: "rgba(255,255,255,0.12)", flexShrink: 0, display: "var(--nav-divider, flex)" }}></div>

          {/* Desktop Nav */}
          <nav style={{ display: "flex", gap: "2px", alignItems: "center", flex: 1, overflow: "hidden" }}
            className="desktop-nav">
            {navItems.map(item => (
              <NavItem key={item.id} label={item.label} active={page === item.id}
                href={item.href} spa={item.spa}
                accentColor={accentColor} onClick={() => handleNav(item.id)} />
            ))}
          </nav>

          <div style={{ marginLeft: "auto", flexShrink: 0, display: "flex", alignItems: "center", gap: "10px" }}>
            <span className="pw-share-wrap">
              <a href="https://share.sage-news.de" target="_blank" rel="noopener noreferrer"
                className="pw-share-btn" aria-describedby="pw-share-tip">
                Passwort teilen
              </a>
              <span className="pw-share-tip" id="pw-share-tip" role="tooltip">
                Teile sicher ein Passwort mit Deinem Empfänger - verschlüsselte
                Passwortübertragung mit Einmal-Link (kostenfrei)
              </span>
            </span>

            <span className="pw-share-wrap">
              <a href="https://dispatcher-ai.de" target="_blank" rel="noopener noreferrer"
                className="pnd-link" aria-describedby="pnd-tip" aria-label="PLAN and DISPATCH">
                <img src="assets/plan-and-dispatch_icon.png" alt="" width="28" height="28" />
              </a>
              <span className="pw-share-tip pnd-tip-wide" id="pnd-tip" role="tooltip">
                PLAN and DISPATCH – KI-gestütztes, self-hosted Dispatch-Board für
                Beratungs- und Serviceteams: Aufgabenverteilung, Zeiterfassung und
                Projektcontrolling im Browser.
              </span>
            </span>

            {/* Hamburger — mobile only */}
            <button onClick={() => setMenuOpen(o => !o)}
              className="hamburger"
              style={{
                background: "none", border: "none", cursor: "pointer",
                padding: "6px", borderRadius: "8px",
                display: "none", flexDirection: "column", gap: "5px",
                alignItems: "center", justifyContent: "center"
              }}>
              {[0,1,2].map(i => (
                <span key={i} style={{
                  display: "block", width: "22px", height: "2px",
                  background: menuOpen && i === 1 ? "transparent" :
                               menuOpen ? accentColor : "rgba(255,255,255,0.85)",
                  borderRadius: "2px",
                  transition: "transform 0.2s, opacity 0.2s",
                  transform: menuOpen && i === 0 ? "translateY(7px) rotate(45deg)" :
                             menuOpen && i === 2 ? "translateY(-7px) rotate(-45deg)" : "none"
                }}></span>
              ))}
            </button>
          </div>
        </div>

        {/* Mobile dropdown menu */}
        {menuOpen && (
          <nav style={{
            borderTop: "1px solid rgba(255,255,255,0.1)",
            padding: "8px 0 12px",
            display: "flex", flexDirection: "column", gap: "2px"
          }}>
            {navItems.map(item => {
              const isActive = page === item.id;
              const style = {
                background: isActive ? accentColor : "transparent",
                color: isActive ? "#07172f" : "rgba(255,255,255,0.85)",
                fontWeight: isActive ? 700 : 500,
                fontSize: "15px", padding: "11px 14px",
                borderRadius: "8px", border: "none",
                cursor: "pointer", textAlign: "left",
                width: "100%"
              };
              // Wie in der Desktop-Nav: die Bereiche fuehren auf die echte
              // Kategorieseite, alles andere bleibt clientseitig.
              return item.spa ? (
                <button key={item.id} onClick={() => handleNav(item.id)}
                  style={style}>{item.label}</button>
              ) : (
                <a key={item.id} href={item.href}
                  style={{ ...style, display: "block", textDecoration: "none", boxSizing: "border-box" }}
                >{item.label}</a>
              );
            })}
            <a href="https://share.sage-news.de" target="_blank" rel="noopener noreferrer" style={{
              display: "block", padding: "11px 14px", borderRadius: "8px",
              color: "rgba(255,255,255,0.6)", fontSize: "15px", fontWeight: 500,
              textDecoration: "none"
            }}>Passwort teilen ↗</a>
            <a href="https://dispatcher-ai.de" target="_blank" rel="noopener noreferrer" style={{
              display: "block", padding: "11px 14px", borderRadius: "8px",
              color: "rgba(255,255,255,0.6)", fontSize: "15px", fontWeight: 500,
              textDecoration: "none"
            }}>PLAN and DISPATCH ↗</a>
          </nav>
        )}
      </div>

      <style>{`
        .pw-share-btn {
          display: flex; align-items: center;
          background: rgba(255,255,255,0.08);
          border: 1px solid rgba(255,255,255,0.15);
          border-radius: 8px; padding: 6px 12px;
          color: rgba(255,255,255,0.85);
          font-size: 13px; font-weight: 500;
          text-decoration: none; white-space: nowrap;
          transition: background 0.15s;
        }
        .pw-share-btn:hover { background: rgba(255,255,255,0.15); }
        .pw-share-wrap { position: relative; display: inline-flex; }
        .pnd-link {
          display: inline-flex; align-items: center;
          border-radius: 8px; padding: 2px;
          line-height: 0; text-decoration: none;
          opacity: 0.9; transition: opacity 0.15s, background 0.15s;
        }
        .pnd-link:hover { opacity: 1; background: rgba(255,255,255,0.12); }
        .pnd-link img { width: 28px; height: 28px; border-radius: 7px; display: block; }
        .pnd-link:focus-visible ~ .pw-share-tip { opacity: 1; visibility: visible; }
        /* Die Blase faellt aus dem dunklen Header auf den hellen Seiten-
           hintergrund — deshalb deckend statt transparent. */
        .pw-share-tip {
          position: absolute; top: calc(100% + 10px); left: 50%;
          transform: translateX(-50%);
          background: var(--sn-blue-950); color: #fff;
          border: 1px solid rgba(255,255,255,0.15); border-radius: 8px;
          padding: 9px 12px; font-size: 12.5px; font-weight: 500;
          line-height: 1.45; text-align: left;
          /* Der Knopf sitzt rechts im Kopf: die Blase muss umbrechen, sonst
             laeuft sie ueber den Bildschirmrand hinaus. 240px sind schmal
             genug, dass die auf den Knopf zentrierte Blase innen bleibt. */
          width: max-content; max-width: 240px;
          box-shadow: 0 6px 20px rgba(6,27,73,0.28);
          opacity: 0; visibility: hidden; pointer-events: none;
          transition: opacity 0.12s; z-index: 200;
        }
        .pw-share-tip::before {
          content: ""; position: absolute; top: -4px; left: 50%;
          width: 8px; height: 8px; margin-left: -4px;
          background: var(--sn-blue-950);
          border-left: 1px solid rgba(255,255,255,0.15);
          border-top: 1px solid rgba(255,255,255,0.15);
          transform: rotate(45deg);
        }
        /* Laengerer Text als beim Passwort-Knopf, und das Icon sitzt ganz
           aussen: die Blase haengt rechtsbuendig statt zentriert, sonst
           laeuft sie bei schmalen Fenstern ueber den Rand. */
        .pnd-tip-wide {
          max-width: 300px;
          left: auto; right: 0; transform: none;
        }
        .pnd-tip-wide::before { left: auto; right: 12px; margin-left: 0; }
        .pw-share-wrap:hover .pw-share-tip,
        .pw-share-btn:focus-visible ~ .pw-share-tip {
          opacity: 1; visibility: visible;
        }
        @media (max-width: 680px) {
          .desktop-nav { display: none !important; }
          .hamburger { display: flex !important; }
          .pw-share-btn, .pw-share-wrap { display: none !important; }
          .post-grid-featured, .post-grid-regular { grid-template-columns: 1fr !important; }
          .post-grid-featured article { grid-column: 1 !important; }
          .info-hero { flex-direction: column !important; align-items: stretch !important; }
          .info-hero-portrait {
            width: 100% !important;
            min-height: 0 !important;
            padding: 20px 20px 0 !important;
            justify-content: center !important;
          }
          .info-hero-portrait-image {
            max-width: 280px !important;
            width: min(100%, 280px) !important;
            max-height: 220px !important;
            margin: 0 auto !important;
          }
          .info-hero-text {
            flex: 1 1 auto !important;
            padding: 18px 22px 24px !important;
            text-align: center !important;
          }
          .info-hero-glow {
            width: 100% !important;
            height: 180px !important;
            left: 0 !important;
            top: 0 !important;
            bottom: auto !important;
            background: radial-gradient(circle at 50% 35%, rgba(255,210,46,0.16) 0%, transparent 68%) !important;
          }
        }
      `}</style>
    </header>
  );
}

function NavItem({ label, active, accentColor, onClick, href, spa = false }) {
  const [hovered, setHovered] = useState(false);
  const highlight = active || hovered;
  // Die Nav bestand frueher aus <button>. Buttons erben font-family nicht und
  // rendern in Chrome per UA-Stylesheet in Arial. Damit der Wechsel auf echte
  // Links das Schriftbild nicht veraendert, wird Arial hier explizit gesetzt.
  const style = {
    background: highlight ? accentColor : "transparent",
    color: highlight ? "#07172f" : "rgba(255,255,255,0.72)",
    fontFamily: "Arial, sans-serif",
    fontWeight: highlight ? 700 : 500,
    fontSize: "13.5px",
    padding: "7px 13px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    whiteSpace: "nowrap",
    transition: "background 0.15s, color 0.15s"
  };
  const handlers = {
    onMouseEnter: () => setHovered(true),
    onMouseLeave: () => setHovered(false)
  };
  if (href) {
    // Ohne spa laeuft der Klick normal weiter — der Browser folgt dem href.
    return (
      <a
        href={href}
        onClick={spa ? (e => { e.preventDefault(); onClick(); }) : undefined}
        {...handlers}
        style={{ ...style, display: "inline-block", textDecoration: "none" }}
      >{label}</a>
    );
  }
  return <button onClick={onClick} {...handlers} style={style}>{label}</button>;
}

// ── HERO BANNER ────────────────────────────────────────────────────────────
function HeroBanner({ headerStyle }) {
  if (headerStyle !== "banner") return null;
  return (
    <div style={{ maxWidth: "1140px", margin: "0 auto", padding: "24px 20px 0" }}>
      <div style={{ borderRadius: "16px", overflow: "hidden" }}>
        <img src="assets/sage-news_banner.png" alt="sage news – Wissen, was wirklich zählt."
          style={{ width: "100%", display: "block", maxHeight: "250px", objectFit: "cover", objectPosition: "center" }} />
      </div>
    </div>
  );
}

// ── CATEGORY PAGE HEADER ───────────────────────────────────────────────────
// ── POST CARD ──────────────────────────────────────────────────────────────
function PostCard({ post, featured, onClick, tweaks }) {
  const [hovered, setHovered] = useState(false);
  const radius = (tweaks?.cardRadius ?? 14) + "px";
  const href = post.permalink ? `/${post.permalink}/` : null;
  const cardProps = href ? {
    as: "a",
    href,
    onClick: undefined
  } : {
    as: "article",
    href: undefined,
    onClick
  };
  const CardTag = cardProps.as;
  if (featured) {
    return (
      <CardTag href={cardProps.href} onClick={cardProps.onClick}
        onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)}
        style={{
          display: "block",
          textDecoration: "none",
          background: "linear-gradient(135deg, var(--sn-blue-950), var(--sn-blue-800))",
          borderRadius: radius, padding: "28px", cursor: "pointer",
          transition: "transform 0.18s, box-shadow 0.18s",
          transform: hovered ? "translateY(-3px)" : "none",
          boxShadow: hovered ? "0 12px 40px rgba(6,27,73,0.22)" : "0 4px 16px rgba(6,27,73,0.10)",
          gridColumn: "span 2", position: "relative", overflow: "hidden", color: "white"
        }}>
        <div style={{
          position: "absolute", top: "-40px", right: "-40px",
          width: "200px", height: "200px",
          background: "radial-gradient(circle, rgba(56,169,245,0.15) 0%, transparent 70%)",
          borderRadius: "50%", pointerEvents: "none"
        }}></div>
        <div style={{ display: "flex", gap: "8px", marginBottom: "12px", flexWrap: "wrap" }}>
          <CategoryBadge category={post.category} />
          <TagBadge tag={post.tag} />
          <span style={{
            display: "inline-block", background: tweaks?.accentColor ?? "#ffc82e",
            color: "#07172f", fontWeight: 700, fontSize: "11px",
            padding: "2px 10px", borderRadius: "999px"
          }}>Featured</span>
        </div>
        <h2 style={{ fontSize: "20px", fontWeight: 800, lineHeight: 1.3, marginBottom: "10px" }}>{post.title}</h2>
        <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.76)", lineHeight: 1.6, marginBottom: "18px" }}>{post.summary}</p>
        <div style={{ display: "flex", gap: "14px", alignItems: "center" }}>
          <span style={{ fontSize: "12px", color: "rgba(255,255,255,0.5)" }}>{post.date}</span>
          <span style={{ fontSize: "12px", color: "rgba(255,255,255,0.5)" }}>· {post.readTime}</span>
          <span style={{ marginLeft: "auto", fontSize: "13px", fontWeight: 700, color: tweaks?.accentColor ?? "#ffc82e" }}>Weiterlesen →</span>
        </div>
      </CardTag>
    );
  }
  return (
    <CardTag href={cardProps.href} onClick={cardProps.onClick}
      onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)}
      style={{
        display: "block",
        textDecoration: "none",
        background: "white", border: "1.5px solid var(--sn-border)",
        borderRadius: radius, padding: "22px", cursor: "pointer",
        transition: "transform 0.18s, box-shadow 0.18s, border-color 0.18s",
        transform: hovered ? "translateY(-2px)" : "none",
        boxShadow: hovered ? "0 8px 28px rgba(6,27,73,0.10)" : "0 1px 4px rgba(6,27,73,0.05)",
        borderColor: hovered ? "var(--sn-blue-400)" : "var(--sn-border)"
      }}>
      <div style={{ display: "flex", gap: "6px", marginBottom: "10px", flexWrap: "wrap" }}>
        <CategoryBadge category={post.category} small />
        <TagBadge tag={post.tag} />
      </div>
      <h3 style={{ fontSize: "15px", fontWeight: 700, lineHeight: 1.35, marginBottom: "8px" }}>{post.title}</h3>
      <p style={{ fontSize: "13px", color: "var(--sn-muted)", lineHeight: 1.6, marginBottom: "14px" }}>{post.summary}</p>
      <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
        <span style={{ fontSize: "12px", color: "var(--sn-muted)" }}>{post.date}</span>
        <span style={{ fontSize: "12px", color: "var(--sn-muted)" }}>· {post.readTime}</span>
        <span style={{ marginLeft: "auto", fontSize: "12px", fontWeight: 700, color: "var(--sn-blue-600)" }}>Weiterlesen →</span>
      </div>
    </CardTag>
  );
}

function PostGrid({ posts, tweaks, onReadPost, onlyNewestFeatured = false }) {
  const featuredPosts = posts.filter(p => isFeaturedActive(p));
  const featured = onlyNewestFeatured ? featuredPosts.slice(0, 1) : featuredPosts;
  const featuredIds = new Set(featured.map(p => p.id));
  const regular  = posts.filter(p => !featuredIds.has(p.id));
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {featured.length > 0 && (
        <div className="post-grid-featured" style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "16px" }}>
          {featured.map(p => <PostCard key={p.id} post={p} featured tweaks={tweaks} onClick={!p.permalink ? () => onReadPost(p) : undefined} />)}
        </div>
      )}
      <div className="post-grid-regular" style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "16px" }}>
        {regular.map(p => <PostCard key={p.id} post={p} tweaks={tweaks} onClick={!p.permalink ? () => onReadPost(p) : undefined} />)}
      </div>
    </div>
  );
}

// ── POST DETAIL ────────────────────────────────────────────────────────────
function PostDetail({ post, onBack, tweaks }) {
  const hasBody = post.body && post.body.trim().length > 0;
  const html = hasBody ? marked.parse(post.body) : null;
  return (
    <div style={{ maxWidth: "760px" }}>
      <button onClick={onBack} style={{
        background: "none", border: "none", cursor: "pointer",
        fontSize: "14px", color: "var(--sn-blue-600)", fontWeight: 600,
        padding: "0 0 20px", display: "flex", alignItems: "center", gap: "6px"
      }}>← Zurück zur Übersicht</button>

      <div style={{
        background: "linear-gradient(135deg, var(--sn-blue-950), var(--sn-blue-800))",
        borderRadius: "14px", padding: "32px", color: "white", marginBottom: "24px"
      }}>
        <div style={{ display: "flex", gap: "8px", marginBottom: "14px", flexWrap: "wrap" }}>
          <CategoryBadge category={post.category} />
          <TagBadge tag={post.tag} />
        </div>
        <h1 style={{ fontSize: "22px", fontWeight: 900, lineHeight: 1.3, marginBottom: "12px" }}>{post.title}</h1>
        <div style={{ display: "flex", gap: "16px", fontSize: "13px", color: "rgba(255,255,255,0.55)" }}>
          <span>{post.date}</span>
          <span>· {post.readTime} Lesezeit</span>
        </div>
      </div>

      <div style={{ background: "white", border: "1.5px solid var(--sn-border)", borderRadius: "14px", padding: "32px" }}>
        {post.summary && (
          <div style={{
            background: "var(--sn-blue-100)", borderRadius: "10px",
            padding: "16px 20px", marginBottom: "24px",
            borderLeft: "3px solid var(--sn-blue-600)"
          }}>
            <div style={{ fontWeight: 800, fontSize: "11px", color: "var(--sn-blue-800)", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.06em" }}>Kurzfazit</div>
            <p style={{ fontSize: "14px", lineHeight: 1.6 }}>{post.summary}</p>
          </div>
        )}

        {hasBody ? (
          <div className="prose" dangerouslySetInnerHTML={{ __html: html }} />
        ) : (
          <p style={{ fontSize: "15px", color: "var(--sn-muted)", lineHeight: 1.7 }}>
            Noch kein Artikeltext vorhanden. Füge eine Markdown-Datei mit dem Body-Inhalt in deinem GitHub-Repo hinzu.
          </p>
        )}
      </div>
    </div>
  );
}

// ── SIDEBAR ────────────────────────────────────────────────────────────────
function Sidebar({ posts, tweaks }) {
  if (!tweaks?.showSidebar) return null;
  const recent = posts.slice(0, 4);
  return (
    <aside style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
      <div style={{
        background: "linear-gradient(135deg, var(--sn-blue-900), var(--sn-blue-700))",
        borderRadius: "14px", padding: "20px", color: "white"
      }}>
        <div style={{ fontWeight: 800, fontSize: "14px", marginBottom: "6px" }}>Newsletter</div>
        <p style={{ fontSize: "13px", color: "rgba(255,255,255,0.72)", lineHeight: 1.5, marginBottom: "12px" }}>
          Neue Artikel direkt ins Postfach.
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <input placeholder="deine@email.de" style={{
            padding: "9px 12px", borderRadius: "8px", border: "none",
            fontSize: "13px", background: "rgba(255,255,255,0.12)", color: "white", outline: "none"
          }} />
          <button style={{
            padding: "9px", borderRadius: "8px", border: "none",
            background: tweaks?.accentColor ?? "#ffc82e",
            color: "#07172f", fontWeight: 800, fontSize: "13px", cursor: "pointer"
          }}>Anmelden</button>
        </div>
      </div>

      <div style={{ background: "white", border: "1.5px solid var(--sn-border)", borderRadius: "14px", padding: "18px" }}>
        <div style={{ fontWeight: 800, fontSize: "13px", marginBottom: "12px" }}>Zuletzt veröffentlicht</div>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          {recent.map(p => (
            <div key={p.id}>
              <CategoryBadge category={p.category} small />
              <div style={{ fontSize: "13px", fontWeight: 600, lineHeight: 1.3, marginTop: "4px" }}>{p.title}</div>
              <div style={{ fontSize: "11px", color: "var(--sn-muted)", marginTop: "2px" }}>{p.date}</div>
            </div>
          ))}
        </div>
      </div>
    </aside>
  );
}

// ── SYSTEMCHECK ────────────────────────────────────────────────────────────
function SystemcheckPage() {
  const [srcdoc, setSrcdoc] = useState('');
  useEffect(() => {
    fetch('systemcheck.html')
      .then(r => r.text())
      .then(html => {
        // Inject base tag so relative paths (assets/, etc.) resolve correctly
        const base = `<base href="${window.location.href.replace(/[^/]*$/, '')}">`;
        const fixed = html.replace('<head>', '<head>' + base);
        setSrcdoc(fixed);
      })
      .catch(() => setSrcdoc('<p style="padding:40px;font-family:sans-serif;color:#555">Systemcheck konnte nicht geladen werden.</p>'));
  }, []);
  return (
    <div style={{ width: "100%" }}>
      {srcdoc ? (
        <iframe
          srcDoc={srcdoc}
          style={{
            width: "100%",
            height: "calc(100vh - 100px)",
            border: "none",
            borderRadius: "14px",
            display: "block"
          }}
          title="Sage 100 Systemvoraussetzungen Checkliste"
        ></iframe>
      ) : (
        <div style={{ padding: "40px", textAlign: "center", color: "var(--sn-muted)", fontSize: "14px" }}>
          Systemcheck wird geladen…
        </div>
      )}
    </div>
  );
}

// ── INFO PAGE ──────────────────────────────────────────────────────────────
function InfoPage({ postsSource }) {
  const heroBtnStyle = {
    display: "inline-flex",
    alignItems: "center",
    gap: "8px",
    background: "rgba(255,255,255,0.12)",
    color: "white",
    border: "1px solid rgba(255,255,255,0.18)",
    borderRadius: "999px",
    padding: "8px 14px",
    fontSize: "12px",
    fontWeight: 700,
    textDecoration: "none"
  };
  return (
    <div style={{ maxWidth: "640px" }}>
      {/* Hero card with portrait */}
      <div className="info-hero" style={{
        background: "linear-gradient(135deg, var(--sn-blue-950), var(--sn-blue-800))",
        borderRadius: "14px", marginBottom: "20px", overflow: "hidden",
        display: "flex", alignItems: "stretch", gap: "0", position: "relative", minHeight: "200px",
        flexWrap: "wrap"
      }}>
        {/* Portrait */}
        <div className="info-hero-portrait" style={{
          flexShrink: 0, width: "220px", minHeight: "200px",
          position: "relative", lineHeight: 0,
          display: "flex", alignItems: "stretch", justifyContent: "center",
          background: "linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0))",
          overflow: "hidden"
        }}>
          <img className="info-hero-portrait-image" src="assets/rene_character.png" alt="René Münz"
            style={{
              width: "100%", height: "100%",
              objectFit: "cover", objectPosition: "center top",
              display: "block"
            }} />
        </div>

        {/* Text */}
        <div className="info-hero-text" style={{ padding: "28px 28px 28px 20px", flex: "1 1 320px", minWidth: "0" }}>
          <div style={{
            display: "inline-block",
            background: "rgba(255,255,255,0.12)",
            border: "1px solid rgba(255,255,255,0.2)",
            borderRadius: "999px", padding: "3px 12px",
            fontSize: "11px", fontWeight: 700, letterSpacing: "0.06em",
            color: "rgba(255,255,255,0.8)", marginBottom: "12px",
            textTransform: "uppercase"
          }}>Über mich</div>
          <h1 style={{ fontSize: "24px", fontWeight: 900, color: "white", marginBottom: "8px", lineHeight: 1.2 }}>René Münz</h1>
          <p style={{ fontSize: "13px", color: "rgba(255,255,255,0.65)", lineHeight: 1.6, marginBottom: "14px" }}>
            Projektmanager<br/>Sage-Spezialist
          </p>
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            <a
              href="https://www.linkedin.com/in/rene-m%C3%BCnz-77912a102/"
              target="_blank"
              rel="noopener noreferrer"
              style={heroBtnStyle}
            >
              LinkedIn-Profil ansehen
            </a>
            <a
              href="https://dispatcher-ai.de"
              target="_blank"
              rel="noopener noreferrer"
              style={heroBtnStyle}
            >
              Plan and Dispatch AI
            </a>
          </div>
        </div>

        {/* Decorative glow behind portrait */}
        <div className="info-hero-glow" style={{
          position: "absolute", bottom: 0, left: 0,
          width: "220px", height: "220px",
          background: "radial-gradient(circle at 50% 100%, rgba(255,210,46,0.12) 0%, transparent 70%)",
          pointerEvents: "none"
        }}></div>
      </div>
      <div style={{ background: "white", border: "1.5px solid var(--sn-border)", borderRadius: "14px", padding: "26px", marginBottom: "16px" }}>
        <h2 style={{ fontSize: "15px", fontWeight: 800, marginBottom: "10px" }}>Über diese Seite</h2>
        <p style={{ fontSize: "14px", color: "var(--sn-muted)", lineHeight: 1.7, marginBottom: "10px" }}>
          <strong style={{ color: "var(--sn-ink)" }}>sage news</strong> ist eine private Wissensplattform rund um die Sage-Produktwelt in Deutschland.
          Schwerpunkt: Sage 100, Sage X3, Sage Operations – mit Blick auf Sage Intact.
        </p>
        <p style={{ fontSize: "14px", color: "var(--sn-muted)", lineHeight: 1.7 }}>
          Kompakte Berichte, technische Einordnungen und Praxiserfahrungen aus dem Projektalltag.
          Kein Marketing, keine Werbung – nur das, was wirklich zählt.
        </p>
      </div>
      <div style={{ background: "white", border: "1.5px solid var(--sn-border)", borderRadius: "14px", padding: "26px", marginBottom: "16px" }}>
        <h2 style={{ fontSize: "15px", fontWeight: 800, marginBottom: "12px" }}>Produkte im Fokus</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {[
            { name: "Sage 100",        desc: "ERP für den deutschen Mittelstand",                     cat: "Sage 100" },
            { name: "Sage X3",         desc: "ERP für internationale Unternehmensstrukturen",         cat: "Sage X3" },
            { name: "Sage Operations", desc: "Fertigungsplanung, MES & Produktionssteuerung",         cat: "Sage Operations" },
            { name: "Sage Intact",     desc: "Cloud-ERP – perspektivisch für den deutschen Markt",   cat: "Sage Intact" }
          ].map(item => (
            <div key={item.name} style={{
              display: "flex", alignItems: "center", gap: "10px",
              padding: "10px 12px", borderRadius: "9px",
              background: "var(--sn-bg)", border: "1px solid var(--sn-border)"
            }}>
              <CategoryBadge category={item.cat} />
              <span style={{ fontSize: "13px", color: "var(--sn-muted)" }}>{item.desc}</span>
            </div>
          ))}
        </div>
      </div>
      <GitHubSetupHint source={postsSource} />
    </div>
  );
}

// ── GITHUB INFO BOX ────────────────────────────────────────────────────────
function GitHubSetupHint({ source }) {
  if (source === "github") return null;
  return (
    <details style={{
      background: "white", border: "1.5px solid var(--sn-border)",
      borderRadius: "12px", padding: "12px 16px", marginTop: "20px"
    }}>
      <summary style={{
        cursor: "pointer", listStyle: "none", fontSize: "12px", color: "var(--sn-muted)",
        display: "flex", alignItems: "center", gap: "8px", fontWeight: 600
      }}>
        <span style={{
          width: "24px", height: "24px", borderRadius: "6px",
          background: "var(--sn-blue-100)",
          display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: "13px"
        }}>📁</span>
        Hinweis zu den Quelldaten
      </summary>
      <div style={{ paddingTop: "10px" }}>
        <div style={{ fontWeight: 700, fontSize: "13px", marginBottom: "4px", color: "var(--sn-ink)" }}>
          Beispieldaten – GitHub noch nicht konfiguriert
        </div>
        <p style={{ fontSize: "12px", color: "var(--sn-muted)", lineHeight: 1.6, margin: 0 }}>
          Trage in <code style={{ background: "var(--sn-blue-100)", padding: "1px 5px", borderRadius: "3px" }}>GH_CONFIG</code> deinen GitHub-Benutzernamen und Repo-Namen ein.
          Lege dann Markdown-Dateien im Ordner <code style={{ background: "var(--sn-blue-100)", padding: "1px 5px", borderRadius: "3px" }}>posts/</code> ab – sie erscheinen automatisch hier.
        </p>
      </div>
    </details>
  );
}

// ── APP ────────────────────────────────────────────────────────────────────
function App() {
  const [tweaks, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [page, setPage] = useState("home");
  const [selectedPost, setSelectedPost] = useState(null);
  const [posts, setPosts] = useState([]);
  const [postsSource, setPostsSource] = useState("github");
  const [loading, setLoading] = useState(false);
  const [currentSlug, setCurrentSlug] = useState(() => {
    const parts = window.location.pathname.split("/").filter(Boolean);
    return parts.length === 1 ? parts[0] : null;
  });

  const routeMap = {
    home: "home",
    systemcheck: "systemcheck",
    info: "info"
  };

  // Alte Lesezeichen auf die frueheren Bereichsansichten. Sie sollen nicht
  // stillschweigend auf der Startseite landen, sondern auf der Seite, die den
  // Bereich heute zeigt.
  const LEGACY_CATEGORY_HASHES = {
    sage100: "/kategorie/sage-100/",
    sagex3: "/kategorie/sage-x3/",
    operations: "/kategorie/sage-operations/"
  };

  function getPageFromHash() {
    const hash = (window.location.hash || "").replace(/^#/, "").trim().toLowerCase();
    return routeMap[hash] || "home";
  }

  // Load posts from GitHub on mount
  useEffect(() => {
    setLoading(true);
    loadPostsFromManifest().then(({ posts: loaded, source }) => {
      setPosts(loaded);
      setPostsSource(source);
      if (currentSlug) {
        const matched = loaded.find(p => p.permalink === currentSlug || p.slug === currentSlug);
        setSelectedPost(matched || null);
      }
      setLoading(false);
    }).catch(() => {
      setPosts([]);
      setPostsSource("github");
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    const syncFromHash = () => {
      const hash = (window.location.hash || "").replace(/^#/, "").trim().toLowerCase();
      const legacy = LEGACY_CATEGORY_HASHES[hash];
      if (legacy) { window.location.replace(legacy); return; }
      setPage(getPageFromHash());
      if (!currentSlug) setSelectedPost(null);
    };
    syncFromHash();
    window.addEventListener("hashchange", syncFromHash);
    return () => window.removeEventListener("hashchange", syncFromHash);
  }, [currentSlug]);

  // Nur noch die Startseite hat einen Feed in der App — die Bereiche liegen
  // unter /kategorie/. postsPerPage gilt damit ausschliesslich hier.
  const displayedPosts = posts.slice(0, tweaks?.postsPerPage ?? TWEAK_DEFAULTS.postsPerPage);
  const showFeed = page === "home";

  function navTo(p) {
    setSelectedPost(null);
    setCurrentSlug(null);
    setPage(p);
    const targetHash = p === "home" ? "" : `#${p}`;
    const basePath = "/";
    if (window.location.hash !== targetHash || window.location.pathname !== basePath) {
      history.replaceState(null, "", basePath + (targetHash || ""));
    }
    window.scrollTo({ top: 0 });
  }

  function onReadPost(post) {
    setSelectedPost(post);
    setCurrentSlug(post.permalink || post.slug || null);
    if (post.permalink) {
      history.pushState(null, "", `/${post.permalink}/`);
    }
    window.scrollTo({ top: 0 });
  }

  return (
    <div>
      <Header page={page} setPage={navTo} accentColor={tweaks?.accentColor ?? TWEAK_DEFAULTS.accentColor} />

      {page === "home" && !selectedPost && <HeroBanner headerStyle={tweaks?.headerStyle ?? "banner"} />}

      <div style={{ maxWidth: "1140px", margin: "0 auto", padding: "24px 20px 64px" }}>

        {loading ? (
          <div style={{ textAlign: "center", padding: "60px 0", color: "var(--sn-muted)", fontSize: "14px" }}>
            Beiträge werden geladen…
          </div>
        ) : selectedPost ? (
          <div style={{ display: "grid", gridTemplateColumns: tweaks?.showSidebar ? "1fr 280px" : "1fr", gap: "24px", alignItems: "start" }}>
            <PostDetail post={selectedPost} onBack={() => navTo("home")} tweaks={tweaks} />
            <Sidebar posts={posts} tweaks={tweaks} />
          </div>
        ) : showFeed ? (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: tweaks?.showSidebar ? "1fr 280px" : "1fr", gap: "24px", alignItems: "start" }}>
              <PostGrid posts={displayedPosts} tweaks={tweaks} onlyNewestFeatured onReadPost={onReadPost} />
              <Sidebar posts={posts} tweaks={tweaks} />
            </div>
          </div>
        ) : page === "systemcheck" ? (
          <SystemcheckPage tweaks={tweaks} />
        ) : page === "info" ? (
          <InfoPage postsSource={postsSource} />
        ) : null}
      </div>

      {/* Footer */}
      <footer style={{ borderTop: "1.5px solid var(--sn-border)", background: "white", padding: "20px" }}>
        <div style={{ maxWidth: "1140px", margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "12px" }}>
          <div style={{ lineHeight: 0 }}>
            <img src="assets/sage-news_logo_3.png" alt="sage news" style={{ height: "36px", width: "auto", display: "block", mixBlendMode: "lighten" }} />
          </div>
          <div style={{ display: "flex", gap: "20px", alignItems: "center", flexWrap: "wrap" }}>
            <button onClick={() => navTo("info")} style={{ background: "none", border: "none", cursor: "pointer", fontSize: "13px", color: "var(--sn-muted)" }}>Info</button>
            <button onClick={() => navTo("systemcheck")} style={{ background: "none", border: "none", cursor: "pointer", fontSize: "13px", color: "var(--sn-muted)" }}>Systemcheck</button>
            <a href="impressum/" style={{ fontSize: "13px", color: "var(--sn-muted)", textDecoration: "none" }}>Impressum</a>
            <a href="datenschutz/" style={{ fontSize: "13px", color: "var(--sn-muted)", textDecoration: "none" }}>Datenschutz</a>
            <span style={{ fontSize: "12px", color: "var(--sn-muted)" }}>© 2026 René Münz</span>
          </div>
        </div>
      </footer>

      {/* Tweaks Panel */}
      <TweaksPanel>
        <TweakSection label="Design" />
        <TweakColor label="Akzentfarbe" value={tweaks?.accentColor ?? "#ffc82e"} onChange={v => setTweak("accentColor", v)} />
        <TweakSlider label="Card-Radius" value={tweaks?.cardRadius ?? 14} min={0} max={24} step={2} onChange={v => setTweak("cardRadius", v)} />
        <TweakSection label="Layout" />
        <TweakRadio label="Header" value={tweaks?.headerStyle ?? "banner"}
          options={["banner", "compact"]} onChange={v => setTweak("headerStyle", v)} />
        <TweakToggle label="Sidebar" value={tweaks?.showSidebar ?? false} onChange={v => setTweak("showSidebar", v)} />
        <TweakSlider label="Beiträge" value={tweaks?.postsPerPage ?? 8} min={2} max={8} step={1} onChange={v => setTweak("postsPerPage", v)} />
      </TweaksPanel>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
