import { useEffect, useState } from "react";
import { Bell, ChevronRight, Home, Leaf, Menu, X } from "lucide-react";
import { DashboardView } from "./DashboardView";
import { WorkspaceViews } from "./WorkspaceViews";

type SelectedLocation = { locality: string; latitude: number; longitude: number; timezone: string };
const navItems = ["Dashboard", "Environment", "Skin", "Routine", "Exposure", "Insights", "Devices", "Profile", "Settings"];
const fallbackLocation: SelectedLocation = { locality: "Bengaluru", latitude: 12.9716, longitude: 77.5946, timezone: "Asia/Kolkata" };

export function App() {
  const [active, setActive] = useState(() => localStorage.getItem("atmo-photo-analysis-complete") ? "Dashboard" : "Skin");
  const [menuOpen, setMenuOpen] = useState(false);
  const [location, setLocation] = useState<SelectedLocation>(() => { try { return JSON.parse(localStorage.getItem("atmo-location") || "null") || fallbackLocation; } catch { return fallbackLocation; } });
  const [locationOpen, setLocationOpen] = useState(false);
  const [locations, setLocations] = useState<SelectedLocation[]>([]);
  const [alertsOpen, setAlertsOpen] = useState(false);
  useEffect(() => { fetch("http://127.0.0.1:8000/api/location/options").then((response) => response.json()).then(setLocations).catch(() => setLocations([fallbackLocation])); }, []);
  function chooseLocation(next: SelectedLocation) { setLocation(next); localStorage.setItem("atmo-location", JSON.stringify(next)); setLocationOpen(false); }
  function navigate(view: string) { setActive(view); setMenuOpen(false); }
  function photoAnalyzed() { localStorage.setItem("atmo-photo-analysis-complete", "true"); setActive("Dashboard"); }
  return <div className="app-shell">
    <aside className={menuOpen ? "sidebar sidebar-open" : "sidebar"}><div className="brand-lockup"><div className="brand-mark"><Leaf size={18} strokeWidth={2.5} /></div><span>ATMO DERMA</span><button className="icon-button mobile-close" onClick={() => setMenuOpen(false)} aria-label="Close navigation"><X size={18} /></button></div><div className="sidebar-context"><span className="eyebrow">YOUR SKIN ENVIRONMENT</span><strong>Good morning, Alex</strong><button className="location location-button" onClick={() => setLocationOpen(true)}><Home size={13} /> {location.locality} · choose location</button></div><nav aria-label="Primary navigation">{navItems.map((item, index) => <button className={active === item ? "nav-item active" : "nav-item"} key={item} onClick={() => navigate(item)}><span className="nav-number">{String(index + 1).padStart(2, "0")}</span>{item}</button>)}</nav><div className="sidebar-footer"><div className="demo-pill"><span className="pulse" /> Demo sensor data</div><button className="profile-link" onClick={() => navigate("Profile")}><span className="avatar">AS</span><span><strong>Alex Shah</strong><small>Personal profile</small></span><ChevronRight size={15} /></button></div></aside>
    <main className="main-content"><header className="topbar"><button className="icon-button menu-trigger" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu size={21} /></button><div className="breadcrumb"><span>Atmo Derma</span><ChevronRight size={14} /><strong>{active}</strong></div><div className="topbar-actions"><span className="live-status"><span className="pulse" /> Live conditions</span><button className="icon-button" onClick={() => setAlertsOpen(true)} aria-label="View alerts"><Bell size={18} /></button></div></header><div className="content-wrap">{active === "Dashboard" ? <DashboardView location={location} onLocation={() => setLocationOpen(true)} onNavigate={navigate} /> : <WorkspaceViews active={active} location={location} onNavigate={navigate} onPhotoAnalyzed={photoAnalyzed} />}</div></main>
    {locationOpen && <div className="modal-backdrop" role="presentation"><section className="dialog" role="dialog" aria-modal="true" aria-labelledby="location-title"><div className="panel-heading"><div><span className="eyebrow">LOCATION CONTEXT</span><h2 id="location-title">Where are you today?</h2></div><button className="icon-button" onClick={() => setLocationOpen(false)} aria-label="Close location chooser"><X size={18} /></button></div><p className="panel-copy">Choose an approximate locality. Precise location history is not stored by this demo.</p><div className="location-options">{locations.map((option) => <button className={option.locality === location.locality ? "location-option selected" : "location-option"} key={option.locality} onClick={() => chooseLocation(option)}><span><strong>{option.locality}</strong><small>{option.timezone}</small></span><ChevronRight size={16} /></button>)}</div></section></div>}
    {alertsOpen && <div className="modal-backdrop" role="presentation"><section className="dialog" role="dialog" aria-modal="true" aria-labelledby="alerts-title"><div className="panel-heading"><div><span className="eyebrow">CONTEXTUAL ALERT</span><h2 id="alerts-title">UV is currently elevated.</h2></div><button className="icon-button" onClick={() => setAlertsOpen(false)} aria-label="Close alerts"><X size={18} /></button></div><p className="panel-copy">Consider your normal broad-spectrum sun protection routine and reduce prolonged direct exposure where practical.</p><button className="primary-button" onClick={() => setAlertsOpen(false)}>Understood</button></section></div>}
  </div>;
}
