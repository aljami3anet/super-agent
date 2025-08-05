import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'

import { AppShell } from './components/layout/AppShell'
import { Dashboard } from './pages/Dashboard'
import { Logs } from './pages/Logs'
import { Config } from './pages/Config'
import { Agents } from './pages/Agents'
import { Conversations } from './pages/Conversations'
import { NotFound } from './pages/NotFound'

function App() {
  return (
    <>
      <Helmet>
        <title>AI Coder Agent</title>
        <meta name="description" content="Autonomous AI coding system with multi-agent orchestration" />
      </Helmet>
      
      <AppShell>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/config" element={<Config />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/conversations" element={<Conversations />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AppShell>
    </>
  )
}

export default App