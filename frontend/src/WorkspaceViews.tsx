import { useEffect, useState } from "react";
import {
  Activity,
  AirVent,
  ArrowUpRight,
  Check,
  ChevronRight,
  CircleHelp,
  CloudSun,
  Droplets,
  Gauge,
  Leaf,
  LockKeyhole,
  Moon,
  Radio,
  Save,
  Settings2,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  Sun,
  Thermometer,
  UserRound,
  Wind,
} from "lucide-react";

type SelectedLocationContext = { locality: string; latitude: number; longitude: number };
type WorkspaceViewsProps = { active: string; onNavigate: (view: string) => void; location?: SelectedLocationContext; onPhotoAnalyzed?: () => void };

type ApiState = { loading: boolean; error: boolean };

function useApi<T>(path: string, fallback: T) {
  const [data, setData] = useState<T>(fallback);
  const [state, setState] = useState<ApiState>({ loading: true, error: false });
  useEffect(() => {
    fetch(`http://127.0.0.1:8000${path}`)
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then((value: T) => { setData(value); setState({ loading: false, error: false }); })
      .catch(() => setState({ loading: false, error: true }));
  }, [path]);
  return { data, ...state };
}

function ViewHeader({ eyebrow, title, copy, action }: { eyebrow: string; title: string; copy: string; action?: React.ReactNode }) {
  return <div className="view-header"><div><span className="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{copy}</p></div>{action}</div>;
}

