import { useState, useEffect, useRef } from 'react';

export const useAgent = () => {
  const [messages, setMessages] = useState<{ role: 'user' | 'agent'; content: string }[]>([]);
  const [status, setStatus] = useState('System Ready');
  const [isLoading, setIsLoading] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect to your FastAPI server
    ws.current = new WebSocket('ws://localhost:8000/ws/query');

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.step === 'done') {
        setMessages((prev) => [...prev, { role: 'agent', content: data.response }]);
        setIsLoading(false);
        setStatus('Ready');
      } else {
        setStatus(data.status); // Updates status for Analytical Swarm
      }
    };

    return () => ws.current?.close();
  }, []);

  const sendText = (text: string) => {
    if (isLoading || !text) return;
    setIsLoading(true);
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    ws.current?.send(JSON.stringify({ text }));
  };

  const sendVoice = async (audioBlob: Blob) => {
    if (isLoading) return;
    setIsLoading(true);
    setStatus('Transcribing...');

    const formData = new FormData();
    // We send it as a webm (browser default) but keep the filename for the backend
    formData.append('file', audioBlob, 'voice_query.webm');

    try {
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
    } catch (e) {
      setStatus('Voice Error');
    } finally {
      setIsLoading(false);
      setStatus('Ready');
    }
  };

  return { messages, status, isLoading, sendText, sendVoice };
};