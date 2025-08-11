import React, { useState, useEffect } from 'react';

interface Config {
  app_name: string;
  app_version: string;
  debug: boolean;
  cors_origins: string[];
  otel_enabled: boolean;
  otel_service_name: string;
  otel_environment: string;
  primary_model: string;
  fallback_model: string;
  max_tokens: number;
  temperature: number;
  rate_limit_requests: number;
  rate_limit_window: number;
}

interface Model {
  id: string;
  name: string;
  provider: string;
  description: string;
}

export function Config() {
  const [config, setConfig] = useState<Config | null>(null);
  const [models, setModels] = useState<Model[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editedConfig, setEditedConfig] = useState<Config | null>(null);

  useEffect(() => {
    // Simulate fetching config
    const mockConfig: Config = {
      app_name: 'AI Coder Agent',
      app_version: '0.1.0',
      debug: true,
      cors_origins: ['http://localhost:3000', 'http://localhost:5173'],
      otel_enabled: true,
      otel_service_name: 'ai-coder-agent',
      otel_environment: 'development',
      primary_model: 'anthropic/claude-2',
      fallback_model: 'openai/gpt-4',
      max_tokens: 4000,
      temperature: 0.7,
      rate_limit_requests: 100,
      rate_limit_window: 60,
    };

    const mockModels: Model[] = [
      {
        id: 'anthropic/claude-2',
        name: 'Claude 2',
        provider: 'Anthropic',
        description: 'Powerful AI assistant for complex reasoning and creativity',
      },
      {
        id: 'openai/gpt-4',
        name: 'GPT-4',
        provider: 'OpenAI',
        description: 'Advanced language model with broad knowledge and reasoning capabilities',
      },
      {
        id: 'openai/gpt-3.5-turbo',
        name: 'GPT-3.5 Turbo',
        provider: 'OpenAI',
        description: 'Fast and capable language model for most tasks',
      },
    ];

    setConfig(mockConfig);
    setEditedConfig(mockConfig);
    setModels(mockModels);
  }, []);

  const handleSaveConfig = () => {
    if (!editedConfig) return;
    
    // In a real implementation, this would call the API
    setConfig(editedConfig);
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditedConfig(config);
    setIsEditing(false);
  };

  const handleConfigChange = (key: keyof Config, value: any) => {
    if (!editedConfig) return;
    
    setEditedConfig({
      ...editedConfig,
      [key]: value,
    });
  };

  if (!config || !editedConfig) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Configuration</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Manage application settings and configuration
          </p>
        </div>
        
        <div>
          {isEditing ? (
            <div className="flex space-x-2">
              <button
                onClick={handleCancelEdit}
                className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md shadow-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveConfig}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Save
              </button>
            </div>
          ) : (
            <button
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Edit
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Application settings */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">Application Settings</h3>
          </div>
          <div className="px-4 py-5 sm:p-6 space-y-4">
            <div>
              <label htmlFor="app-name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Application Name
              </label>
              {isEditing ? (
                <input
                  type="text"
                  id="app-name"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.app_name}
                  onChange={(e) => handleConfigChange('app_name', e.target.value)}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.app_name}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="app-version" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Application Version
              </label>
              {isEditing ? (
                <input
                  type="text"
                  id="app-version"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.app_version}
                  onChange={(e) => handleConfigChange('app_version', e.target.value)}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.app_version}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="debug" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Debug Mode
              </label>
              {isEditing ? (
                <div className="mt-1">
                  <select
                    id="debug"
                    className="block w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:text-white"
                    value={editedConfig.debug ? 'true' : 'false'}
                    onChange={(e) => handleConfigChange('debug', e.target.value === 'true')}
                  >
                    <option value="true">Enabled</option>
                    <option value="false">Disabled</option>
                  </select>
                </div>
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">
                  {config.debug ? 'Enabled' : 'Disabled'}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* AI model settings */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">AI Model Settings</h3>
          </div>
          <div className="px-4 py-5 sm:p-6 space-y-4">
            <div>
              <label htmlFor="primary-model" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Primary Model
              </label>
              {isEditing ? (
                <div className="mt-1">
                  <select
                    id="primary-model"
                    className="block w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:text-white"
                    value={editedConfig.primary_model}
                    onChange={(e) => handleConfigChange('primary_model', e.target.value)}
                  >
                    {models.map((model) => (
                      <option key={model.id} value={model.id}>
                        {model.name} ({model.provider})
                      </option>
                    ))}
                  </select>
                </div>
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">
                  {models.find(m => m.id === config.primary_model)?.name || config.primary_model}
                </p>
              )}
            </div>
            
            <div>
              <label htmlFor="fallback-model" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Fallback Model
              </label>
              {isEditing ? (
                <div className="mt-1">
                  <select
                    id="fallback-model"
                    className="block w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:text-white"
                    value={editedConfig.fallback_model}
                    onChange={(e) => handleConfigChange('fallback_model', e.target.value)}
                  >
                    {models.map((model) => (
                      <option key={model.id} value={model.id}>
                        {model.name} ({model.provider})
                      </option>
                    ))}
                  </select>
                </div>
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">
                  {models.find(m => m.id === config.fallback_model)?.name || config.fallback_model}
                </p>
              )}
            </div>
            
            <div>
              <label htmlFor="max-tokens" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Max Tokens
              </label>
              {isEditing ? (
                <input
                  type="number"
                  id="max-tokens"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.max_tokens}
                  onChange={(e) => handleConfigChange('max_tokens', parseInt(e.target.value))}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.max_tokens}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="temperature" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Temperature
              </label>
              {isEditing ? (
                <input
                  type="number"
                  id="temperature"
                  step="0.1"
                  min="0"
                  max="1"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.temperature}
                  onChange={(e) => handleConfigChange('temperature', parseFloat(e.target.value))}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.temperature}</p>
              )}
            </div>
          </div>
        </div>

        {/* Rate limiting settings */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">Rate Limiting</h3>
          </div>
          <div className="px-4 py-5 sm:p-6 space-y-4">
            <div>
              <label htmlFor="rate-limit-requests" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Requests per window
              </label>
              {isEditing ? (
                <input
                  type="number"
                  id="rate-limit-requests"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.rate_limit_requests}
                  onChange={(e) => handleConfigChange('rate_limit_requests', parseInt(e.target.value))}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.rate_limit_requests}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="rate-limit-window" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Window duration (seconds)
              </label>
              {isEditing ? (
                <input
                  type="number"
                  id="rate-limit-window"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.rate_limit_window}
                  onChange={(e) => handleConfigChange('rate_limit_window', parseInt(e.target.value))}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.rate_limit_window}</p>
              )}
            </div>
          </div>
        </div>

        {/* Observability settings */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">Observability</h3>
          </div>
          <div className="px-4 py-5 sm:p-6 space-y-4">
            <div>
              <label htmlFor="otel-enabled" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                OpenTelemetry
              </label>
              {isEditing ? (
                <div className="mt-1">
                  <select
                    id="otel-enabled"
                    className="block w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:text-white"
                    value={editedConfig.otel_enabled ? 'true' : 'false'}
                    onChange={(e) => handleConfigChange('otel_enabled', e.target.value === 'true')}
                  >
                    <option value="true">Enabled</option>
                    <option value="false">Disabled</option>
                  </select>
                </div>
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">
                  {config.otel_enabled ? 'Enabled' : 'Disabled'}
                </p>
              )}
            </div>
            
            <div>
              <label htmlFor="otel-service-name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Service Name
              </label>
              {isEditing ? (
                <input
                  type="text"
                  id="otel-service-name"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.otel_service_name}
                  onChange={(e) => handleConfigChange('otel_service_name', e.target.value)}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.otel_service_name}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="otel-environment" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Environment
              </label>
              {isEditing ? (
                <input
                  type="text"
                  id="otel-environment"
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                  value={editedConfig.otel_environment}
                  onChange={(e) => handleConfigChange('otel_environment', e.target.value)}
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900 dark:text-white">{config.otel_environment}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}