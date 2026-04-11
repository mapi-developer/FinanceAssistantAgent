'use client';
import { useState, useRef } from 'react';
import { Mic, Send, Activity, ShieldCheck, Sparkles } from 'lucide-react';
import { useAgent } from '@/hooks/useAgent';

export default function LandingPage() {
  const { messages, status, isLoading, sendText, sendVoice } = useAgent();
  const [input, setInput] = useState('');
  const [recording, setRecording] = useState(false);
  
  // Refs for managing recording state and preventing leaks
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const toggleRecording = async () => {
    if (isLoading) return;

    if (!recording) {
      // START RECORDING
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        
        // Use browser default format (safer than forcing wav)
        mediaRecorder.current = new MediaRecorder(stream);
        const chunks: BlobPart[] = [];
        
        mediaRecorder.current.ondataavailable = (e) => chunks.push(e.data);
        mediaRecorder.current.onstop = () => {
          sendVoice(new Blob(chunks, { type: 'audio/webm' }));
          // CRITICAL: Stop the microphone hardware
          stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.current.start();
        setRecording(true);
      } catch (err) {
        console.error("Mic access denied", err);
      }
    } else {
      // STOP AND SEND
      mediaRecorder.current?.stop();
      setRecording(false);
    }
  };

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-[#02010a] font-sans">
      
      {/* Animated Background Blobs (Purple & Yellow) */}
      <div className="absolute -top-[20%] -left-[10%] w-[80vw] h-[80vw] bg-purple-900/20 blur-[120px] rounded-full animate-pulse" />
      <div className="absolute -bottom-[10%] -right-[10%] w-[60vw] h-[60vw] bg-yellow-500/5 blur-[120px] rounded-full" />

      {/* Full-Height Sidebar */}
      <aside className="w-80 h-full border-r border-white/5 bg-black/40 backdrop-blur-2xl p-10 flex flex-col z-10">
        <div className="flex items-center gap-3 mb-16">
          <div className="w-4 h-4 rounded-full bg-yellow-500 shadow-[0_0_15px_rgba(250,204,21,0.6)]" />
          <h1 className="text-2xl font-bold text-white tracking-tighter">AaaS <span className="text-yellow-500">Finance</span></h1>
        </div>
        <nav className="space-y-8 flex-1">
          <div className="flex items-center gap-4 text-purple-400 font-bold uppercase tracking-widest text-[10px]">
            <Activity size={18} /> Swarm Analytics
          </div>
          <div className="flex items-center gap-4 text-slate-500 font-bold uppercase tracking-widest text-[10px]">
            <ShieldCheck size={18} /> Risk Protocols
          </div>
        </nav>
        <div className="text-[10px] text-slate-600 uppercase tracking-widest">
           Status: <span className="text-emerald-500">Connected</span>
        </div>
      </aside>

      {/* Main Chat: Stretched Whole Page */}
      <main className="flex-1 flex flex-col h-full relative z-10">
        <header className="p-8 px-12 border-b border-white/5 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Sparkles size={20} className="text-yellow-500" />
            <h2 className="text-xl font-medium text-white/80">Agent Intelligence</h2>
          </div>
          <div className={`px-5 py-2 rounded-full text-[10px] font-black uppercase tracking-widest transition-all
            ${isLoading ? 'bg-purple-600 text-white animate-pulse' : 'bg-white/5 text-yellow-500 border border-yellow-500/30'}`}>
            {status}
          </div>
        </header>

        {/* Chat History Container */}
        <div className="flex-1 overflow-y-auto p-12 px-24 space-y-8 scroll-smooth">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`p-6 px-8 rounded-3xl max-w-[75%] text-base shadow-2xl
                ${m.role === 'user' 
                  ? 'bg-gradient-to-br from-purple-600 to-purple-900 text-white rounded-tr-none' 
                  : 'bg-white/5 backdrop-blur-md border border-white/10 text-slate-200 rounded-tl-none'}`}>
                {m.content}
              </div>
            </div>
          ))}
        </div>

        {/* Pinned Pill Input Area */}
        <div className="p-10 px-24 bg-gradient-to-t from-black to-transparent">
          <div className={`flex items-center gap-4 p-3 px-6 bg-white/5 backdrop-blur-xl border border-white/10 rounded-full transition-all
            ${isLoading ? 'opacity-30 pointer-events-none' : 'hover:border-purple-500/50 hover:shadow-[0_0_30px_rgba(147,51,234,0.1)]'}`}>
            <input
              disabled={isLoading}
              className="flex-1 bg-transparent outline-none text-lg text-white placeholder:text-slate-600"
              placeholder="Query tickers or latest news..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (sendText(input), setInput(''))}
            />
            <button 
              onClick={toggleRecording}
              className={`p-4 rounded-full transition-all ${recording ? 'bg-red-500 text-white animate-pulse' : 'text-yellow-500 hover:bg-white/10'}`}
            >
              <Mic size={24} />
            </button>
            <button 
              disabled={isLoading || !input}
              onClick={() => { sendText(input); setInput(''); }}
              className="bg-yellow-500 text-black p-4 px-8 rounded-full font-bold hover:bg-yellow-400 disabled:bg-slate-800 disabled:text-slate-600"
            >
              <Send size={24} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}