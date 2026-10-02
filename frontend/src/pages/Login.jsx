import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Shield, Eye, EyeOff } from 'lucide-react';
import { useToast } from '../components/Toast';

export default function Login({ setAuth }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { addToast } = useToast();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();
      
      if (data.success) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', data.username);
        setAuth(true);
        addToast('Uplink established. Authenticated.', 'success');
        navigate('/dashboard');
      } else {
        addToast(data.message || 'Login failed', 'error');
      }
    } catch (err) {
      addToast('Unable to connect to Quantum Network', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative px-4">
      {/* Abstract Background Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[100px] -z-10"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-[100px] -z-10"></div>
      
      <div className="glass-card w-full max-w-md p-8 relative overflow-hidden">
        {/* Glow effect border */}
        <div className="absolute -top-1/2 -left-1/2 w-[200%] h-[200%] bg-gradient-to-br from-primary/10 via-transparent to-accent/10 opacity-30 animate-spin-slow pointer-events-none"></div>
        
        <div className="relative z-10">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-primary/10 rounded-2xl border border-primary/20">
              <Shield size={40} className="text-primary" />
            </div>
          </div>
          
          <h2 className="text-3xl font-bold text-center mb-2 text-white tracking-tight">Access System</h2>
          <p className="text-gray-400 text-center mb-8 text-sm">Quantum-Secured IDS Framework</p>
          
          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label htmlFor="agentId" className="block text-sm font-medium text-gray-400 mb-1">Agent ID</label>
              <input
                id="agentId"
                type="text"
                className="input-field"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            
            <div>
              <label htmlFor="passphrase" className="block text-sm font-medium text-gray-400 mb-1">Passphrase</label>
              <div className="relative">
                <input
                  id="passphrase"
                  type={showPassword ? "text" : "password"}
                  className="input-field pr-10"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
            
            <button 
              type="submit" 
              className="w-full btn-primary py-3 flex justify-center mt-2 font-semibold tracking-wide border border-transparent focus-visible:border-white focus-visible:ring-2 focus-visible:ring-primary focus:outline-none"
              disabled={loading}
            >
              {loading ? 'AUTHENTICATING...' : 'INITIALIZE UPLINK'}
            </button>
          </form>
          
          <p className="text-center text-gray-400 text-sm mt-6">
            New operative? <Link to="/signup" className="text-primary hover:text-accent font-medium ml-1 transition-colors">Request Access</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
