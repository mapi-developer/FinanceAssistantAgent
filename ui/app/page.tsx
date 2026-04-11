'use client';
import { useState, useRef } from 'react';
import { Mic, Send, Activity, ShieldCheck, Sparkles, LayoutDashboard } from 'lucide-react';
import { useAgent } from '@/hooks/useAgent';

export default function LandingPage() {
  const { messages, status, isLoading, sendText, sendVoice } = useAgent();
  const [input, setInput] = useState('');
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);

  const toggleRecording = async () => {
    if (isLoading) return;
    if (!recording) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      const chunks: BlobPart[] = [];
      mediaRecorder.current.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.current.onstop = () => sendVoice(new Blob(chunks, { type: 'audio/wav' }));
      mediaRecorder.current.start();
      setRecording(true);
    } else {
      mediaRecorder.current?.stop();
      setRecording(false);
    }
  };

  return (
    <div className="relative flex h-screen w-screen overflow-hidden font-sans">
      
      {/* --- Animated Cosmic Background --- */}
      <div className="bg-blob w-[80vw] h-[80vw] -top-[20%] -left-[10%] bg-purple-900/30" />
      <div className="bg-blob w-[70vw] h-[70vw] -bottom-[10%] -right-[10%] bg-yellow-900/10" style={{ animationDelay: '-7s' }} />

      {/* Sidebar: Edge-to-Edge Minimal Sidebar */}
      <aside className="w-80 h-full border-r border-white/5 bg-black/20 backdrop-blur-3xl p-10 flex flex-col">
        <div className="flex items-center gap-3 mb-16">
          <div className="w-4 h-4 rounded-full bg-yellow-500 shadow-[0_0_15px_rgba(250,204,21,0.5)]" />
          <h1 className="text-2xl font-bold tracking-tight text-white">
            AaaS <span className="text-yellow-500">Finance</span>
          </h1>
        </div>
        
        <nav className="space-y-8 text-sm flex-1">
          <div className="flex items-center gap-4 text-purple-400 cursor-pointer hover:text-purple-300 transition-colors">
            <Activity size={20}/>
            <span className="font-semibold uppercase tracking-widest text-[11px]">Intelligence Swarm</span>
          </div>
          <div className="flex items-center gap-4 text-slate-500 cursor-pointer hover:text-slate-300 transition-colors">
            <ShieldCheck size={20}/> 
            <span className="font-semibold uppercase tracking-widest text-[11px]">Risk Protocols</span>
          </div>
        </nav>

        <div className="pt-8 border-t border-white/5 text-[10px] text-slate-600 uppercase tracking-[0.2em] space-y-2">
          <p>Kafka Node: <span className="text-emerald-500">Synced</span></p>
          <p>Llama 3 Vetting: <span className="text-purple-500">Active</span></p>
        </div>
      </aside>

      {/* Main Interface: Stretched for Whole Page */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        <header className="flex justify-between items-center p-8 px-12 border-b border-white/5 bg-black/10">
          <div className="flex items-center gap-3">
             <Sparkles size={20} className="text-yellow-500 animate-pulse" />
             <h2 className="text-xl font-medium text-white/80">Agent Assistant</h2>
          </div>
          
          <div className={`px-5 py-2 rounded-full text-[10px] font-black uppercase tracking-widest shadow-2xl transition-all
            ${isLoading ? 'bg-purple-600 text-white animate-pulse scale-105' : 'bg-white/5 text-yellow-500 border border-yellow-500/30'}`}>
            {status}
          </div>
        </header>

        {/* Chat History: Fills viewport */}
        <div className="flex-1 overflow-y-auto space-y-8 p-12 px-20 custom-scrollbar">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-slate-700 animate-in fade-in duration-1000">
              <LayoutDashboard size={48} className="mb-4 opacity-20" />
              <p className="italic text-lg">Awaiting financial query...</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2`}>
              <div className={`p-6 px-8 rounded-3xl max-w-[70%] text-base leading-relaxed shadow-2xl
                ${m.role === 'user' 
                  ? 'bg-gradient-to-br from-purple-600 to-purple-900 text-white rounded-tr-none' 
                  : 'glass-panel text-slate-100 rounded-tl-none border-purple-500/20'}`}>
                {m.content}
              </div>
            </div>
          ))}
        </div>

        {/* Input Bar: Full width pinned at bottom */}
        <div className="p-8 px-20 bg-gradient-to-t from-black/50 to-transparent">
          <div className={`glass-panel p-3 px-6 rounded-full flex items-center gap-4 transition-all duration-700
            ${isLoading ? 'opacity-30 blur-[2px]' : 'hover:border-purple-500/50 hover:shadow-[0_0_40px_rgba(147,51,234,0.1)]'}`}>
            
            <input
              disabled={isLoading}
              className="flex-1 bg-transparent outline-none text-lg text-white placeholder:text-slate-600 disabled:cursor-not-allowed"
              placeholder={isLoading ? "Swarm is validating data..." : "Enter ticker or news request (e.g. 'AAPL volatility')"}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !isLoading && (sendText(input), setInput(''))}
            />
            
            <button 
              onClick={toggleRecording}
              className={`p-4 rounded-full transition-all 
                ${recording ? 'bg-red-500 text-white scale-110 shadow-[0_0_20px_rgba(239,68,68,0.4)]' : 'text-yellow-500 hover:bg-white/5'}`}
            >
              <Mic size={24} />
            </button>
            
            <button 
              disabled={isLoading || !input}
              onClick={() => { sendText(input); setInput(''); }}
              className="bg-yellow-500 text-black p-4 px-8 rounded-full font-bold hover:bg-yellow-400 transition-all hover:scale-105 disabled:bg-slate-900 disabled:text-slate-700"
            >
              <Send size={24} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}