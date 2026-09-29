import React, { useEffect, useMemo, useState } from 'react';
import {
  Activity, AlertTriangle, ArrowRight, Blocks, CheckCircle2, ClipboardCheck, FileSearch, Fingerprint,
  History, KeyRound, LockKeyhole, LogOut, ScanLine, Search, ShieldCheck, Sparkles, UploadCloud, UserCheck,
  XCircle, Eye, RefreshCw, Globe2, Database, BrainCircuit
} from 'lucide-react';
import { api, authStore, openEvidence } from './api.js';

const workflow = [
  ['1', 'Upload document', 'Submit an ID or certificate through the secure web interface.', UploadCloud],
  ['2', 'Extract & inspect', 'Tesseract OCR extracts text while OpenCV, ELA, sharpness, noise and edges inspect visual signals.', FileSearch],
  ['3', 'Gemini analysis', 'Gemini reasons over OCR + forensic evidence and creates an explainable reviewer summary.', BrainCircuit],
  ['4', 'Human review', 'A verifier checks evidence, model reasoning and the original encrypted document before deciding.', UserCheck],
  ['5', 'Hash & record', 'SHA-256 and a chained revision event create tamper-evident verification history.', Fingerprint],
  ['6', 'Verify later', 'Authorized/public lookup exposes hash and status without revealing private identity evidence.', Search],
];

const features = [
  ['AI-assisted screening', 'OCR + image forensics assess text consistency, visual tampering, sharpness, noise and edges.', ScanLine],
  ['Gemini reasoning', 'Gemini combines extracted text and visual signals into concise, explainable review guidance.', Sparkles],
  ['Human-in-the-loop', 'The screening score never approves a document; a reviewer makes the final decision.', UserCheck],
  ['Tamper-evident history', 'SHA-256 revision chaining plus optional blockchain anchoring create an auditable history.', Blocks],
  ['Privacy & security', 'Identity evidence is encrypted off-chain with AES-256-GCM, JWT access controls and Argon2 passwords.', LockKeyhole],
  ['Public verification', 'Hash/status can be checked without exposing the private document or extracted identity fields.', Globe2],
];

function Brand({ compact = false }) {
  return <div className="flex items-center gap-3">
    <div className="relative h-11 w-11 shrink-0">
      <div className="absolute left-0 top-4 h-6 w-6 rotate-45 rounded-[8px] bg-greenx/95" />
      <div className="absolute right-0 top-0 h-6 w-6 rotate-45 rounded-[8px] bg-cyanx/95" />
      <div className="absolute right-0 bottom-0 h-6 w-6 rotate-45 rounded-[8px] bg-indigox/95" />
      <div className="absolute inset-[13px] rounded-full bg-white shadow" />
    </div>
    {!compact && <div className="leading-none">
      <div className="text-xl font-black tracking-tight text-ink">VERI<span className="text-indigox">SHIELD</span></div>
      <div className="mt-1 text-[9px] font-bold uppercase tracking-[.25em] text-slate-400">Detect · Review · Verify</div>
    </div>}
  </div>;
}

