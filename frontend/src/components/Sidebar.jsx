import { Link, useLocation } from 'react-router-dom';
import { Activity, LayoutDashboard, LogOut, BarChart2, X } from 'lucide-react';

export default function Sidebar({ onLogout, isOpen, setIsOpen }) {
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    onLogout();
  };

  const navItems = [
    { path: '/dashboard', label: 'Monitor', icon: <Activity size={20} /> },
    { path: '/visualizations', label: 'Analytics', icon: <BarChart2 size={20} /> },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
      
      <div className={`w-64 fixed top-0 left-0 h-full glass-panel border-r border-white/5 flex flex-col pt-8 pb-4 px-4 z-50 transition-transform duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <div className="mb-10 px-2 flex items-center justify-between md:justify-center">
          <div className="flex items-center space-x-2">
            <LayoutDashboard className="text-primary" size={28} />
            <h1 className="text-xl font-bold neon-text tracking-wide uppercase">Quantum IDS</h1>
          </div>
          <button 
            className="md:hidden text-gray-400 hover:text-white"
            onClick={() => setIsOpen(false)}
          >
            <X size={24} />
          </button>
        </div>
        
        <div className="flex-1 space-y-2 relative">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen && setIsOpen(false)}
                className={`group relative flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                  isActive 
                    ? 'bg-primary/20 text-primary border border-primary/30 shadow-[0_0_15px_rgba(59,130,246,0.1)]' 
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                {isActive && (
                  <div className="absolute -left-4 w-1 rounded-r-full bg-primary h-8 shadow-[0_0_10px_rgba(59,130,246,0.5)]"></div>
                )}
                <div className={isActive ? 'text-primary' : 'text-gray-500 group-hover:text-gray-300'}>
                  {item.icon}
                </div>
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>

        <div className="border-t border-white/10 pt-4 mt-auto">
          <div className="mb-4 px-4 text-sm text-gray-400">
            Operative: <span className="text-white font-medium">{localStorage.getItem('username')}</span>
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-4 py-3 text-red-500 hover:text-red-400 hover:bg-red-500/10 border border-transparent hover:border-red-500/20 rounded-xl transition-all duration-300"
          >
            <LogOut size={20} />
            <span className="font-medium">Disconnect</span>
          </button>
        </div>
      </div>
    </>
  );
}
