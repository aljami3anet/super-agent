import React from 'react'
import { MessageSquare, Search, Plus } from 'lucide-react'

export function Conversations() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Conversations
          </h1>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            View and manage your conversation history
          </p>
        </div>
        <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
          <Plus className="mr-2 h-4 w-4" />
          New Conversation
        </button>
      </div>

      {/* Search */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search conversations..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Conversations List */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="space-y-4">
            {/* Conversation 1 */}
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <MessageSquare className="h-5 w-5 text-blue-600 dark:text-blue-400 mr-3" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      React Component Development
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Created a new dashboard component with TypeScript and Tailwind CSS
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    2 hours ago
                  </p>
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    15 messages
                  </p>
                </div>
              </div>
            </div>

            {/* Conversation 2 */}
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <MessageSquare className="h-5 w-5 text-green-600 dark:text-green-400 mr-3" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      API Integration
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Integrated OpenRouter API with authentication and error handling
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    1 day ago
                  </p>
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    8 messages
                  </p>
                </div>
              </div>
            </div>

            {/* Conversation 3 */}
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <MessageSquare className="h-5 w-5 text-purple-600 dark:text-purple-400 mr-3" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      Database Schema Design
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Designed PostgreSQL schema for user management and conversations
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    3 days ago
                  </p>
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    12 messages
                  </p>
                </div>
              </div>
            </div>

            {/* Conversation 4 */}
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <MessageSquare className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mr-3" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      Testing Strategy
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Implemented comprehensive testing with pytest and coverage
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    1 week ago
                  </p>
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    6 messages
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}