function Pill({ children, tone = 'blue' }) {
  const tones = {
    blue: 'bg-blue-50 text-navy ring-blue-100', green: 'bg-emerald-50 text-emerald-700 ring-emerald-100',
    amber: 'bg-amber-50 text-amber-700 ring-amber-100', red: 'bg-rose-50 text-rose-700 ring-rose-100', gray: 'bg-slate-50 text-slate-600 ring-slate-100'
  };
  return <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-[11px] font-bold ring-1 ${tones[tone]}`}>{children}</span>;
}

function Landing({ onAuth, onPublicVerify }) {
  return <div className="min-h-screen bg-paper text-ink">
    <header className="sticky top-0 z-30 border-b border-navy/10 bg-white/90 backdrop-blur-xl">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-5 lg:px-8">
        <Brand />
        <nav className="hidden items-center gap-7 text-sm font-semibold text-slate-600 md:flex">
          <a href="#solution" className="hover:text-navy">Solution</a><a href="#features" className="hover:text-navy">Features</a><a href="#workflow" className="hover:text-navy">Workflow</a>
        </nav>
        <div className="flex gap-2">
          <button onClick={onPublicVerify} className="hidden rounded-xl px-4 py-2 text-sm font-bold text-navy hover:bg-blue-50 sm:block">Public verify</button>
          <button onClick={() => onAuth('login')} className="rounded-xl border border-navy/15 bg-white px-4 py-2 text-sm font-bold text-navy">Sign in</button>
          <button onClick={() => onAuth('register')} className="rounded-xl bg-ink px-4 py-2 text-sm font-bold text-white shadow-lg shadow-blue-950/15">Get started</button>
        </div>
      </div>
      <div className="gradient-rule h-1 w-full" />
    </header>

    <main>
      <section className="ppt-grid relative overflow-hidden">
        <div className="mx-auto grid min-h-[690px] max-w-7xl items-center gap-12 px-5 py-16 lg:grid-cols-[1.1fr_.9fr] lg:px-8">
          <div>
            <div className="mb-6 flex flex-wrap gap-2">
              <Pill>Blockchain & Cybersecurity</Pill><Pill tone="green">Software</Pill><Pill tone="gray">Algorithm Avengers</Pill>
            </div>
            <h1 className="max-w-4xl text-5xl font-black uppercase leading-[.98] tracking-[-.045em] text-ink sm:text-6xl lg:text-[72px]">
              AI-Based Fake Identity & <span className="text-navy">Document Screening System</span>
            </h1>
            <div className="gradient-rule my-7 h-1.5 w-52 rounded-full" />
            <p className="max-w-2xl text-lg leading-8 text-slate-600">Fast screening + explainability + trusted verification history. VeriShield combines OCR, OpenCV/ELA, Gemini reasoning, reviewer control and tamper-evident records.</p>
            <div className="mt-8 flex flex-wrap gap-3">
              <button onClick={() => onAuth('register')} className="flex items-center gap-2 rounded-2xl bg-ink px-6 py-3.5 font-extrabold text-white shadow-soft">Start screening <ArrowRight size={18}/></button>
              <button onClick={onPublicVerify} className="flex items-center gap-2 rounded-2xl border border-navy/15 bg-white px-6 py-3.5 font-extrabold text-navy"><Fingerprint size={18}/> Verify a hash</button>
            </div>
            <p className="mt-8 text-sm font-extrabold uppercase tracking-[.18em] text-slate-400">“AI Eyes for Authentic Identities.”</p>
          </div>

          <div className="relative mx-auto h-[500px] w-full max-w-[520px]">
            <div className="hex absolute right-5 top-8 h-80 w-80 bg-slate-200/60" />
            <div className="hex absolute left-10 bottom-9 h-40 w-40 bg-slate-200/50" />
            <div className="absolute inset-8 rounded-[30px] border border-navy/10 bg-white p-6 shadow-soft">
              <div className="flex items-center justify-between"><Pill tone="green"><span className="status-dot bg-emerald-500"/> AI screening ready</Pill><ShieldCheck className="text-indigox"/></div>
              <div className="mt-6 rounded-2xl border border-dashed border-navy/20 bg-blue-50/50 p-5">
                <div className="flex items-center gap-4"><div className="rounded-2xl bg-white p-4 shadow"><FileSearch className="text-navy"/></div><div><p className="font-black text-navy">identity_document.pdf</p><p className="text-sm text-slate-500">OCR + OpenCV + ELA + Gemini</p></div></div>
              </div>
              <div className="mt-5 grid grid-cols-2 gap-3">
                <Metric label="ELA" value="7.8" status="Normal" /><Metric label="Sharpness" value="132" status="Readable" />
                <Metric label="Noise" value="9.4" status="Normal" /><Metric label="Edge density" value="0.14" status="Normal" />
              </div>
              <div className="mt-5 rounded-2xl bg-ink p-5 text-white">
                <div className="flex items-center justify-between"><span className="text-xs font-bold uppercase tracking-widest text-blue-200">Gemini reviewer summary</span><Pill tone="amber">Risk 28</Pill></div>
                <p className="mt-3 text-sm leading-6 text-blue-50">Core fields appear coherent. One typography alignment detail should be checked by a human reviewer.</p>
              </div>
              <div className="mt-5 flex items-center gap-2 text-xs font-bold text-slate-500"><UserCheck size={16} className="text-indigox"/> Final decision: PENDING HUMAN REVIEW</div>
            </div>
          </div>
        </div>
      </section>

      <section id="solution" className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
        <SectionTitle kicker="Solution overview" title="DETECT → REVIEW → VERIFY" text="An AI-assisted platform that combines document analysis, OCR, cybersecurity controls, human verification and blockchain-backed records." />
        <div className="mt-10 grid gap-4 md:grid-cols-3">
          <InfoCard icon={ScanLine} title="Detect" text="Upload IDs/certificates; OCR and forensic checks surface text and visual inconsistencies." />
          <InfoCard icon={UserCheck} title="Review" text="Gemini explains the evidence, but a verifier reviews the original document and makes the decision." />
          <InfoCard icon={Blocks} title="Verify" text="SHA-256 revision history and optional blockchain anchoring allow later hash/status verification." />
        </div>
      </section>

      <section id="features" className="border-y border-navy/10 bg-white py-20">
        <div className="mx-auto max-w-7xl px-5 lg:px-8">
          <SectionTitle kicker="Key features" title="Explainable AI + reviewer control + privacy-aware storage" text="The implementation mirrors the Round 1 design principle and keeps the screening score separate from the final human decision." />
          <div className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {features.map(([title, text, Icon]) => <InfoCard key={title} icon={Icon} title={title} text={text} />)}
          </div>
        </div>
      </section>

      <section id="workflow" className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
        <SectionTitle kicker="Workflow" title="Six stages, exactly where each control belongs" text="Gemini is a visible, functional part of the AI screening stage—not a cosmetic mention—and the original Detect → Review → Verify principle is preserved." />
        <div className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {workflow.map(([n, title, text, Icon]) => <div key={n} className="relative rounded-3xl border border-navy/10 bg-white p-6 shadow-sm">
            <div className="mb-5 flex items-center justify-between"><div className="rounded-2xl bg-blue-50 p-3 text-navy"><Icon/></div><span className="text-4xl font-black text-slate-100">{n}</span></div>
            <h3 className="text-lg font-black text-ink">{title}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{text}</p>
          </div>)}
        </div>
      </section>
    </main>

    <footer className="bg-ink text-white"><div className="mx-auto flex max-w-7xl flex-col gap-6 px-5 py-10 sm:flex-row sm:items-center sm:justify-between lg:px-8"><Brand/><div className="text-sm text-blue-200">Algorithm Avengers · MLH Hack Day @ DTU · Round 1 implementation</div></div></footer>
  </div>;
}

function Metric({ label, value, status }) {
  return <div className="rounded-2xl border border-navy/10 bg-white p-3"><div className="text-[10px] font-black uppercase tracking-wider text-slate-400">{label}</div><div className="mt-1 text-xl font-black text-ink">{value}</div><div className="text-xs font-semibold text-emerald-600">{status}</div></div>;
}
function SectionTitle({ kicker, title, text }) { return <div className="max-w-3xl"><p className="text-xs font-black uppercase tracking-[.2em] text-indigox">{kicker}</p><h2 className="mt-3 text-3xl font-black tracking-tight text-ink sm:text-4xl">{title}</h2><p className="mt-4 text-base leading-7 text-slate-500">{text}</p></div>; }
function InfoCard({ icon: Icon, title, text }) { return <div className="rounded-3xl border border-navy/10 bg-white p-6 shadow-sm"><div className="mb-5 inline-flex rounded-2xl bg-blue-50 p-3 text-navy"><Icon/></div><h3 className="text-lg font-black">{title}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{text}</p></div>; }

function AuthModal({ mode, onClose, onSuccess }) {
  const [tab, setTab] = useState(mode);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  async function submit(e) {
    e.preventDefault(); setBusy(true); setError('');
    const form = new FormData(e.currentTarget);
    const payload = Object.fromEntries(form.entries());
    try {
      const data = tab === 'login' ? await api.login(payload) : await api.register(payload);
      authStore.token = data.token; onSuccess(data.user);
    } catch (err) { setError(err.message); } finally { setBusy(false); }
  }
  return <div className="fixed inset-0 z-50 grid place-items-center bg-ink/60 p-4 backdrop-blur-sm">
    <div className="w-full max-w-md rounded-[28px] bg-white p-7 shadow-2xl">
      <div className="flex items-center justify-between"><Brand/><button onClick={onClose} className="rounded-xl p-2 text-slate-400 hover:bg-slate-50"><XCircle/></button></div>
      <div className="mt-7 grid grid-cols-2 rounded-xl bg-slate-100 p-1"><button onClick={() => setTab('login')} className={`rounded-lg py-2 text-sm font-bold ${tab==='login'?'bg-white text-ink shadow':'text-slate-500'}`}>Sign in</button><button onClick={() => setTab('register')} className={`rounded-lg py-2 text-sm font-bold ${tab==='register'?'bg-white text-ink shadow':'text-slate-500'}`}>Create account</button></div>
      <form onSubmit={submit} className="mt-6 space-y-4">
        {tab==='register' && <Field label="Full name" name="name" placeholder="Mayank Panchal" required />}
        <Field label="Email" name="email" type="email" placeholder="you@example.com" required />
        <Field label="Password" name="password" type="password" placeholder="Minimum 8 characters" required minLength={8} />
        {error && <div className="rounded-xl bg-rose-50 p-3 text-sm font-semibold text-rose-700">{error}</div>}
        <button disabled={busy} className="w-full rounded-xl bg-ink py-3 font-extrabold text-white disabled:opacity-60">{busy?'Please wait…':tab==='login'?'Sign in':'Create account'}</button>
      </form>
      <div className="mt-5 rounded-2xl border border-navy/10 bg-blue-50/60 p-4 text-xs leading-5 text-slate-600">
        <b className="text-navy">Demo accounts</b><br/>Submitter: <code>submitter@verishield.ai</code><br/>Reviewer: <code>reviewer@verishield.ai</code><br/>Password: <code>Demo@12345</code>
      </div>
    </div>
  </div>;
}
function Field({ label, ...props }) { return <label className="block"><span className="mb-1.5 block text-xs font-black uppercase tracking-wider text-slate-500">{label}</span><input {...props} className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none transition focus:border-indigox focus:ring-4 focus:ring-indigo-100" /></label>; }

function PublicVerifyModal({ onClose }) {
  const [hash, setHash] = useState(''); const [result, setResult] = useState(null); const [error, setError] = useState(''); const [busy, setBusy] = useState(false);
  async function verify(e) { e.preventDefault(); setBusy(true); setError(''); try { setResult(await api.verify(hash.trim())); } catch (err) { setError(err.message); } finally { setBusy(false); } }
  return <div className="fixed inset-0 z-50 grid place-items-center bg-ink/60 p-4 backdrop-blur-sm"><div className="w-full max-w-2xl rounded-[28px] bg-white p-7 shadow-2xl">
    <div className="flex items-center justify-between"><div><p className="text-xs font-black uppercase tracking-[.2em] text-indigox">Public verification</p><h2 className="mt-1 text-2xl font-black">Check a SHA-256 document hash</h2></div><button onClick={onClose} className="rounded-xl p-2 text-slate-400 hover:bg-slate-50"><XCircle/></button></div>
    <p className="mt-3 text-sm leading-6 text-slate-500">Only hash/status metadata is returned. Private identity evidence remains encrypted off-chain.</p>
    <form onSubmit={verify} className="mt-6 flex gap-2"><input value={hash} onChange={e=>setHash(e.target.value)} required minLength={64} maxLength={64} placeholder="64-character SHA-256 hash" className="min-w-0 flex-1 rounded-xl border border-slate-200 px-4 py-3 font-mono text-sm outline-none focus:border-indigox"/><button disabled={busy} className="rounded-xl bg-ink px-5 font-extrabold text-white">Verify</button></form>
    {error && <div className="mt-4 rounded-xl bg-rose-50 p-3 text-sm font-semibold text-rose-700">{error}</div>}
    {result && <div className="mt-5 rounded-2xl border border-navy/10 bg-slate-50 p-5">{result.found ? <div className="space-y-3"><div className="flex items-center gap-2"><CheckCircle2 className="text-emerald-500"/><b>Record found</b></div><KV label="Status" value={result.status}/><KV label="Reviewer decision" value={result.reviewer_decision || 'Pending'}/><KV label="Latest event hash" value={result.latest_event_hash}/><KV label="Blockchain tx" value={result.blockchain_tx || 'Not anchored / optional'}/><p className="text-xs text-slate-500">{result.privacy_note}</p></div> : <div className="flex items-center gap-2 text-slate-600"><AlertTriangle className="text-amber-500"/> No verification record found for this hash.</div>}</div>}
  </div></div>;
}

function Dashboard({ user, onLogout }) {
  const [view, setView] = useState(user.role === 'reviewer' ? 'review' : 'scan');
  const nav = [
    ['scan','New screening',ScanLine],
    ...(user.role==='reviewer' ? [['review','Review queue',UserCheck]] : []),
    ['history','Verification history',History],
    ['verify','Public verify',Fingerprint],
  ];
  return <div className="min-h-screen bg-paper text-ink lg:grid lg:grid-cols-[260px_1fr]">
    <aside className="border-r border-navy/10 bg-white p-5 lg:sticky lg:top-0 lg:h-screen">
      <Brand/>
      <div className="my-6 gradient-rule h-1 rounded-full"/>
      <div className="rounded-2xl bg-blue-50 p-4"><p className="text-xs font-black uppercase tracking-wider text-navy">Detect → Review → Verify</p><p className="mt-1 text-xs leading-5 text-slate-500">Screening output is evidence for a reviewer, never an automatic approval.</p></div>
      <nav className="mt-6 space-y-2">{nav.map(([key,label,Icon])=><button key={key} onClick={()=>setView(key)} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-bold transition ${view===key?'bg-ink text-white shadow':'text-slate-600 hover:bg-slate-50'}`}><Icon size={19}/>{label}</button>)}</nav>
      <div className="mt-6 rounded-2xl border border-navy/10 p-4 lg:absolute lg:bottom-5 lg:left-5 lg:right-5"><div className="text-sm font-black">{user.name}</div><div className="mt-1 text-xs text-slate-500">{user.email}</div><div className="mt-3 flex items-center justify-between"><Pill tone={user.role==='reviewer'?'green':'blue'}>{user.role}</Pill><button onClick={onLogout} title="Sign out" className="rounded-lg p-2 text-slate-400 hover:bg-slate-50 hover:text-rose-500"><LogOut size={18}/></button></div></div>
    </aside>
    <main className="p-4 sm:p-6 lg:p-8">
      {view==='scan' && <ScreeningView user={user}/>} {view==='review' && <ReviewQueue/>} {view==='history' && <HistoryView user={user}/>} {view==='verify' && <VerifyView/>}
    </main>
  </div>;
}

