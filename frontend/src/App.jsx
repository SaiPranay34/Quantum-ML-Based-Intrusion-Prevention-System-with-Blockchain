import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Menu, Wifi, Activity } from 'lucide-react';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Visualizations from './pages/Visualizations';
import Sidebar from './components/Sidebar';
import { ToastProvider } from './components/Toast';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    // Check if token exists in localStorage
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-primary bg-[#0a0a0f]">
        <div className="relative w-24 h-24 flex items-center justify-center">
          <div className="absolute inset-0 rounded-full border-t-2 border-primary animate-spin"></div>
          <div className="absolute inset-2 rounded-full border-t-2 border-secondary animate-spin-slow" style={{ animationDirection: 'reverse' }}></div>
          <Activity className="text-primary animate-pulse" size={24} />
        </div>
      </div>
    );
  }

  return (
    <ToastProvider>
      <Router>
        <div className="flex min-h-screen relative">
          {isAuthenticated && (
            <>
              {/* Mobile Header */}
              <div className="md:hidden fixed top-0 w-full z-40 bg-[#0a0a0f]/90 backdrop-blur-md border-b border-white/10 p-4 flex justify-between items-center">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                  <span className="text-sm font-medium text-white tracking-widest uppercase">Quantum IDS</span>
                </div>
                <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="text-white hover:text-primary transition-colors">
                  <Menu size={24} />
                </button>
              </div>
              
              <Sidebar 
                onLogout={() => setIsAuthenticated(false)} 
                isOpen={isSidebarOpen}
                setIsOpen={setIsSidebarOpen}
              />
            </>
          )}
          
          <main className={`flex-1 overflow-x-hidden overflow-y-auto bg-transparent transition-all duration-300 ${isAuthenticated ? 'md:ml-64 pt-16 md:pt-0' : ''}`}>
            {isAuthenticated && (
              <div className="hidden md:flex bg-black/40 border-b border-white/5 px-6 py-2 items-center justify-between sticky top-0 z-30 backdrop-blur-md">
                <div className="flex items-center space-x-6 text-xs font-mono">
                  <div className="flex items-center space-x-2 text-green-400 bg-green-500/10 border border-green-500/20 px-2 py-1 rounded">
                    <Wifi size={14} />
                    <span>Network: Secured</span>
                  </div>
                  <div className="text-gray-400">
                    Block Height: <span className="text-white font-semibold flex-inline items-center"><span className="text-primary mr-1">#</span>104,429</span>
                  </div>
                  <div className="text-gray-400">
                    Active Validating Peers: <span className="text-white font-semibold">12</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2 text-xs font-mono text-primary animate-pulse">
                  <span>Consensus Reached - 100% Synced</span>
                </div>
              </div>
            )}

            <Routes>
              <Route 
                path="/login" 
                element={!isAuthenticated ? <Login setAuth={setIsAuthenticated} /> : <Navigate to="/dashboard" />} 
              />
              <Route 
                path="/signup" 
                element={!isAuthenticated ? <Signup setAuth={setIsAuthenticated} /> : <Navigate to="/dashboard" />} 
              />
              <Route 
                path="/dashboard" 
                element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/visualizations" 
                element={isAuthenticated ? <Visualizations /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/" 
                element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} 
              />
            </Routes>
          </main>
        </div>
      </Router>
    </ToastProvider>
  );
}

export default App;
