import { useState, useEffect, useRef } from 'react';

export const useAgent = () => {
  const [messages, setMessages] = useState<{ role: 'user' | 'agent'; content: string }[]>([]);
  const [status, setStatus] = useState('System Ready');
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect to your FastAPI WebSocket handler
    ws.current = new WebSocket('ws://localhost:8000/ws/query');

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.step === 'done') {
        setStatus('Analysis Complete');
        setMessages((prev) => [...prev, { role: 'agent', content: data.response }]);
      } else {
        // Displays "🧠 Parsing intent..." or "📊 Swarm activated..."
        setStatus(data.status);
      }
    };

    return () => ws.current?.close();
  }, []);

  const sendText = (text: string) => {
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    ws.current?.send(JSON.stringify({ text }));
  };

  const sendVoice = async (audioBlob: Blob) => {
    setStatus('Transcribing Voice...');
    const formData = new FormData();
    formData.append('file', audioBlob, 'voice_query.wav');

    // POST to the ElevenLabs transcription endpoint
    const res = await fetch('http://localhost:8000/api/v1/query/voice', {
      method: 'POST',
      body: formData,
    });
    
    const result = await res.json();
    setMessages((prev) => [
      ...prev,
      { role: 'user', content: `🎤 ${result.transcription}` },
      { role: 'agent', content: result.response }
    ]);
  };

  return { messages, status, sendText, sendVoice };
};