function StatTile({ label, value, detail, tone = "neutral" }: { label: string; value: string; detail: string; tone?: string }) {
  return <article className={`stat-tile ${tone}`}><span className="metric-label">{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}

export function WorkspaceViews({ active, onNavigate, location, onPhotoAnalyzed }: WorkspaceViewsProps) {
  if (active === "Environment") return <EnvironmentView />;
  if (active === "Skin") return <SkinView onNavigate={onNavigate} location={location} onPhotoAnalyzed={onPhotoAnalyzed} />;
  if (active === "Routine") return <RoutineView />;
  if (active === "Exposure") return <ExposureView />;
  if (active === "Insights") return <InsightsView />;
  if (active === "Devices") return <DevicesView />;
  if (active === "Profile") return <ProfileView />;
  return <SettingsView />;
}

function EnvironmentView() {
  const { data, loading, error } = useApi("/api/environment/current", { temperature: 29, humidity: 31, uv_index: 7.2, pm25: 12, aqi: 42, wind_speed: 14, data_quality: "SIMULATED" });
  const [showIndoor, setShowIndoor] = useState(false);
  return <>
    <ViewHeader eyebrow="OUTDOOR ENVIRONMENT" title="Read the air around you." copy="Current conditions are translated into skin-relevant signals, with uncertainty kept visible." action={<span className="data-quality"><span className="pulse" /> {data.data_quality}</span>} />
    {error && <div className="error-banner">Live environmental data is unavailable. Showing the last available demo snapshot.</div>}
    <div className="stat-grid">{loading ? <LoadingTiles count={4} /> : <><StatTile label="Temperature" value={`${data.temperature}°`} detail="Feels like 31°" tone="warm" /><StatTile label="Humidity" value={`${data.humidity}%`} detail="Below your recent norm" tone="dry" /><StatTile label="UV index" value={`${data.uv_index}`} detail="High exposure" tone="alert" /><StatTile label="Air quality" value={`${data.aqi}`} detail={`PM2.5 ${data.pm25}`} tone="good" /></>}</div>
    <section className="view-grid"><article className="wide-panel chart-panel"><div className="panel-heading"><div><span className="eyebrow">TODAY'S RANGE</span><h3>Conditions through the day</h3></div><CloudSun size={20} /></div><div className="chart-area"><div className="chart-line uv-line" /><div className="chart-line humidity-line" /><div className="chart-axis"><span>06:00</span><span>10:00</span><span>14:00</span><span>18:00</span><span>22:00</span></div></div><div className="legend"><span><i className="dot coral" /> UV index</span><span><i className="dot green" /> Humidity</span></div></article><article className="side-panel"><span className="section-kicker"><Gauge size={15} /> {showIndoor ? "INDOOR DEMO" : "AIR QUALITY"}</span><div className="big-reading">{showIndoor ? "46%" : `${data.aqi}`} <small>{showIndoor ? "humidity" : "AQI"}</small></div><p>{showIndoor ? "The demo indoor sensor currently reports 46% humidity and simulated readings. Indoor is not automatically safer." : "Air quality is currently good based on available data. Indoor conditions should be judged from actual sensor readings."}</p><button className="text-button" onClick={() => setShowIndoor(!showIndoor)}>{showIndoor ? "View outdoor air" : "Compare indoor air"} <ChevronRight size={15} /></button></article></section>
  </>;
}

function SkinView({ onNavigate, location = { locality: "Bengaluru", latitude: 12.9716, longitude: 77.5946 }, onPhotoAnalyzed }: Pick<WorkspaceViewsProps, "onNavigate" | "location" | "onPhotoAnalyzed">) {
  const trend = useApi("/api/users/demo-user-001/skin-trends", { trend: "INSUFFICIENT_DATA", explanation: "Your personal baseline is still forming.", observation_count: 0 });
  const state = useApi("/api/users/demo-user-001/skin-state", null as { dryness_indicator?: number; redness_indicator?: number; user_reported_irritation?: string } | null);
  return <><ViewHeader eyebrow="PERSONAL SKIN TRACKING" title="Your skin, over time." copy="Upload a current photo to unlock the full analysis. The image supplies visual indicators; live environment data supplies the surrounding context." action={<button className="outline-button" onClick={() => onNavigate("Dashboard")}><ArrowUpRight size={15} /> Quick check-in</button>} /><div className="stat-grid"><StatTile label="Dryness indicator" value={state.data?.dryness_indicator ? `${state.data.dryness_indicator}` : "—"} detail="Visual wellness indicator" tone="dry" /><StatTile label="Redness indicator" value={state.data?.redness_indicator ? `${state.data.redness_indicator}` : "—"} detail="Not a diagnosis" tone="neutral" /><StatTile label="Irritation" value={state.data?.user_reported_irritation || "—"} detail="Most recent check-in" tone="neutral" /><StatTile label="Observations" value={`${trend.data.observation_count}`} detail="Personal history" tone="good" /></div><section className="view-grid"><article className="wide-panel"><div className="panel-heading"><div><span className="eyebrow">PERSONAL BASELINE</span><h3>{trend.data.trend.replaceAll("_", " ")}</h3></div><Activity size={20} /></div><div className="baseline-track"><span style={{ width: trend.data.observation_count ? "42%" : "12%" }} /></div><p className="panel-copy">{trend.data.explanation}</p><div className="observation-row"><span><Check size={14} /> Check-ins are optional</span><span><LockKeyhole size={14} /> Private by design</span><span><CircleHelp size={14} /> Not medical advice</span></div></article><PhotoPanel location={location} onAnalyzed={onPhotoAnalyzed} /></section></>;
}

function PhotoPanel({ location, onAnalyzed }: { location: SelectedLocationContext; onAnalyzed?: () => void }) {
  const [result, setResult] = useState<{ photo: { analysis_possible: boolean; message: string; image_quality: number; dryness_indicator?: number; confidence?: number }; environment?: { humidity: number; data_quality: string }; risk?: { overall_exposure: number }; insight?: string } | null>(null);
  const [busy, setBusy] = useState(false);
  async function analyze(file: File) { setBusy(true); setResult(null); try { const form = new FormData(); form.append("photo", file); const query = new URLSearchParams({ latitude: String(location.latitude), longitude: String(location.longitude), skin_type: "Dry", sensitivity: "Moderate", transportation: "MOTORCYCLE" }); const response = await fetch(`http://127.0.0.1:8000/api/users/demo-user-001/skin-insight?${query}`, { method: "POST", body: form }); const payload = await response.json().catch(() => null); setResult(response.ok ? payload : null); if (response.ok && payload?.photo?.analysis_possible) onAnalyzed?.(); } catch { setResult(null); } finally { setBusy(false); } }
  return <article className="side-panel photo-placeholder"><div className="photo-icon"><Sun size={22} /></div><span className="eyebrow">REQUIRED FOR FULL ANALYSIS</span><h3>{result ? "Combined skin insight" : "Upload your current skin photo."}</h3>{result ? <div className="photo-result"><strong>{result.photo.analysis_possible ? "Combined insight ready" : "Photo needs another try"}</strong><p>{result.photo.message}</p>{result.photo.analysis_possible && <><small>Quality {result.photo.image_quality}/100 · Confidence {result.photo.confidence}/100 · Dryness {result.photo.dryness_indicator}/100</small><small>Location {location.locality} · Humidity {result.environment?.humidity}% · Exposure {result.risk?.overall_exposure}/100</small><p>{result.insight}</p></>}</div> : <p>A current image is required before Atmo Derma can combine visual skin indicators with your profile and live environment. The image does not diagnose a condition.</p>}<label className="upload-button" htmlFor="skin-photo-upload">{busy ? "Analyzing with environment..." : result ? "Upload a newer photo" : "Upload photo to continue"}<input id="skin-photo-upload" required={!result} aria-required="true" type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => { const file = event.target.files?.[0]; if (file) analyze(file); }} /></label></article>;
}

