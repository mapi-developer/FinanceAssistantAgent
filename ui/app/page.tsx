'use client';
import { useState, useRef } from 'react';
import { Mic, Send, Activity, ShieldCheck } from 'lucide-react';
import { useAgent } from '@/hooks/useAgent';

export default function LandingPage() {
  const { messages, status, sendText, sendVoice } = useAgent();
  const [input, setInput] = useState('');
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);

  const toggleRecording = async () => {
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
    <div className="flex h-screen bg-slate-950 text-slate-200">
      {/* Sidebar: System Specs [cite: 9, 65] */}
      <aside className="w-72 bg-slate-900 border-r border-slate-800 p-8">
        <h1 className="text-xl font-bold text-blue-400 mb-10">AaaS Platform</h1>
        <div className="space-y-6 text-sm">
          <div className="flex items-center gap-3"><Activity size={16}/> Analytical Swarm</div>
          <div className="flex items-center gap-3"><ShieldCheck size={16}/> Risk Vetting Active</div>
          <div className="pt-10 border-t border-slate-800 text-slate-500">
            <p>Kafka Ingestion: 30m Sync</p>
            <p>Engine: Llama 3 (Local)</p>
          </div>
        </div>
      </aside>

      {/* Main Interface [cite: 59] */}
      <main className="flex-1 flex flex-col p-10 max-w-5xl mx-auto w-full">
        <header className="flex justify-between items-center mb-10">
          <h2 className="text-2xl font-semibold">Intelligence Dashboard</h2>
          <div className="bg-slate-800 px-4 py-1 rounded-full text-xs animate-pulse">
            {status}
          </div>
        </header>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-4 custom-scrollbar">
          {messages.map((m, i) => (
            <div key={i} className={`p-4 rounded-xl max-w-[85%] ${
              m.role === 'user' ? 'bg-blue-600 ml-auto' : 'bg-slate-800 border border-slate-700'
            }`}>
              <p className="text-sm leading-relaxed">{m.content}</p>
            </div>
          ))}
        </div>

        {/* Input Bar [cite: 50] */}
        <div className="mt-8 flex gap-4 bg-slate-900 p-3 rounded-2xl border border-slate-800">
          <input
            className="flex-1 bg-transparent outline-none px-4 text-sm"
            placeholder="Query market metrics (e.g., 'Analyze AAPL volatility')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && (sendText(input), setInput(''))}
          />
          <button 
            onClick={toggleRecording}
            className={`p-3 rounded-xl transition ${recording ? 'bg-red-500 animate-pulse' : 'hover:bg-slate-800'}`}
          >
            <Mic size={20} />
          </button>
          <button 
            onClick={() => { sendText(input); setInput(''); }}
            className="bg-blue-600 p-3 rounded-xl hover:bg-blue-500 transition"
          >
            <Send size={20} />
          </button>
        </div>
      </main>
    </div>
  );
}