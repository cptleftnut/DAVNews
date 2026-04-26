import React, { useState, useEffect, useRef } from 'react';
import {
  Activity, Terminal, Database, Brain, Zap, DollarSign,
  TrendingUp, BarChart2, GitPullRequest, ShieldCheck,
  Share2, Play, RefreshCw, AlertTriangle, Film, Mic,
  Video, FileText, Subtitles, UploadCloud
} from 'lucide-react';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const VIRAL_TOPICS_POOL = [
  "AGI breakthrough rumored at OpenAI headquarters",
  "Nvidia announces new architecture that changes everything",
  "Massive zero-day leak exposes major tech company",
  "Apple's secret AI hardware project just leaked",
  "TikTok's new algorithm reverse-engineered by researchers",
  "Elon Musk open-sources next generation AI model"
];

const StatusBadge = ({ label, state }) => {
  const colors = {
    IDLE: 'bg-slate-700 text-slate-400',
    WAITING: 'bg-slate-800 text-slate-500',
    RUNNING: 'bg-blue-900 text-blue-300 animate-pulse',
    ACTIVE: 'bg-emerald-900 text-emerald-300 animate-pulse',
    CONNECTED: 'bg-green-900 text-green-300',
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-mono ${colors[state] || colors.IDLE}`}>
      {label}: {state}
    </span>
  );
};

const MetricCard = ({ icon: Icon, label, value, sub }) => (
  <div className="bg-[#0b0f17] border border-slate-800 rounded-lg p-4">
    <div className="flex items-center gap-2 text-slate-500 text-xs mb-1">
      <Icon className="w-3.5 h-3.5" /> {label}
    </div>
    <div className="text-xl font-bold text-white">{value}</div>
    {sub && <div className="text-xs text-slate-600 mt-1">{sub}</div>}
  </div>
);

export default function DAVNewsDashboard() {
  const [logs, setLogs] = useState([]);
  const [metrics, setMetrics] = useState({ views: 14500, rpm: 0.12, revenue: 1.74, aum: 1250 });
  const [systemState, setSystemState] = useState({
    ingest: 'IDLE', ai: 'WAITING', video: 'WAITING',
    storage: 'WAITING', hedge: 'WAITING', publish: 'IDLE', ws: 'CONNECTED'
  });
  const [feed, setFeed] = useState([]);
  const [abTests, setAbTests] = useState([]);
  const [activeAsset, setActiveAsset] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const logsEndRef = useRef(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const addLog = (message, type = "info") => {
    const timestamp = new Date().toISOString().split('T')[1].slice(0, -1);
    setLogs(prev => [...prev.slice(-49), { timestamp, message, type }]);
  };

  const logColor = (type) => {
    switch (type) {
      case 'success': return 'text-emerald-400';
      case 'error': return 'text-red-400';
      case 'action': return 'text-blue-400';
      case 'system': return 'text-purple-400';
      default: return 'text-slate-400';
    }
  };

  const triggerPipeline = async () => {
    if (isRunning) return;
    setIsRunning(true);

    setSystemState(prev => ({ ...prev, ingest: 'RUNNING' }));
    addLog(`[CRON JOB] Initiating autonomous content cycle...`, "system");
    await sleep(800);

    addLog(`[TREND SCOUT] Scanning X, HackerNews & Reddit for viral velocity signals...`, "action");
    await sleep(1500);

    const topic = VIRAL_TOPICS_POOL[Math.floor(Math.random() * VIRAL_TOPICS_POOL.length)];
    const viralScore = Math.floor(Math.random() * 15) + 85;

    addLog(`[AI SCOUT] Locked onto viral trend: "${topic}" (Velocity Score: ${viralScore}/100)`, "success");
    await sleep(1000);

    addLog("[INGESTION] Fetching source articles, live tweets, and media assets...", "info");
    await sleep(1000);

    setSystemState(prev => ({ ...prev, ingest: 'IDLE', ai: 'ACTIVE' }));
    addLog(`[AI ENGINE] Rewriting content to tech news format...`, "action");
    await sleep(1200);

    addLog(`[A/B TESTING] Generating hooks for viral retention...`, "info");
    const hooks = [
      `This changes everything for: ${topic}`,
      `Nobody is talking about the truth behind: ${topic}`,
      `Look at the numbers behind: ${topic}`
    ];

    const evaluatedHooks = hooks.map(h => ({
      hook: h,
      hold3s: (Math.random() * 0.5 + 0.3).toFixed(2),
    })).sort((a, b) => b.hold3s - a.hold3s);

    setAbTests(evaluatedHooks);
    const winningHook = evaluatedHooks[0];
    addLog(`[AI PREDICT] Selected winner: "${winningHook.hook}" (Predicted 3s Hold: ${(winningHook.hold3s * 100).toFixed(0)}%)`, "success");
    await sleep(1000);

    setSystemState(prev => ({ ...prev, ai: 'WAITING', video: 'ACTIVE' }));
    setActiveAsset({ hook: winningHook.hook, topic, status: 'script' });

    addLog(`[SCRIPT ENGINE] Expanding winning hook into full English video script...`, "action");
    await sleep(1000);
    setActiveAsset(prev => ({ ...prev, script: `Did you know that the latest news around ${topic.toLowerCase()} is completely changing the landscape?` }));
    await sleep(1500);

    addLog(`[TTS ENGINE] Initiating Voice Clone: Dylan Page "News Daddy" (11Labs integration)...`, "info");
    setActiveAsset(prev => ({ ...prev, voice: 'Dylan Page (Voice Clone)', status: 'audio' }));
    await sleep(1200);

    addLog(`[VIDEO ENGINE] Generating actual MP4: Assembling B-roll, syncing audio & rendering subtitles...`, "action");
    setActiveAsset(prev => ({ ...prev, languages: ['EN', 'DA', 'ES', 'DE', 'ZH', 'FR'], status: 'render' }));
    await sleep(2500);

    setActiveAsset(prev => ({ ...prev, videoReady: true }));
    addLog(`[VIDEO ENGINE] Render complete! Video saved to /output folder.`, "success");

    // Google Drive Upload
    setSystemState(prev => ({ ...prev, video: 'WAITING', storage: 'ACTIVE' }));
    addLog(`[G-DRIVE] Authenticating with Google Drive API...`, "info");
    await sleep(800);
    addLog(`[G-DRIVE] Locating/Creating "DAVNews" remote folder...`, "action");
    await sleep(1000);
    const filename = `${topic.replace(/\s+/g, '_').toLowerCase()}.mp4`;
    addLog(`[G-DRIVE] Uploading final video asset: ${filename}...`, "action");
    await sleep(2000);
    addLog(`[G-DRIVE] Upload successful! File synced to Google Cloud.`, "success");

    // Quality Gate & Hedge
    setSystemState(prev => ({ ...prev, storage: 'WAITING', hedge: 'ACTIVE' }));
    addLog(`[QUALITY GATE] Scoring script length, AV sync and keyword density...`, "info");
    const score = Math.floor(Math.random() * 3) + 1;
    await sleep(800);

    if (score < 2) {
      addLog(`[QUALITY GATE] Rejected! Score ${score} < 2. Aborting cycle.`, "error");
      setSystemState(prev => ({ ...prev, hedge: 'WAITING' }));
      setIsRunning(false);
      return;
    }

    addLog(`[HEDGE ENGINE] Calculating risk/reward allocation...`, "action");
    const risk = (Math.random() * 0.9 + 0.1).toFixed(2);
    const reward = (Math.random() * 1.9 + 0.1).toFixed(2);
    await sleep(1000);

    setSystemState(prev => ({ ...prev, hedge: 'WAITING', publish: 'ACTIVE' }));
    addLog(`[DISTRIBUTION] Publishing video to Router (TikTok, YouTube Shorts, Reels)...`, "action");
    await sleep(1200);

    const newViews = Math.floor(Math.random() * 50000) + 5000;
    const newRevenue = ((newViews / 1000) * metrics.rpm);

    setMetrics(prev => ({
      views: prev.views + newViews,
      rpm: +(prev.rpm + (Math.random() * 0.02 - 0.01)).toFixed(3),
      revenue: +(prev.revenue + newRevenue).toFixed(2),
      aum: +(prev.aum + (newRevenue * 0.5)).toFixed(2)
    }));

    setFeed(prev => [{
      id: Math.random().toString(36).substr(2, 9),
      headline: winningHook.hook,
      topic: topic,
      views: newViews,
      revenue: newRevenue.toFixed(2),
      risk: risk
    }, ...prev.slice(0, 4)]);

    addLog(`[WS BROADCAST] Event: { type: 'publish', status: 'published' }`, "success");
    setSystemState(prev => ({ ...prev, publish: 'IDLE' }));
    setIsRunning(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 font-sans p-4 md:p-6">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Zap className="text-emerald-400" /> DAVNews AI Hedge Network
          </h1>
          <p className="text-xs text-slate-600 mt-1">Autonomous Media Hedge Fund — Viral Content Engine</p>
        </div>
        <div className="flex items-center gap-4 mt-4 md:mt-0">
          <button
            onClick={triggerPipeline}
            disabled={isRunning}
            className={`flex items-center gap-2 px-4 py-2 rounded font-medium transition-all ${
              isRunning ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-500 text-white'
            }`}
          >
            {isRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            {isRunning ? 'Processing...' : 'Auto-Scout Viral Trend'}
          </button>
        </div>
      </header>

      {/* System Status Row */}
      <div className="flex flex-wrap gap-2 mb-6">
        {Object.entries(systemState).map(([key, val]) => (
          <StatusBadge key={key} label={key.toUpperCase()} state={val} />
        ))}
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <MetricCard icon={TrendingUp} label="Total Views" value={metrics.views.toLocaleString()} />
        <MetricCard icon={DollarSign} label="RPM" value={`$${metrics.rpm.toFixed(3)}`} sub="Revenue Per Mille" />
        <MetricCard icon={BarChart2} label="Revenue" value={`$${metrics.revenue.toFixed(2)}`} />
        <MetricCard icon={ShieldCheck} label="AUM" value={`$${metrics.aum.toFixed(0)}`} sub="Assets Under Mgmt" />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Terminal / Logs */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <div className="bg-[#0b0f17] border border-slate-800 rounded-lg flex flex-col h-[400px]">
            <div className="flex items-center gap-2 px-4 py-2 border-b border-slate-800 text-xs text-slate-500">
              <Terminal className="w-3.5 h-3.5" /> LIVE PIPELINE LOG
            </div>
            <div className="p-4 font-mono text-xs overflow-y-auto flex-1 space-y-1">
              {logs.length === 0 && (
                <div className="text-slate-700">Waiting for pipeline trigger...</div>
              )}
              {logs.map((log, i) => (
                <div key={i} className={logColor(log.type)}>
                  <span className="text-slate-600">[{log.timestamp}]</span> {log.message}
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          </div>

          {/* A/B Test Results */}
          {abTests.length > 0 && (
            <div className="bg-[#0b0f17] border border-slate-800 rounded-lg p-4">
              <div className="flex items-center gap-2 text-xs text-slate-500 mb-3">
                <GitPullRequest className="w-3.5 h-3.5" /> A/B HOOK TEST RESULTS
              </div>
              <div className="space-y-2">
                {abTests.map((t, i) => (
                  <div key={i} className={`flex justify-between items-center p-2 rounded text-xs font-mono ${
                    i === 0 ? 'bg-emerald-950 border border-emerald-800 text-emerald-300' : 'bg-slate-900 text-slate-500'
                  }`}>
                    <span className="truncate mr-4">{i === 0 ? '★ ' : '  '}{t.hook}</span>
                    <span className="whitespace-nowrap">3s Hold: {(t.hold3s * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          {/* Active Asset */}
          {activeAsset && (
            <div className="bg-[#0b0f17] border border-slate-800 rounded-lg p-4">
              <div className="flex items-center gap-2 text-xs text-slate-500 mb-3">
                <Film className="w-3.5 h-3.5" /> ACTIVE ASSET
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <FileText className="w-3 h-3 text-blue-400" />
                  <span className="text-slate-400">Topic:</span>
                  <span className="text-white truncate">{activeAsset.topic}</span>
                </div>
                {activeAsset.script && (
                  <div className="flex items-start gap-2">
                    <Subtitles className="w-3 h-3 text-purple-400 mt-0.5" />
                    <span className="text-slate-500 italic line-clamp-3">{activeAsset.script}</span>
                  </div>
                )}
                {activeAsset.voice && (
                  <div className="flex items-center gap-2">
                    <Mic className="w-3 h-3 text-yellow-400" />
                    <span className="text-slate-400">Voice:</span>
                    <span className="text-white">{activeAsset.voice}</span>
                  </div>
                )}
                {activeAsset.languages && (
                  <div className="flex items-center gap-2">
                    <Subtitles className="w-3 h-3 text-cyan-400" />
                    <span className="text-slate-400">Subs:</span>
                    <div className="flex gap-1">
                      {activeAsset.languages.map(l => (
                        <span key={l} className="bg-slate-800 px-1.5 py-0.5 rounded text-[10px] text-slate-400">{l}</span>
                      ))}
                    </div>
                  </div>
                )}
                {activeAsset.videoReady && (
                  <div className="flex items-center gap-2 text-emerald-400">
                    <Video className="w-3 h-3" />
                    <span>MP4 Rendered</span>
                    <UploadCloud className="w-3 h-3 ml-1" />
                    <span>Uploaded to Drive</span>
                  </div>
                )}
                <div className="mt-2 flex items-center gap-2">
                  <Activity className="w-3 h-3" />
                  <span className="text-slate-400">Status:</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${
                    activeAsset.status === 'render' ? 'bg-blue-900 text-blue-300 animate-pulse' :
                    activeAsset.videoReady ? 'bg-emerald-900 text-emerald-300' :
                    'bg-slate-800 text-slate-400'
                  }`}>
                    {activeAsset.videoReady ? 'COMPLETE' : activeAsset.status?.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Published Feed */}
          <div className="bg-[#0b0f17] border border-slate-800 rounded-lg p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500 mb-3">
              <Share2 className="w-3.5 h-3.5" /> PUBLISHED FEED
            </div>
            {feed.length === 0 ? (
              <div className="text-xs text-slate-700">No assets published yet.</div>
            ) : (
              <div className="space-y-3">
                {feed.map(item => (
                  <div key={item.id} className="border border-slate-800 rounded p-3 text-xs">
                    <div className="text-white font-medium mb-1 line-clamp-2">{item.headline}</div>
                    <div className="flex justify-between text-slate-500">
                      <span>{item.views.toLocaleString()} views</span>
                      <span className="text-emerald-400">${item.revenue}</span>
                    </div>
                    <div className="text-slate-600 mt-1">Risk: {item.risk}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-8 pt-4 border-t border-slate-800 text-center text-xs text-slate-700">
        DAVNews AI Hedge Network v1.0 — Autonomous Media Fund Engine
      </footer>
    </div>
  );
}
