import { useState, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Fingerprint, Eye, EyeOff } from 'lucide-react';
import { useToast } from '../components/Toast';

export default function Signup({ setAuth }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { addToast } = useToast();

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Log them in immediately
        const loginRes = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        const loginData = await loginRes.json();
        
        if (loginData.success) {
          localStorage.setItem('token', loginData.token);
          localStorage.setItem('username', loginData.username);
          setAuth(true);
          addToast('Identity provisioned successfully.', 'success');
          navigate('/dashboard');
        } else {
          navigate('/login');
        }
      } else {
        addToast(data.message || 'Registration failed', 'error');
      }
    } catch (err) {
      addToast('Unable to connect to server', 'error');
    } finally {
      setLoading(false);
    }
  };

  const getStrength = (pass) => {
    let score = 0;
    if (pass.length > 5) score += 1;
    if (pass.length > 8) score += 1;
    if (/[A-Z]/.test(pass)) score += 1;
    if (/[0-9]/.test(pass)) score += 1;
    if (/[^a-zA-Z0-9]/.test(pass)) score += 1;
    return score;
  };
  
  const strength = useMemo(() => getStrength(password), [password]);

  return (
    <div className="min-h-screen flex items-center justify-center relative px-4">
      {/* Abstract Background Orbs */}
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[400px] bg-secondary/20 rounded-full blur-[120px] -z-10"></div>
      <div className="absolute bottom-1/4 left-1/4 w-[300px] h-[300px] bg-primary/20 rounded-full blur-[100px] -z-10"></div>
      
      <div className="glass-card w-full max-w-md p-8 relative overflow-hidden">
        <div className="relative z-10">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-secondary/10 rounded-2xl border border-secondary/20">
              <Fingerprint size={40} className="text-secondary" />
            </div>
          </div>
          
          <h2 className="text-3xl font-bold text-center mb-2 text-white tracking-tight">Register Origin</h2>
          <p className="text-gray-400 text-center mb-8 text-sm">Secure Identity Provisioning</p>
          
          <form onSubmit={handleSignup} className="space-y-5">
            <div>
              <label htmlFor="regUsername" className="block text-sm font-medium text-gray-400 mb-1">Desired Agent ID</label>
              <input
                id="regUsername"
                type="text"
                className="input-field"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            
            <div>
              <label htmlFor="regPassphrase" className="block text-sm font-medium text-gray-400 mb-1">Passphrase</label>
              <div className="relative">
                <input
                  id="regPassphrase"
                  type={showPassword ? "text" : "password"}
                  className="input-field pr-10"
                  placeholder="Create password"
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
              {/* Strength Indicator */}
              {password.length > 0 && (
                <div className="mt-2 flex space-x-1">
                  {[1, 2, 3, 4, 5].map((level) => (
                    <div 
                      key={level} 
                      className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                        strength >= level 
                          ? (strength > 3 ? 'bg-secondary' : strength > 2 ? 'bg-yellow-400' : 'bg-red-400') 
                          : 'bg-white/10'
                      }`}
                    ></div>
                  ))}
                </div>
              )}
            </div>
            
            <button 
              type="submit" 
              className="w-full relative px-4 py-3 bg-secondary/90 hover:bg-secondary text-white font-semibold rounded-lg transition-all duration-300 shadow-[0_0_15px_rgba(139,92,246,0.3)] hover:shadow-[0_0_25px_rgba(139,92,246,0.5)] mt-4 tracking-wide flex justify-center focus:outline-none focus:ring-2 focus:ring-secondary focus-visible:border-white"
              disabled={loading}
            >
              {loading ? 'PROVISIONING...' : 'ENROLL IDENTITY'}
            </button>
          </form>
          
          <p className="text-center text-gray-400 text-sm mt-6">
            Already registered? <Link to="/login" className="text-secondary hover:text-white font-medium ml-1 transition-colors">Return to Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
