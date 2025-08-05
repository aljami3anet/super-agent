import React from 'react'
import { Bot, Play, Pause, Settings } from 'lucide-react'

export function Agents() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          AI Agents
        </h1>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
          Manage and monitor your AI agents
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {/* Planner Agent */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Bot className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Planner
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Task planning and strategy
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button className="p-2 text-green-600 hover:text-green-700">
                  <Play className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-500">
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">Status</span>
                <span className="text-green-600 dark:text-green-400">Active</span>
              </div>
              <div className="flex items-center justify-between text-sm mt-1">
                <span className="text-gray-500 dark:text-gray-400">Tasks</span>
                <span className="text-gray-900 dark:text-gray-100">15</span>
              </div>
            </div>
          </div>
        </div>

        {/* Coder Agent */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Bot className="h-8 w-8 text-green-600 dark:text-green-400" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Coder
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Code generation and implementation
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button className="p-2 text-green-600 hover:text-green-700">
                  <Play className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-500">
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">Status</span>
                <span className="text-green-600 dark:text-green-400">Active</span>
              </div>
              <div className="flex items-center justify-between text-sm mt-1">
                <span className="text-gray-500 dark:text-gray-400">Tasks</span>
                <span className="text-gray-900 dark:text-gray-100">23</span>
              </div>
            </div>
          </div>
        </div>

        {/* Critic Agent */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Bot className="h-8 w-8 text-yellow-600 dark:text-yellow-400" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Critic
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Code review and feedback
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button className="p-2 text-green-600 hover:text-green-700">
                  <Play className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-500">
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">Status</span>
                <span className="text-green-600 dark:text-green-400">Active</span>
              </div>
              <div className="flex items-center justify-between text-sm mt-1">
                <span className="text-gray-500 dark:text-gray-400">Reviews</span>
                <span className="text-gray-900 dark:text-gray-100">8</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tester Agent */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Bot className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Tester
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Automated testing and validation
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button className="p-2 text-green-600 hover:text-green-700">
                  <Play className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-500">
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">Status</span>
                <span className="text-green-600 dark:text-green-400">Active</span>
              </div>
              <div className="flex items-center justify-between text-sm mt-1">
                <span className="text-gray-500 dark:text-gray-400">Tests</span>
                <span className="text-gray-900 dark:text-gray-100">12</span>
              </div>
            </div>
          </div>
        </div>

        {/* Summarizer Agent */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Bot className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Summarizer
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Conversation and code summarization
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button className="p-2 text-green-600 hover:text-green-700">
                  <Play className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-500">
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">Status</span>
                <span className="text-green-600 dark:text-green-400">Active</span>
              </div>
              <div className="flex items-center justify-between text-sm mt-1">
                <span className="text-gray-500 dark:text-gray-400">Summaries</span>
                <span className="text-gray-900 dark:text-gray-100">5</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}