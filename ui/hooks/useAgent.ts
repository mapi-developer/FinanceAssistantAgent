import { useState, useEffect, useRef } from 'react';

export const useAgent = () => {
  const [messages, setMessages] = useState<{ role: 'user' | 'agent'; content: string }[]>([]);
  const [status, setStatus] = useState('System Ready');
  const [isLoading, setIsLoading] = useState(false); // New state to lock requests
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws/query');

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.step === 'done') {
        setStatus('Analysis Complete');
        setMessages((prev) => [...prev, { role: 'agent', content: data.response }]);
        setIsLoading(false); // Unlock when synthesis is done
      } else {
        setStatus(data.status);
      }
    };

    return () => ws.current?.close();
  }, []);

  const sendText = (text: string) => {
    if (isLoading || !text) return; // Prevent new request if busy
    setIsLoading(true);
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    ws.current?.send(JSON.stringify({ text }));
  };

  const sendVoice = async (audioBlob: Blob) => {
    if (isLoading) return; // Prevent voice upload if already processing
    setIsLoading(true);
    setStatus('Transcribing Voice...');
    
    const formData = new FormData();
    formData.append('file', audioBlob, 'voice_query.wav');

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
    } catch (error) {
      setStatus('System Error');
    } finally {
      setIsLoading(false); // Unlock after synthesis & delivery
      setStatus('System Ready');
    }
  };

  return { messages, status, isLoading, sendText, sendVoice };
};