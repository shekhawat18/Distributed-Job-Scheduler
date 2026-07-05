import { useState } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, FolderKanban, ListTree, Activity, 
  Server, Skull, LogOut, Bell, Menu 
} from 'lucide-react';
import { useAuth } from '../../features/auth/context/AuthContext';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Projects', path: '/projects', icon: FolderKanban },
  { name: 'Queues', path: '/queues', icon: ListTree },
  { name: 'Jobs', path: '/jobs', icon: Activity },
  { name: 'Workers', path: '/workers', icon: Server },
  { name: 'Dead Letters', path: '/dlq', icon: Skull },
];

export const DashboardLayout = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="flex h-screen overflow-hidden bg-background text-foreground">
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarOpen ? 240 : 72 }}
        className="z-20 flex h-full shrink-0 flex-col border-r border-border bg-card"
      >
        <div className="flex h-16 items-center justify-between border-b border-border px-4">
          <div className="flex items-center overflow-hidden space-x-3">
            <Activity className="shrink-0 text-primary" size={24} />
            <AnimatePresence>
              {isSidebarOpen && (
                <motion.span 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, width: 0 }}
                  className="whitespace-nowrap font-semibold tracking-tight"
                >
                  Scheduler
                </motion.span>
              )}
            </AnimatePresence>
          </div>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-6">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname.startsWith(item.path);
            
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 rounded-md px-3 py-2 transition-colors ${
                  isActive ? 'bg-white/10 text-primary' : 'text-muted hover:bg-white/5 hover:text-foreground'
                }`}
              >
                <Icon size={20} className="shrink-0" />
                {isSidebarOpen && <span className="text-sm font-medium">{item.name}</span>}
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-border p-4">
          <button onClick={logout} className="flex w-full items-center space-x-3 rounded-md px-3 py-2 text-muted transition-colors hover:bg-danger/10 hover:text-danger">
            <LogOut size={20} className="shrink-0" />
            {isSidebarOpen && <span className="text-sm font-medium">Logout</span>}
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex min-w-0 flex-1 flex-col">
        {/* Top Navbar */}
        <header className="z-10 flex h-16 items-center justify-between border-b border-border bg-background/50 px-6 backdrop-blur-md">
          <div className="flex items-center space-x-4">
            <button onClick={() => setSidebarOpen(!isSidebarOpen)} className="text-muted transition-colors hover:text-foreground">
              <Menu size={20} />
            </button>
            <div className="hidden text-sm capitalize text-muted sm:block">
              {location.pathname.split('/')[1] || 'Dashboard'}
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="relative text-muted hover:text-foreground">
              <Bell size={20} />
              <span className="absolute right-0 top-0 h-2 w-2 rounded-full bg-danger ring-2 ring-background"></span>
            </button>
            <div className="flex h-8 w-8 items-center justify-center rounded-full border border-border bg-zinc-800 text-sm font-medium">
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto p-6">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mx-auto max-w-7xl space-y-6"
          >
            <Outlet />
          </motion.div>
        </div>
      </main>
    </div>
  );
};