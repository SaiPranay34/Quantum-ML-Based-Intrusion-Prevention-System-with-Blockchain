import { useState, useEffect, useRef } from 'react';
import { Activity, ShieldAlert, CheckCircle, Box, Server, Terminal, Link as LinkIcon } from 'lucide-react';
import { useToast } from '../components/Toast';

export default function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [ledger, setLedger] = useState([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [attackMode, setAttackMode] = useState(false);
  const [recentBlocks, setRecentBlocks] = useState([]);
  
  const simulationInterval = useRef(null);
  const { addToast } = useToast();

  const fetchLedger = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('/api/ledger', {
        headers: { 'Authorization': token }
      });
      const data = await res.json();
      if (data.success) {
        setLedger(prev => {
          // Detect new records for animation
          if (prev.length > 0 && prev.length !== data.records.length) {
            const newRecords = data.records.filter(r => !prev.find(p => p.id === r.id));
            if (newRecords.length > 0) {
              const newIds = newRecords.map(r => r.id);
              setRecentBlocks(blocks => [...blocks, ...newIds]);
              setTimeout(() => {
                setRecentBlocks(blocks => blocks.filter(id => !newIds.includes(id)));
              }, 1000); // Animation duration
            }
          }
          return data.records;
        });
      }
    } catch (e) {
      console.error('Failed to fetch ledger', e);
    }
  };

  useEffect(() => {
    fetchLedger();
    const ledgerInterval = setInterval(fetchLedger, 5000);
    return () => clearInterval(ledgerInterval);
  }, []);

  const triggerAnalysis = async (isAttack) => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify({ attack_mode: isAttack })
      });
      const data = await res.json();
      
      if (data.success) {
        setLogs(prev => [data, ...prev].slice(0, 50)); 
        if (data.is_attack) {
          fetchLedger(); // Refresh ledger immediately on attack
        }
      }
    } catch (e) {
      console.error(e);
      addToast('Inference Error: QML Engine down', 'error');
    }
  };

  const toggleSimulation = () => {
    if (isSimulating) {
      clearInterval(simulationInterval.current);
      setIsSimulating(false);
      addToast('Simulation Halted', 'info');
    } else {
      setIsSimulating(true);
      addToast('Simulation Started: Monitoring network traffic', 'success');
      simulationInterval.current = setInterval(() => {
        triggerAnalysis(attackMode);
      }, 1500); // 1.5s interval
    }
  };

  // Base Block number to simulate high network activity
  const baseBlockNumber = 104429;

  return (
    <div className="p-4 md:p-8">
      <header className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-end space-y-4 md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center">
            <Terminal className="text-primary mr-3" size={32} />
            System Terminal
          </h1>
          <p className="text-gray-400 mt-1">Real-time network traffic analysis powered by QML</p>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-3 bg-white/5 px-4 py-2 rounded-xl border border-white/10">
            <span className="text-sm font-medium text-red-400">Inject Attacks</span>
            <div className="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
              <input 
                type="checkbox" 
                name="toggle" 
                id="toggle" 
                className="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer"
                checked={attackMode}
                onChange={(e) => setAttackMode(e.target.checked)}
              />
              <label 
                htmlFor="toggle" 
                className="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"
              ></label>
            </div>
          </div>
          
          <button 
            onClick={toggleSimulation}
            className={`px-6 py-2.5 rounded-xl font-medium tracking-wide transition-all shadow-lg flex items-center space-x-2 ${
              isSimulating 
                ? 'bg-red-500/80 hover:bg-red-500 text-white shadow-[0_0_15px_rgba(239,68,68,0.4)] hover:shadow-[0_0_25px_rgba(239,68,68,0.6)]' 
                : 'btn-primary'
            }`}
          >
            <Activity size={18} className={isSimulating ? 'animate-pulse' : ''} />
            <span>{isSimulating ? 'HALT SIMULATION' : 'START SIMULATION'}</span>
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Live Traffic Monitor */}
        <div className="glass-card flex flex-col h-[650px] overflow-hidden">
          <div className="p-5 border-b border-white/10 bg-black/40 flex items-center justify-between backdrop-blur-md">
            <h2 className="text-xl font-semibold text-white flex items-center tracking-wide">
              <Server className="text-primary mr-2" size={20} /> Traffic Console
            </h2>
            <div className="flex items-center space-x-2">
              <span className="relative flex h-3 w-3">
                {isSimulating && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>}
                <span className={`relative inline-flex rounded-full h-3 w-3 ${isSimulating ? 'bg-green-500' : 'bg-gray-500'}`}></span>
              </span>
              <span className="text-xs text-gray-400 uppercase tracking-widest">{isSimulating ? 'Active' : 'Standby'}</span>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-[#050508]/80 font-mono text-sm shadow-[inset_0_4px_20px_rgba(0,0,0,0.5)]">
            {logs.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-60">
                <Terminal size={48} className="mb-4 text-primary/40" />
                <p>Awaiting network packets...</p>
                <p className="text-xs mt-2">Initialize simulation to begin capturing data.</p>
              </div>
            ) : (
              logs.map((log, i) => (
                <div key={i} className={`p-3 rounded-lg border flex flex-col justify-between transition-all ${
                  log.is_attack 
                    ? 'bg-red-500/10 border-red-500/30 text-red-300 shadow-[inset_0_0_15px_rgba(239,68,68,0.1)]' 
                    : 'bg-green-500/5 border-green-500/20 text-green-300'
                }`}>
                  <div className="flex items-center space-x-3 mb-2">
                    {log.is_attack ? <ShieldAlert size={16} className="text-red-400 shrink-0" /> : <CheckCircle size={16} className="text-green-500 shrink-0" />}
                    <span className="text-white/50 text-xs">[{log.timestamp}]</span>
                    <span className="font-semibold truncate">{log.message}</span>
                  </div>
                  <div className="flex items-center justify-between text-xs mt-1">
                    <span className="text-white/40 uppercase tracking-wider text-[10px]">Confidence Score</span>
                    <div className="flex items-center space-x-2 w-1/2">
                      <div className="h-1.5 flex-1 bg-black/50 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full ${log.is_attack ? 'bg-red-500' : 'bg-green-500'}`} 
                          style={{ width: `${parseFloat(String(log.confidence || '0').replace('%', ''))}%` }}
                        ></div>
                      </div>
                      <span className="font-mono w-10 text-right opacity-90 text-[11px]">{parseFloat(String(log.confidence || '0').replace('%', '')).toFixed(2)}%</span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Immutable Ledger - Block Explorer */}
        <div className="glass-card flex flex-col h-[650px] overflow-hidden border-secondary/20 shadow-[0_4px_30px_rgba(139,92,246,0.05)]">
          <div className="p-5 border-b border-white/10 bg-black/40 flex items-center justify-between backdrop-blur-md">
            <h2 className="text-xl font-semibold text-white flex items-center tracking-wide">
              <Box className="text-secondary mr-2" size={20} /> Verified On-Chain Events
            </h2>
            <span className="px-3 py-1 bg-secondary/20 border border-secondary/30 rounded-full text-xs font-medium text-secondary-200 shadow-[0_0_10px_rgba(139,92,246,0.2)]">
              {ledger.length} Blocks Mined
            </span>
          </div>
          
          <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-[#0a0a0f]/50 to-transparent relative">
            {/* Visual background line spanning the blocks */}
            {ledger.length > 1 && (
              <div className="absolute left-[3.25rem] top-10 bottom-10 w-0.5 bg-gradient-to-b from-secondary/50 via-secondary/20 to-transparent z-0"></div>
            )}
            
            {ledger.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-60 z-10 relative">
                <LinkIcon size={48} className="mb-4 text-secondary/40" />
                <p>Genesis Block Initialized.</p>
                <p className="text-xs mt-2">Awaiting smart contract executions.</p>
              </div>
            ) : (
              ledger.map((record, idx) => {
                const isNew = recentBlocks.includes(record.id);
                return (
                  <div key={record.id} className="relative z-10 flex">
                    <div className="mr-4 flex flex-col items-center">
                      <div className={`w-12 h-12 rounded-xl border flex items-center justify-center font-bold text-xs shadow-lg transition-all duration-300 ${
                        isNew ? 'bg-secondary/20 border-secondary text-white animate-pulse-ring' : 'bg-black/60 border-secondary/30 text-secondary'
                      }`}>
                        #{baseBlockNumber + (ledger.length - idx)}
                      </div>
                    </div>
                    
                    <div className={`flex-1 p-4 rounded-xl border transition-all duration-500 hover:-translate-y-1 ${
                      isNew ? 'bg-secondary/10 border-secondary/50 shadow-[0_0_20px_rgba(139,92,246,0.15)]' : 'bg-black/40 border-white/5 hover:border-white/20'
                    }`}>
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Cryptographic Hash</p>
                          <p className={`font-mono text-sm text-gray-300 ${isNew ? 'animate-hash' : ''}`}>
                            {record.txHash}
                          </p>
                        </div>
                        <span className="text-xs text-gray-500 whitespace-nowrap bg-black/40 px-2 py-1 rounded">
                          {new Date(record.timestamp * 1000).toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center border-t border-white/5 pt-3 mt-1">
                        <div className="flex items-center">
                          <span className="text-[10px] text-gray-500 uppercase tracking-widest mr-2">Execution Log:</span>
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-500/20 text-red-400 border border-red-500/20">
                            {record.attackType} Logged
                          </span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-[10px] text-gray-500 uppercase tracking-widest">Conf.</span>
                          <span className="font-mono text-xs font-semibold text-secondary-100">{record.confidence}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
