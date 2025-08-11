import React, { useState, useEffect } from 'react';

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  logger: string;
  message: string;
  metadata?: Record<string, any>;
}

export function Logs() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([]);
  const [levelFilter, setLevelFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    // Simulate fetching logs
    const mockLogs: LogEntry[] = [
      {
        id: '1',
        timestamp: '2023-01-01T12:00:00Z',
        level: 'info',
        logger: 'agent.planner',
        message: 'Planning task: Create a new React component',
      },
      {
        id: '2',
        timestamp: '2023-01-01T12:01:00Z',
        level: 'info',
        logger: 'agent.coder',
        message: 'Generated code for React component',
      },
      {
        id: '3',
        timestamp: '2023-01-01T12:02:00Z',
        level: 'warn',
        logger: 'agent.critic',
        message: 'Potential performance issue detected in component',
        metadata: {
          component: 'UserProfile',
          issue: 'Unnecessary re-renders',
        },
      },
      {
        id: '4',
        timestamp: '2023-01-01T12:03:00Z',
        level: 'error',
        logger: 'agent.tester',
        message: 'Test failed: Component should render user data',
        metadata: {
          test: 'UserProfile.render',
          error: 'Expected user data to be defined',
        },
      },
      {
        id: '5',
        timestamp: '2023-01-01T12:04:00Z',
        level: 'info',
        logger: 'agent.summarizer',
        message: 'Generated summary for conversation',
      },
    ];

    setLogs(mockLogs);
    setFilteredLogs(mockLogs);
  }, []);

  useEffect(() => {
    // Apply filters
    let result = logs;
    
    if (levelFilter !== 'all') {
      result = result.filter(log => log.level === levelFilter);
    }
    
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(log => 
        log.message.toLowerCase().includes(term) || 
        log.logger.toLowerCase().includes(term)
      );
    }
    
    setFilteredLogs(result);
  }, [logs, levelFilter, searchTerm]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (autoRefresh) {
      // Simulate new logs being added
      interval = setInterval(() => {
        const newLog: LogEntry = {
          id: String(logs.length + 1),
          timestamp: new Date().toISOString(),
          level: 'info',
          logger: 'system',
          message: 'Auto-refresh: No new logs',
        };
        
        setLogs(prev => [newLog, ...prev]);
      }, 5000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh, logs.length]);

  const getLevelColor = (level: LogEntry['level']) => {
    switch (level) {
      case 'info':
        return 'bg-blue-100 text-blue-800';
      case 'warn':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      case 'debug':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Logs</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            View and filter application logs
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-500 dark:text-gray-400">Auto-refresh</span>
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
              autoRefresh ? 'bg-indigo-600' : 'bg-gray-200 dark:bg-gray-700'
            }`}
            role="switch"
            aria-checked={autoRefresh}
          >
            <span
              aria-hidden="true"
              className={`pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200 ${
                autoRefresh ? 'translate-x-5' : 'translate-x-0'
              }`}
            />
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
            <div className="flex space-x-2">
              <select
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md dark:bg-gray-700 dark:text-white"
                value={levelFilter}
                onChange={(e) => setLevelFilter(e.target.value)}
              >
                <option value="all">All Levels</option>
                <option value="debug">Debug</option>
                <option value="info">Info</option>
                <option value="warn">Warning</option>
                <option value="error">Error</option>
              </select>
            </div>
            
            <div className="flex-1 max-w-lg">
              <div className="relative rounded-md shadow-sm">
                <input
                  type="text"
                  className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pr-10 sm:text-sm border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md"
                  placeholder="Search logs..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="overflow-hidden">
          <ul className="divide-y divide-gray-200 dark:divide-gray-700 max-h-[calc(100vh-250px)] overflow-y-auto">
            {filteredLogs.length === 0 ? (
              <li className="py-12 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No logs found</h3>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">Try adjusting your filters.</p>
              </li>
            ) : (
              filteredLogs.map((log) => (
                <li key={log.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-750">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getLevelColor(log.level)}`}>
                        {log.level.toUpperCase()}
                      </span>
                      <p className="ml-3 text-sm font-mono text-gray-500 dark:text-gray-400">{log.logger}</p>
                    </div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">{formatTimestamp(log.timestamp)}</p>
                  </div>
                  <div className="mt-2 text-sm text-gray-900 dark:text-white">
                    {log.message}
                  </div>
                  {log.metadata && (
                    <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                      <pre className="bg-gray-100 dark:bg-gray-700 p-2 rounded overflow-x-auto">
                        {JSON.stringify(log.metadata, null, 2)}
                      </pre>
                    </div>
                  )}
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}