function RoutineView() {
  const routine = useApi("/api/routine/today", [] as { title: string; detail: string; reason: string }[]);
  return <><ViewHeader eyebrow="ADAPTIVE ROUTINE" title="Small steps, well timed." copy="Your existing routine stays stable. Environmental adjustments are temporary, explainable, and optional." action={<span className="demo-pill light-pill"><span className="pulse" /> Personalized today</span>} /><section className="routine-columns"><RoutineColumn title="Morning" icon={<Sun size={18} />} items={routine.data.slice(0, 1)} /><RoutineColumn title="During the day" icon={<CloudSun size={18} />} items={routine.data.slice(1, 2)} /><RoutineColumn title="Evening" icon={<Moon size={18} />} items={routine.data.slice(2)} /></section><article className="wide-panel why-routine"><div className="panel-heading"><div><span className="section-kicker"><Sparkles size={15} /> WHY THESE SUGGESTIONS</span><h3>Guidance follows your context.</h3></div><ShieldCheck size={20} /></div><p className="panel-copy">Today’s plan combines your dry-skin profile, elevated UV, lower humidity, motorcycle commute, and recent environment data. It does not diagnose a condition or prescribe treatment.</p></article></>;
}

function RoutineColumn({ title, icon, items }: { title: string; icon: React.ReactNode; items: { title: string; detail: string; reason: string }[] }) {
  return <article className="routine-column"><div className="routine-title">{icon}<h3>{title}</h3></div>{items.length ? items.map((item) => <div className="routine-item" key={item.title}><span className="check done"><Check size={13} /></span><div><strong>{item.title}</strong><p>{item.detail}</p><small>Why: {item.reason}</small></div></div>) : <p className="empty-copy">No additional adjustment is needed right now.</p>}</article>;
}

function ExposureView() {
  const { data } = useApi("/api/exposure/today", { outdoor_minutes: 252, high_uv_minutes: 68, elevated_pollution_minutes: 0, highest_exposure_period: "12:30 PM - 2:00 PM", transport_context: "MOTORCYCLE", indoor_air_quality: "Good" });
  const [period, setPeriod] = useState("Today");
  return <><ViewHeader eyebrow="EXPOSURE HISTORY" title="See when conditions changed." copy="Exposure context helps explain the day without pretending that transport changes the measured environment." action={<div className="period-switch">{["Today", "7 days", "30 days"].map((item) => <button className={period === item ? "selected" : ""} key={item} onClick={() => setPeriod(item)}>{item}</button>)}</div>} /><div className="stat-grid"><StatTile label="Outdoor exposure" value={`${Math.floor(data.outdoor_minutes / 60)}h ${data.outdoor_minutes % 60}m`} detail={`${period} recorded periods`} tone="neutral" /><StatTile label="High UV" value={`${data.high_uv_minutes}m`} detail="Strongest period" tone="alert" /><StatTile label="Elevated pollution" value={`${data.elevated_pollution_minutes}m`} detail="No elevated period recorded" tone="good" /><StatTile label="Indoor air" value={data.indoor_air_quality} detail="From available readings" tone="good" /></div><article className="wide-panel timeline-panel"><div className="panel-heading"><div><span className="eyebrow">24-HOUR TIMELINE</span><h3>Your highest exposure period</h3></div><Activity size={20} /></div><div className="timeline"><span className="timeline-fill" /><i className="timeline-marker" /><span className="timeline-label">12:30 PM</span></div><div className="timeline-hours"><span>00</span><span>06</span><span>12</span><span>18</span><span>24</span></div><div className="observation-row"><span><i className="dot coral" /> UV high</span><span><i className="dot green" /> Indoor</span><span><i className="dot amber" /> Commute</span></div><p className="panel-copy">Your environmental exposure was highest during your afternoon {data.transport_context.toLowerCase()} commute. Selected range: {period}.</p></article></>;
}

