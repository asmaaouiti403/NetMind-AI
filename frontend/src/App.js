import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Plus, Trash2, Edit3, Loader2, Database, Activity, Send, ShieldCheck, Terminal, Cpu, BookOpen
} from 'lucide-react';

const App = () => {
  const [chats, setChats] = useState(() => {
    const saved = localStorage.getItem('netai_history');
    return saved ? JSON.parse(saved) : [{ id: 1, title: 'SESSION_01', messages: [] }];
  });
  const [activeChatId, setActiveChatId] = useState(chats[0]?.id || 1);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [tempTitle, setTempTitle] = useState('');
  
  const scrollRef = useRef(null);
  const activeChat = chats.find(c => c.id === activeChatId) || chats[0];

  useEffect(() => {
    localStorage.setItem('netai_history', JSON.stringify(chats));
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chats, activeChatId]);

  const handleNewChat = () => {
    const newId = Date.now();
    setChats([{ id: newId, title: `SESSION_${chats.length + 1}`, messages: [] }, ...chats]);
    setActiveChatId(newId);
  };

  const handleDelete = (e, id) => {
    e.stopPropagation();
    const filtered = chats.filter(c => c.id !== id);
    setChats(filtered.length ? filtered : [{ id: Date.now(), title: 'SESSION_01', messages: [] }]);
    if (activeChatId === id && filtered.length) setActiveChatId(filtered[0].id);
  };

  const saveRename = (id) => {
    if (!tempTitle.trim()) return setEditingId(null);
    setChats(chats.map(c => c.id === id ? { ...c, title: tempTitle.toUpperCase() } : c));
    setEditingId(null);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input };
    setChats(prev => prev.map(c => c.id === activeChatId ? { ...c, messages: [...c.messages, userMsg] } : c));
    
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      // Ensure this matches your backend IP and port exactly
      const res = await axios.post('http://127.0.0.1:8000/api/chat', { 
        question: currentInput 
      });
      
      const botMsg = { 
        role: 'bot', 
        content: res.data.answer,
        sources: res.data.sources || [] 
      };

      setChats(prev => prev.map(c => c.id === activeChatId ? { ...c, messages: [...c.messages, botMsg] } : c));
    } catch (err) {
      setChats(prev => prev.map(c => c.id === activeChatId ? { ...c, messages: [...c.messages, { role: 'bot', content: "Error: Groq Cloud Unreachable. Please check your API Key and Internet connection." }] } : c));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#0f172a] text-slate-200 font-sans overflow-hidden">
      
      {/* SIDEBAR */}
      <aside className="w-72 bg-[#1e293b] border-r border-slate-700 flex flex-col z-20 shadow-2xl">
        <div className="p-8 border-b border-slate-700">
           <h1 className="text-white font-black text-2xl uppercase italic tracking-tighter">NetMind <span className="text-blue-500">AI</span></h1>
        </div>

        <div className="p-4 space-y-2 border-b border-slate-700">
            <button onClick={handleNewChat} className="w-full p-3 bg-blue-600 hover:bg-blue-500 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all shadow-lg shadow-blue-500/20">+ New Chat</button>
        </div>

        <div className="flex-1 overflow-y-auto px-4 mt-4 custom-scrollbar">
          <p className="text-[9px] text-slate-500 font-black mb-4 uppercase tracking-[0.2em] px-2 opacity-50 italic">History</p>
          {chats.map(chat => (
            <div 
              key={chat.id} 
              onClick={() => setActiveChatId(chat.id)} 
              className={`p-3 mb-1 rounded-lg cursor-pointer flex justify-between items-center group transition-all ${activeChatId === chat.id ? 'bg-slate-700 text-blue-400 border border-blue-500/30' : 'text-slate-500 hover:bg-slate-800'}`}
            >
              <div className="flex items-center gap-3 overflow-hidden">
                <Terminal size={14} className={activeChatId === chat.id ? "text-blue-500" : "opacity-30"} />
                {editingId === chat.id ? (
                  <input autoFocus className="bg-slate-900 w-full p-1 rounded text-white text-[10px] outline-none border border-blue-500" value={tempTitle} onChange={e => setTempTitle(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && saveRename(chat.id)} onBlur={() => setEditingId(null)} />
                ) : (
                  <span className="truncate text-[11px] font-bold uppercase tracking-wider">{chat.title}</span>
                )}
              </div>
              <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100">
                 <button onClick={(e) => {e.stopPropagation(); setEditingId(chat.id); setTempTitle(chat.title);}}><Edit3 size={12} /></button>
                 <button onClick={(e) => handleDelete(e, chat.id)}><Trash2 size={12} /></button>
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* MAIN PANEL */}
      <div className="flex-1 flex flex-col relative bg-[#0f172a]">
        
        <div className="flex-1 overflow-y-auto p-8 space-y-10 custom-scrollbar">
          {activeChat.messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center opacity-20">
               <h2 className="text-5xl font-black italic uppercase tracking-tighter text-white">NetMind <span className="text-blue-500">AI</span></h2>
               <p className="text-[10px] uppercase tracking-[0.4em] mt-4 font-bold tracking-widest">Your AI expert for computer networking.</p>
            </div>
          ) : (
            activeChat.messages.map((msg, i) => (
              <div key={i} className="max-w-5xl mx-auto space-y-4">
                {msg.role === 'user' ? (
                  <div className="flex justify-end">
                    <div className="bg-blue-600 px-6 py-4 rounded-2xl rounded-tr-none text-[13px] font-bold shadow-xl border border-blue-400/20 max-w-[80%] text-white">
                      {msg.content}
                    </div>
                  </div>
                ) : (
                  <div className="flex justify-start">
                    <div className="bg-[#1e293b] border border-slate-700 p-8 rounded-3xl rounded-tl-none w-full shadow-2xl">
                      <div className="text-blue-400 font-black text-[9px] uppercase tracking-[0.4em] mb-4 border-b border-slate-700/50 pb-3 font-sans">NETMIND ANALYSIS</div>
                      <div className="text-slate-200 text-[14px] leading-relaxed whitespace-pre-wrap font-sans">{msg.content}</div>
                      
                      {msg.sources?.length > 0 && (
                        <div className="mt-6 pt-4 border-t border-slate-700/50">
                          <div className="flex items-center gap-2 text-[10px] font-bold text-blue-400 mb-2 uppercase tracking-widest">
                            <BookOpen size={12} /> Knowledge Source
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {msg.sources.map((s, j) => (
                              <a 
                                key={j} 
                                href={s.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-[10px] bg-slate-900/50 text-slate-400 px-2 py-1 rounded border border-slate-700 hover:border-blue-500 hover:text-blue-400 transition-all cursor-pointer"
                              >
                                {s.name}
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
          {loading && (
            <div className="max-w-5xl mx-auto flex items-center gap-3 text-blue-500 font-bold opacity-50 px-4">
              <Loader2 className="animate-spin" size={16} />
              <span className="text-[10px] uppercase tracking-widest">EXECUTING_GROQ_LPU...</span>
            </div>
          )}
          <div ref={scrollRef} />
        </div>

        {/* INPUT DOCK */}
        <div className="p-8 border-t border-slate-800 bg-[#0f172a]">
          <form onSubmit={handleSend} className="max-w-4xl mx-auto flex gap-4 bg-[#1e293b] p-2 rounded-2xl border border-slate-700 shadow-2xl">
            <input 
              className="flex-1 bg-transparent px-6 outline-none text-xs font-bold text-white placeholder-slate-600" 
              placeholder="Message NetMind AI..." 
              value={input} 
              onChange={e => setInput(e.target.value)} 
            />
            <button disabled={loading || !input.trim()} className="bg-blue-600 hover:bg-blue-500 text-white px-10 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest text-white shadow-lg active:scale-95 transition-all">
              {loading ? "..." : "Execute"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default App;