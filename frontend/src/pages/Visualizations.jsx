import { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { BarChart2, ShieldAlert, Cpu } from 'lucide-react';
import { useToast } from '../components/Toast';

export default function Visualizations() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch('/api/stats', {
          headers: { 'Authorization': token }
        });
        const data = await res.json();
        if (data.success) {
          setStats(data);
        }
      } catch (e) {
        console.error('Failed to fetch stats', e);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    // Refresh stats every 10 seconds
    const interval = setInterval(fetchStats, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-8">
        <div className="h-10 w-1/3 bg-white/5 animate-pulse rounded-lg"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="h-32 bg-white/5 animate-pulse rounded-xl"></div>
          <div className="h-32 bg-white/5 animate-pulse rounded-xl"></div>
          <div className="h-32 bg-white/5 animate-pulse rounded-xl"></div>
        </div>
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          <div className="xl:col-span-2 h-[450px] bg-white/5 animate-pulse rounded-xl"></div>
          <div className="h-[450px] bg-white/5 animate-pulse rounded-xl"></div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-8 flex flex-col items-center justify-center h-[80vh] text-center">
        <ShieldAlert size={64} className="text-red-500/50 mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Telemetry Unavailable</h2>
        <p className="text-gray-400">Failed to load analytics data from the network layer.</p>
        <button onClick={() => window.location.reload()} className="mt-6 btn-outline">Retry Connection</button>
      </div>
    );
  }

  // Colors for Pie Chart
  const COLORS = ['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6'];

  return (
    <div className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white tracking-tight flex items-center">
          <BarChart2 className="text-accent mr-3" size={32} /> 
          Telemetry & Analytics
        </h1>
        <p className="text-gray-400 mt-1">Aggregated insight into system stability and QML performance</p>
      </header>
      
      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="glass-card p-6 border-l-4 border-l-red-500">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-1">Total Threats Logged</p>
              <h3 className="text-4xl font-bold text-white">{stats.total_attacks_logged}</h3>
            </div>
            <div className="p-3 bg-red-500/10 rounded-xl">
              <ShieldAlert className="text-red-500" size={24} />
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 border-l-4 border-l-primary">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-1">QML Inference Speed</p>
              <h3 className="text-4xl font-bold text-white">42 <span className="text-xl text-gray-500">ms/pkt</span></h3>
            </div>
            <div className="p-3 bg-primary/10 rounded-xl">
              <Cpu className="text-primary" size={24} />
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 border-l-4 border-l-secondary">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-1">Blockchain Sync</p>
              <h3 className="text-4xl font-bold text-white">100<span className="text-xl text-gray-500">%</span></h3>
            </div>
            <div className="p-3 bg-secondary/10 rounded-xl">
              <div className="w-6 h-6 rounded-full bg-secondary/20 border-2 border-secondary animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        {/* Area Chart - Network Traffic Volume */}
        <div className="xl:col-span-2 glass-card p-6">
          <h2 className="text-xl font-semibold text-white mb-6">Network Traffic Volume (1H Interval)</h2>
          <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats.time_series} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorNormal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorAttacks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                <XAxis dataKey="time" stroke="#ffffff40" tick={{fill: '#ffffff80', fontSize: 12}} />
                <YAxis stroke="#ffffff40" tick={{fill: '#ffffff80', fontSize: 12}} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#12121c', borderColor: '#ffffff20', borderRadius: '8px' }}
                  itemStyle={{ fontSize: '14px' }}
                />
                <Legend />
                <Area type="monotone" dataKey="normal" name="Normal Traffic" stroke="#3b82f6" fillOpacity={1} fill="url(#colorNormal)" strokeWidth={2} />
                <Area type="monotone" dataKey="attacks" name="Detected Intrusions" stroke="#ef4444" fillOpacity={1} fill="url(#colorAttacks)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie Chart - Attack Distribution */}
        <div className="glass-card p-6 flex flex-col">
          <h2 className="text-xl font-semibold text-white mb-2">Threat Distribution</h2>
          <p className="text-sm text-gray-400 mb-6">Classification breakdown of blocked patterns</p>
          <div className="flex-1 min-h-[300px] w-full relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.attack_types}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {stats.attack_types.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#12121c', borderColor: '#ffffff20', borderRadius: '8px', border: 'none', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.5)' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend 
                  layout="vertical" 
                  verticalAlign="bottom"
                  align="center"
                  wrapperStyle={{ paddingTop: '20px' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none pb-8">
              <span className="block text-3xl font-bold text-white leading-none">{stats.total_attacks_logged}</span>
              <span className="text-xs text-gray-500 font-medium tracking-wider uppercase">Total</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
