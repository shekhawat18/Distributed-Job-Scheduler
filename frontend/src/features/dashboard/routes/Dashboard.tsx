import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts';
import {
  CheckCircle2,
  AlertCircle,
  Server,
  Activity,
  Loader2,
} from "lucide-react";

import type { LucideIcon } from "lucide-react";
import { AxiosError } from 'axios';
import { dashboardService } from '../../../services/dashboard.service';
import type { DashboardStats, StatusDistribution } from '../../../types';

interface StatCardProps {
  title: string;
  value: number;
  icon: LucideIcon;
}

const StatCard = ({ title, value, icon: Icon }: StatCardProps) => (
  <motion.div 
    variants={{ hidden: { opacity: 0, y: 10 }, show: { opacity: 1, y: 0 } }}
    className="rounded-xl border border-border bg-card p-5 shadow-sm transition-colors hover:border-zinc-700"
  >
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm font-medium text-muted">{title}</p>
        <h3 className="mt-2 text-3xl font-bold tracking-tight">{value}</h3>
      </div>
      <div className="rounded-lg bg-zinc-900 p-3">
        <Icon size={20} className="text-primary" />
      </div>
    </div>
  </motion.div>
);

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeframe, setTimeframe] = useState<'24h' | '7d' | '30d'>('24h');

  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await dashboardService.getStats(timeframe);
        setStats(data);
      } catch (err) {
        const message = err instanceof AxiosError 
          ? err.response?.data?.detail || 'Failed to load dashboard statistics' 
          : 'An unexpected error occurred';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, [timeframe]);

  if (error) {
    return (
      <div className="flex h-64 items-center justify-center rounded-xl border border-danger/20 bg-danger/5 p-6">
        <div className="text-center">
          <AlertCircle className="mx-auto mb-2 h-8 w-8 text-danger" />
          <p className="text-sm font-medium text-danger">{error}</p>
        </div>
      </div>
    );
  }

  if (isLoading || !stats) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    show: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Overview</h1>
        <select 
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value as '24h' | '7d' | '30d')}
          className="rounded-md border border-border bg-card px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="24h">Last 24 Hours</option>
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
        </select>
      </div>

      <motion.div 
        variants={containerVariants} 
        initial="hidden" 
        animate="show"
        className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4"
      >
        <StatCard title="Active Workers" value={stats.active_workers} icon={Server} />
        <StatCard title="Running Jobs" value={stats.jobs_running} icon={Activity} />
        <StatCard title="Completed Jobs" value={stats.jobs_completed} icon={CheckCircle2} />
        <StatCard title="Failed Jobs" value={stats.jobs_failed} icon={AlertCircle} />
      </motion.div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Execution Trend Line Chart */}
        <div className="col-span-1 rounded-xl border border-border bg-card p-6 lg:col-span-2">
          <h3 className="mb-6 text-sm font-semibold text-muted">Execution Trend</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats.execution_trend}>
                <defs>
                  <linearGradient id="colorSuccess" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="time" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#09090b', border: '1px solid #27272a', borderRadius: '8px' }}
                  itemStyle={{ color: '#ededed' }}
                />
                <Area type="monotone" dataKey="success" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorSuccess)" />
                <Area type="monotone" dataKey="failed" stroke="#ef4444" strokeWidth={2} fill="none" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Job Status Donut Chart */}
        <div className="flex flex-col rounded-xl border border-border bg-card p-6">
          <h3 className="mb-2 text-sm font-semibold text-muted">Job Status Distribution</h3>
          <div className="relative flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.status_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {stats.status_distribution.map((entry: StatusDistribution, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#09090b', border: '1px solid #27272a', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold">
                {stats.jobs_completed + stats.jobs_failed + stats.jobs_running + stats.jobs_queued}
              </span>
              <span className="text-xs text-muted">Total Jobs</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}