function InsightsView() {
  const daily = useApi("/api/insights/daily", [] as { title: string; message: string; source: string }[]);
  const weekly = useApi("/api/insights/weekly", [] as { title: string; message: string; source: string }[]);
  const [filtered, setFiltered] = useState(false);
  const visibleDaily = filtered ? daily.data.filter((item) => item.source.includes("environment")) : daily.data;
  return <><ViewHeader eyebrow="TRACEABLE INSIGHTS" title="What we are learning." copy="Every insight points back to an environmental reading, your profile, or a self-reported observation." action={<button className="outline-button" onClick={() => setFiltered(!filtered)}><SlidersHorizontal size={15} /> {filtered ? "Show all insights" : "Environment only"}</button>} /><section className="insight-feed"><div><span className="eyebrow">TODAY</span>{visibleDaily.map((item) => <InsightCard key={item.title} item={item} />)}{!visibleDaily.length && <p className="empty-copy">No environment-only insight is available yet.</p>}</div><div><span className="eyebrow">THIS WEEK</span>{weekly.data.map((item) => <InsightCard key={item.title} item={item} />)}<article className="privacy-note"><LockKeyhole size={18} /><div><strong>Your data stays yours.</strong><p>Atmo Derma uses your own history as your baseline. You can delete skin observations and photos from settings.</p></div></article></div></section></>;
}

function InsightCard({ item }: { item: { title: string; message: string; source: string } }) { return <article className="insight-card"><div className="insight-icon"><Sparkles size={16} /></div><div><h3>{item.title}</h3><p>{item.message}</p><small>Source: {item.source}</small></div><ChevronRight size={16} /></article>; }

function DevicesView() {
  const { data, loading } = useApi("/api/devices", [] as { device_id: string; name: string; connected: boolean; data_quality: string; sensors: string[] }[]);
  return <><ViewHeader eyebrow="INDOOR SENSORS" title="The room matters too." copy="Connect a future sensor or explore the simulator. Indoor readings are never assumed to be medically meaningful." action={<span className="demo-pill light-pill"><span className="pulse" /> Demo controls</span>} /><section className="device-list">{loading ? <div className="loading-block" /> : data.map((device) => <article className="device-card" key={device.device_id}><div className="device-icon"><AirVent size={23} /></div><div className="device-main"><div className="device-title"><h3>{device.name}</h3><span className="status-badge"><span className="pulse" /> Connected</span></div><p>{device.device_id} · {device.data_quality} data</p><div className="sensor-tags">{device.sensors.map((sensor) => <span key={sensor}>{sensor}</span>)}</div></div><ChevronRight size={18} /></article>)}</section><IndoorDemoPanel /><article className="wide-panel device-callout"><div className="callout-icon"><Leaf size={20} /></div><div><span className="eyebrow">DEMO MODE</span><h3>Demo sensor data is moving gradually.</h3><p className="panel-copy">The simulator produces changing temperature, humidity, PM2.5, CO2-equivalent, and VOC values. It is not a substitute for calibrated environmental measurement.</p></div></article></>;
}

function IndoorDemoPanel() {
  const [values, setValues] = useState({ temperature: 27.4, humidity: 46.2, pm25: 31.5, co2: 740, voc: 120 });
  const [saved, setSaved] = useState(false);
  async function submit(event: React.FormEvent<HTMLFormElement>) { event.preventDefault(); const form = new FormData(event.currentTarget); const payload = Object.fromEntries(Object.entries(Object.fromEntries(form.entries())).map(([key, value]) => [key, Number(value)])); const response = await fetch("http://127.0.0.1:8000/api/indoor/demo", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }); if (response.ok) { const next = await response.json(); setValues({ temperature: next.temperature, humidity: next.humidity, pm25: next.pm25, co2: next.co2, voc: next.voc }); setSaved(true); } }
  return <form className="wide-panel indoor-demo" onSubmit={submit}><div className="panel-heading"><div><span className="eyebrow">SIMULATOR CONTROLS</span><h3>Test indoor air conditions</h3></div><Settings2 size={19} /></div><p className="panel-copy">Change values to see how the indoor context behaves. These readings are simulated.</p><div className="indoor-form-grid">{Object.entries(values).map(([key, value]) => <label key={key}>{key.toUpperCase()}<input name={key} type="number" step="0.1" value={value} onChange={(event) => setValues({ ...values, [key]: Number(event.target.value) })} /></label>)}</div><button className="primary-button" type="submit"><Radio size={16} /> {saved ? "Demo updated" : "Apply demo conditions"}</button></form>;
}

