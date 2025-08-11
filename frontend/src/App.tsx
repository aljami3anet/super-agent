import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppShell } from './components/layout/AppShell';
import { Dashboard } from './pages/Dashboard';
import { Agents } from './pages/Agents';
import { Conversations } from './pages/Conversations';
import { Config } from './pages/Config';
import { Logs } from './pages/Logs';
import { NotFound } from './pages/NotFound';
import { ThemeProvider } from './components/theme/ThemeProvider';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <AppShell>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/conversations" element={<Conversations />} />
            <Route path="/config" element={<Config />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AppShell>
      </Router>
    </ThemeProvider>
  );
}

export default App;