function PageHead({ kicker, title, text, action }) { return <div className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><p className="text-xs font-black uppercase tracking-[.2em] text-indigox">{kicker}</p><h1 className="mt-2 text-3xl font-black tracking-tight sm:text-4xl">{title}</h1><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">{text}</p></div>{action}</div>; }

function ScreeningView() {
  const [file, setFile] = useState(null); const [busy,setBusy]=useState(false); const [data,setData]=useState(null); const [error,setError]=useState('');
  async function analyze(){ if(!file)return; setBusy(true);setError('');setData(null); try{const result=await api.createScreening(file);setData(result.screening);}catch(e){setError(e.message);}finally{setBusy(false);} }
  return <>
    <PageHead kicker="AI-assisted screening" title="Detect suspicious identity documents" text="The analysis layer runs OCR + OpenCV/ELA first, then Gemini reasons over those signals. Every result remains pending until human review." action={<Pill tone="green"><ShieldCheck size={13}/> Encrypted off-chain evidence</Pill>}/>
    <div className="grid gap-5 xl:grid-cols-[.8fr_1.2fr]">
      <section className="rounded-3xl border border-navy/10 bg-white p-5 shadow-sm">
        <div className="rounded-3xl border-2 border-dashed border-navy/15 bg-blue-50/40 p-8 text-center">
          <div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-white text-indigox shadow"><UploadCloud/></div>
          <h3 className="mt-4 font-black">Upload ID / Certificate</h3><p className="mt-1 text-sm text-slate-500">JPG, PNG, WebP or PDF · max 10 MB</p>
          <label className="mt-5 inline-flex cursor-pointer rounded-xl bg-ink px-5 py-3 text-sm font-extrabold text-white">Choose document<input type="file" accept="image/jpeg,image/png,image/webp,application/pdf" hidden onChange={e=>setFile(e.target.files?.[0]||null)}/></label>
        </div>
        {file && <div className="mt-4 flex items-center justify-between rounded-2xl border border-navy/10 p-4"><div className="flex items-center gap-3"><div className="rounded-xl bg-blue-50 p-3 text-navy"><FileSearch/></div><div><p className="max-w-[220px] truncate text-sm font-black">{file.name}</p><p className="text-xs text-slate-400">{(file.size/1024/1024).toFixed(2)} MB</p></div></div><button onClick={()=>setFile(null)} className="text-slate-400"><XCircle/></button></div>}
        <button onClick={analyze} disabled={!file||busy} className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigox to-cyanx py-3.5 font-extrabold text-white shadow-lg shadow-indigo-200 disabled:opacity-40">{busy?<><RefreshCw className="animate-spin" size={18}/> Running OCR → forensics → Gemini…</>:<><Sparkles size={18}/> Run AI screening</>}</button>
        {error && <div className="mt-4 rounded-xl bg-rose-50 p-4 text-sm font-semibold text-rose-700">{error}</div>}
        <div className="mt-5 grid grid-cols-2 gap-3 text-xs"><MiniControl icon={FileSearch} text="Tesseract OCR"/><MiniControl icon={Activity} text="OpenCV + ELA"/><MiniControl icon={BrainCircuit} text="Gemini reasoning"/><MiniControl icon={LockKeyhole} text="AES-256-GCM"/></div>
      </section>
      <section className="min-h-[620px] rounded-3xl border border-navy/10 bg-white p-5 shadow-sm">
        {!data ? <EmptyResults busy={busy}/> : <ResultPanel data={data}/>}
      </section>
    </div>
  </>;
}
function MiniControl({icon:Icon,text}){return <div className="flex items-center gap-2 rounded-xl bg-slate-50 p-3 font-bold text-slate-600"><Icon size={16} className="text-indigox"/>{text}</div>}
function EmptyResults({busy}){return <div className="grid min-h-[570px] place-items-center text-center"><div><div className="mx-auto grid h-20 w-20 place-items-center rounded-full bg-blue-50 text-navy">{busy?<RefreshCw className="animate-spin" size={34}/>:<ScanLine size={34}/>}</div><h3 className="mt-5 text-xl font-black">{busy?'Analyzing evidence…':'Screening results appear here'}</h3><p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">{busy?'Local OCR and forensics run first; Gemini then receives those signals plus the document for reviewer-facing reasoning.':'Upload a document to see OCR fields, forensic metrics, Gemini explanation, risk signal and reviewer status.'}</p></div></div>}

function ResultPanel({data}) {
  const ai=data.ai_review||{}; const fields=data.extracted_fields||{}; const agg=data.forensics?.aggregate||{}; const tone=data.risk_level==='High'?'red':data.risk_level==='Medium'?'amber':'green';
  const color=data.risk_level==='High'?'#e11d48':data.risk_level==='Medium'?'#f59e0b':'#10b981';
  const localFallback=ai.analysis_mode==='LOCAL_FALLBACK';
  const fallbackModel=ai.analysis_mode==='GEMINI_FALLBACK_MODEL';
  const summaryTitle=localFallback?'Local OCR / forensics fallback summary':fallbackModel?'Gemini fallback-model reviewer summary':'Gemini reviewer summary';
  return <div>
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><p className="text-xs font-black uppercase tracking-[.2em] text-indigox">Screening complete</p><h2 className="mt-1 text-2xl font-black">Evidence package for reviewer</h2></div><Pill tone="amber"><UserCheck size={13}/> {data.status?.replaceAll('_',' ')}</Pill></div>
    <div className="mt-5 grid gap-4 md:grid-cols-[180px_1fr]">
      <div className="rounded-2xl bg-slate-50 p-5 text-center"><div className="risk-ring mx-auto grid h-28 w-28 place-items-center rounded-full" style={{'--score':data.risk_score,'--ring':color}}><div className="grid h-20 w-20 place-items-center rounded-full bg-white"><div><div className="text-3xl font-black">{data.risk_score}</div><div className="text-[10px] font-black uppercase text-slate-400">risk / 100</div></div></div></div><div className="mt-3"><Pill tone={tone}>{data.risk_level} risk</Pill></div><p className="mt-2 text-[11px] text-slate-400">Deterministic: {data.deterministic_risk}</p></div>
      <div className="rounded-2xl bg-ink p-5 text-white"><div className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-blue-200"><BrainCircuit size={15}/> {summaryTitle}</div><p className="mt-3 text-sm leading-6 text-blue-50">{ai.reviewer_summary || 'No summary returned.'}</p><div className="mt-4 flex flex-wrap gap-2"><Pill tone={localFallback?'amber':'blue'}>Confidence {Math.round((data.confidence||0)*100)}%</Pill><Pill tone="gray">{data.document_type}</Pill>{ai.analysis_model&&<Pill tone={localFallback?'amber':'green'}>{ai.analysis_model}</Pill>}</div>{ai.service_note&&<p className={`mt-3 rounded-xl p-3 text-xs leading-5 ${localFallback?'bg-amber-400/15 text-amber-100':'bg-emerald-400/10 text-emerald-100'}`}>{ai.service_note}</p>}</div>
    </div>
    <div className="mt-5 grid gap-4 lg:grid-cols-2">
      <ResultBox title="OCR + extracted fields" icon={FileSearch}><div className="space-y-2">{Object.entries(fields).filter(([,v])=>v).slice(0,8).map(([k,v])=><KV key={k} label={labelize(k)} value={v}/>)}</div></ResultBox>
      <ResultBox title="OpenCV / ELA signals" icon={Activity}><div className="grid grid-cols-2 gap-2"><SmallMetric label="ELA mean" value={agg.ela_mean}/><SmallMetric label="Sharpness" value={agg.sharpness}/><SmallMetric label="Noise" value={agg.noise}/><SmallMetric label="Edge density" value={agg.edge_density}/></div>{data.forensics?.flags?.length>0&&<ul className="mt-3 space-y-1 text-xs text-amber-700">{data.forensics.flags.map(x=><li key={x}>• {x}</li>)}</ul>}</ResultBox>
      <ResultBox title="Consistency checks" icon={ClipboardCheck}><div className="space-y-2">{(ai.checks||[]).map((c,i)=><div key={i} className="rounded-xl bg-slate-50 p-3"><div className="flex items-start justify-between gap-3"><div><b className="text-sm">{c.name}</b><p className="mt-1 text-xs leading-5 text-slate-500">{c.details}</p></div><CheckBadge status={c.status}/></div></div>)}</div></ResultBox>
      <ResultBox title="Human review focus" icon={UserCheck}><ul className="space-y-2 text-sm text-slate-600">{(ai.recommended_focus||[]).map((x,i)=><li key={i} className="flex gap-2"><span className="text-indigox">→</span>{x}</li>)}</ul><p className="mt-4 rounded-xl bg-blue-50 p-3 text-xs leading-5 text-navy"><b>Limitation:</b> {ai.limitations}</p></ResultBox>
    </div>
    <div className="mt-5 rounded-2xl border border-navy/10 bg-slate-50 p-4"><div className="flex items-center gap-2 text-xs font-black uppercase tracking-wider text-slate-500"><Fingerprint size={15}/> SHA-256 document hash</div><code className="mt-2 block break-all text-xs text-navy">{data.document_hash}</code></div>
  </div>;
}
function ResultBox({title,icon:Icon,children}){return <div className="rounded-2xl border border-navy/10 p-4"><div className="mb-3 flex items-center gap-2 text-sm font-black"><Icon size={17} className="text-indigox"/>{title}</div>{children}</div>}
function SmallMetric({label,value}){return <div className="rounded-xl bg-slate-50 p-3"><div className="text-[10px] font-black uppercase tracking-wider text-slate-400">{label}</div><div className="mt-1 text-lg font-black">{value ?? '—'}</div></div>}
function CheckBadge({status}){const tone=status==='PASS'?'green':status==='FAIL'?'red':status==='WARN'?'amber':'gray';return <Pill tone={tone}>{status}</Pill>}
function KV({label,value}){return <div className="grid grid-cols-[130px_1fr] gap-3 border-b border-slate-100 py-2 text-xs"><span className="font-bold text-slate-400">{label}</span><span className="break-all font-semibold text-slate-700">{String(value ?? '—')}</span></div>}
const labelize=(s)=>s.replaceAll('_',' ').replace(/\b\w/g,m=>m.toUpperCase());

function ReviewQueue(){const[items,setItems]=useState([]);const[selected,setSelected]=useState(null);const[busy,setBusy]=useState(false);const[error,setError]=useState('');
  async function load(){setBusy(true);setError('');try{const d=await api.reviewQueue();setItems(d.items||[]);if(selected){setSelected(d.items.find(x=>x.id===selected.id)||null)}}catch(e){setError(e.message)}finally{setBusy(false)}}
  useEffect(()=>{load()},[]);
  async function decide(decision){if(!selected)return;const note=window.prompt('Reviewer note (optional):','')??'';setBusy(true);try{await api.decide(selected.id,{decision,note});setSelected(null);await load()}catch(e){setError(e.message)}finally{setBusy(false)}}
  return <><PageHead kicker="Human-in-the-loop" title="Reviewer queue" text="AI screening prioritizes evidence; a human verifier makes the final decision after checking the original encrypted document." action={<button onClick={load} className="flex items-center gap-2 rounded-xl border border-navy/10 bg-white px-4 py-2 text-sm font-bold"><RefreshCw size={16}/> Refresh</button>}/>{error&&<div className="mb-4 rounded-xl bg-rose-50 p-3 text-sm font-semibold text-rose-700">{error}</div>}
  <div className="grid gap-5 xl:grid-cols-[.72fr_1.28fr]"><section className="rounded-3xl border border-navy/10 bg-white p-4 shadow-sm"><div className="mb-3 text-xs font-black uppercase tracking-wider text-slate-400">Pending review · {items.length}</div><div className="space-y-2">{items.length===0?<div className="p-8 text-center text-sm text-slate-400">No documents are waiting for review.</div>:items.map(x=><button key={x.id} onClick={()=>setSelected(x)} className={`w-full rounded-2xl border p-4 text-left transition ${selected?.id===x.id?'border-indigox bg-indigo-50':'border-navy/10 hover:bg-slate-50'}`}><div className="flex items-start justify-between gap-3"><div><div className="font-black">{x.filename}</div><div className="mt-1 text-xs text-slate-400">{x.document_type} · #{x.id}</div></div><Pill tone={x.risk_level==='High'?'red':x.risk_level==='Medium'?'amber':'green'}>{x.risk_score}</Pill></div></button>)}</div></section>
  <section className="min-h-[620px] rounded-3xl border border-navy/10 bg-white p-5 shadow-sm">{!selected?<div className="grid min-h-[570px] place-items-center text-center"><div><UserCheck size={42} className="mx-auto text-slate-300"/><h3 className="mt-4 text-xl font-black">Select a screening</h3><p className="mt-2 text-sm text-slate-500">Review evidence, Gemini reasoning and the original document before deciding.</p></div></div>:<ReviewDetail item={selected} onDecision={decide} busy={busy}/>}</section></div></>}
function ReviewDetail({item,onDecision,busy}){const ai=item.ai_review||{};const localFallback=ai.analysis_mode==='LOCAL_FALLBACK';return <div><div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><div><p className="text-xs font-black uppercase tracking-wider text-indigox">Human review · #{item.id}</p><h2 className="mt-1 text-2xl font-black">{item.filename}</h2></div><Pill tone={item.risk_level==='High'?'red':item.risk_level==='Medium'?'amber':'green'}>{item.risk_score} · {item.risk_level}</Pill></div>
  <div className="mt-5 rounded-2xl bg-ink p-5 text-white"><div className="flex flex-wrap items-center justify-between gap-2 text-xs font-black uppercase tracking-wider text-blue-200"><span>{localFallback?'Local fallback evidence summary':'Gemini evidence summary'}</span>{ai.analysis_model&&<Pill tone={localFallback?'amber':'green'}>{ai.analysis_model}</Pill>}</div><p className="mt-2 text-sm leading-6">{ai.reviewer_summary}</p>{ai.service_note&&<p className="mt-3 text-xs text-amber-100">{ai.service_note}</p>}</div>
  <div className="mt-4 grid gap-4 md:grid-cols-2"><ResultBox title="Extracted identity fields" icon={FileSearch}><div className="space-y-1">{Object.entries(item.extracted_fields||{}).filter(([,v])=>v).map(([k,v])=><KV key={k} label={labelize(k)} value={v}/>)}</div></ResultBox><ResultBox title="Recommended reviewer focus" icon={UserCheck}><ul className="space-y-2 text-sm text-slate-600">{(ai.recommended_focus||[]).map((x,i)=><li key={i}>• {x}</li>)}</ul></ResultBox></div>
  <button onClick={()=>openEvidence(item.id).catch(e=>alert(e.message))} className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-navy/10 bg-blue-50 py-3 font-extrabold text-navy"><Eye size={18}/> Open original encrypted evidence</button>
  <div className="mt-5 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-xs leading-5 text-amber-800"><b>Reviewer control:</b> The AI score is triage evidence only. Compare the original document and context before recording a decision.</div>
  <div className="mt-5 grid gap-2 sm:grid-cols-3"><button disabled={busy} onClick={()=>onDecision('VALID')} className="rounded-xl bg-emerald-600 py-3 font-extrabold text-white">Mark valid</button><button disabled={busy} onClick={()=>onDecision('NEEDS_MORE_EVIDENCE')} className="rounded-xl bg-amber-500 py-3 font-extrabold text-white">Need more evidence</button><button disabled={busy} onClick={()=>onDecision('INVALID')} className="rounded-xl bg-rose-600 py-3 font-extrabold text-white">Mark invalid</button></div>
</div>}

function HistoryView(){const[items,setItems]=useState([]);const[busy,setBusy]=useState(false);const[error,setError]=useState('');async function load(){setBusy(true);setError('');try{setItems((await api.screenings()).items||[])}catch(e){setError(e.message)}finally{setBusy(false)}}useEffect(()=>{load()},[]);return <><PageHead kicker="Tamper-evident history" title="Verification history" text="Sensitive evidence stays encrypted off-chain. The history displays screening metadata, SHA-256 hashes and reviewer outcomes." action={<button onClick={load} className="rounded-xl border border-navy/10 bg-white px-4 py-2 text-sm font-bold">{busy?'Refreshing…':'Refresh'}</button>}/>{error&&<div className="mb-4 rounded-xl bg-rose-50 p-3 text-sm font-semibold text-rose-700">{error}</div>}<div className="overflow-hidden rounded-3xl border border-navy/10 bg-white shadow-sm"><div className="hidden grid-cols-[.7fr_1.4fr_.8fr_.8fr_1.4fr] gap-4 bg-slate-50 px-5 py-3 text-[10px] font-black uppercase tracking-wider text-slate-400 md:grid"><span>ID</span><span>Document</span><span>Risk</span><span>Status</span><span>SHA-256</span></div>{items.length===0?<div className="p-12 text-center text-sm text-slate-400">No screening history yet.</div>:items.map(x=><div key={x.id} className="grid gap-3 border-t border-slate-100 px-5 py-4 text-sm md:grid-cols-[.7fr_1.4fr_.8fr_.8fr_1.4fr] md:items-center"><span className="font-black">#{x.id}</span><span><b>{x.filename}</b><small className="block text-slate-400">{x.document_type}</small></span><span><Pill tone={x.risk_level==='High'?'red':x.risk_level==='Medium'?'amber':'green'}>{x.risk_score}</Pill></span><span className="text-xs font-bold text-slate-600">{x.status?.replaceAll('_',' ')}</span><code className="truncate text-[11px] text-navy" title={x.document_hash}>{x.document_hash}</code></div>)}</div></>}

function VerifyView(){const[hash,setHash]=useState('');const[result,setResult]=useState(null);const[error,setError]=useState('');async function go(e){e.preventDefault();setError('');setResult(null);try{setResult(await api.verify(hash.trim()))}catch(err){setError(err.message)}}return <><PageHead kicker="Public hash / status lookup" title="Verify later without exposing private evidence" text="Enter the SHA-256 hash of a document. This endpoint returns only verification status and tamper-evident record identifiers."/><div className="mx-auto max-w-3xl rounded-3xl border border-navy/10 bg-white p-6 shadow-sm"><form onSubmit={go} className="flex flex-col gap-3 sm:flex-row"><input value={hash} onChange={e=>setHash(e.target.value)} minLength={64} maxLength={64} required className="min-w-0 flex-1 rounded-xl border border-slate-200 px-4 py-3 font-mono text-sm outline-none focus:border-indigox" placeholder="SHA-256 document hash"/><button className="rounded-xl bg-ink px-6 py-3 font-extrabold text-white">Verify record</button></form>{error&&<div className="mt-4 rounded-xl bg-rose-50 p-3 text-sm text-rose-700">{error}</div>}{result&&<div className="mt-6 rounded-2xl bg-slate-50 p-5">{result.found?<div className="space-y-2"><div className="mb-4 flex items-center gap-2 text-emerald-700"><CheckCircle2/><b>Verification record found</b></div><KV label="Status" value={result.status}/><KV label="Decision" value={result.reviewer_decision||'Pending human review'}/><KV label="Event hash" value={result.latest_event_hash}/><KV label="Blockchain tx" value={result.blockchain_tx||'Optional anchoring not enabled'}/><p className="mt-4 text-xs leading-5 text-slate-500">{result.privacy_note}</p></div>:<div className="flex items-center gap-2 text-amber-700"><AlertTriangle/> No record found for this hash.</div>}</div>}</div></>}

export default function App(){const[user,setUser]=useState(null);const[authMode,setAuthMode]=useState(null);const[verifyOpen,setVerifyOpen]=useState(false);const[boot,setBoot]=useState(true);
  useEffect(()=>{if(!authStore.token){setBoot(false);return}api.me().then(x=>setUser(x.user)).catch(()=>{authStore.token=null}).finally(()=>setBoot(false))},[]);
  if(boot)return <div className="grid min-h-screen place-items-center bg-paper"><div className="text-center"><Brand/><RefreshCw className="mx-auto mt-5 animate-spin text-indigox"/></div></div>;
  if(user)return <Dashboard user={user} onLogout={()=>{authStore.token=null;setUser(null)}}/>;
  return <><Landing onAuth={setAuthMode} onPublicVerify={()=>setVerifyOpen(true)}/>{authMode&&<AuthModal mode={authMode} onClose={()=>setAuthMode(null)} onSuccess={u=>{setUser(u);setAuthMode(null)}}/>}{verifyOpen&&<PublicVerifyModal onClose={()=>setVerifyOpen(false)}/>}</>;
}