function ProfileView() {
  const [saved, setSaved] = useState(false);
  return <><ViewHeader eyebrow="YOUR PROFILE" title="Make the context personal." copy="These details help Atmo Derma weight environmental context. You can change or remove them anytime." action={saved ? <span className="saved-note"><Check size={15} /> Saved locally</span> : undefined} /><form className="settings-form" onSubmit={(event) => { event.preventDefault(); setSaved(true); }}><div className="form-section"><UserRound size={20} /><div><h3>About you</h3><p>Only information relevant to your experience is requested.</p></div></div><div className="form-grid"><label>Display name<input defaultValue="Alex Shah" /></label><label>Age<input type="number" defaultValue="29" min="13" max="120" /></label><label>Skin type<select defaultValue="Dry"><option>Normal</option><option>Dry</option><option>Oily</option><option>Combination</option><option>Unsure</option></select></label><label>Sensitivity<select defaultValue="Moderate"><option>Low</option><option>Moderate</option><option>High</option><option>Unsure</option></select></label><label>Transportation<select defaultValue="MOTORCYCLE"><option>Walking</option><option>Bicycle</option><option>Motorcycle</option><option>Car</option><option>Public transport</option><option>Mostly indoors</option></select></label><label>Typical outdoor exposure<select defaultValue="ONE_TO_THREE_HOURS"><option>Less than 30 minutes/day</option><option>30–60 minutes</option><option>1–3 hours</option><option>3+ hours</option></select></label></div><button className="primary-button" type="submit"><Save size={16} /> Save profile</button></form></>;
}

function SettingsView() {
  const [deleteOpen, setDeleteOpen] = useState(false);
  return <><ViewHeader eyebrow="CONTROL CENTER" title="Quiet controls for a private product." copy="Choose what Atmo Derma can remember, notify you about, and use for personal context." /><section className="settings-list"><SettingRow icon={<BellIcon />} title="Contextual notifications" detail="Useful, rare, actionable alerts" enabled /><SettingRow icon={<Sparkles size={18} />} title="Smart check-ins" detail="Ask only when a question may be useful" enabled /><SettingRow icon={<CloudSun size={18} />} title="Location access" detail="Use current location for environment lookups" /><SettingRow icon={<LockKeyhole size={18} />} title="Retain original photos" detail="Off by default. Structured indicators are preferred." /><SettingRow icon={<Moon size={18} />} title="Appearance" detail="Light mode · system preference" enabled /></section><article className="danger-panel"><div><span className="eyebrow">DATA CONTROLS</span><h3>Delete your skin history</h3><p>{deleteOpen ? "Demo mode: no data has been deleted. Connect PostgreSQL to enable account-wide deletion." : "This removes check-ins, visual indicators, and retained photos from the account."}</p></div><button className="outline-button danger-button" onClick={() => setDeleteOpen(!deleteOpen)}>{deleteOpen ? "Close" : "Review deletion"}</button></article></>;
}

function SettingRow({ icon, title, detail, enabled = false }: { icon: React.ReactNode; title: string; detail: string; enabled?: boolean }) {
  const [on, setOn] = useState(enabled);
  return <div className="setting-row"><span className="setting-icon">{icon}</span><div className="setting-copy"><strong>{title}</strong><span>{detail}</span></div><button className={on ? "toggle on" : "toggle"} onClick={() => setOn(!on)} aria-label={`${on ? "Disable" : "Enable"} ${title}`} aria-pressed={on}><span /></button></div>;
}

function BellIcon() { return <Activity size={18} />; }
function LoadingTiles({ count }: { count: number }) { return <>{Array.from({ length: count }, (_, index) => <div className="skeleton-tile" key={index} />)}</>; }
