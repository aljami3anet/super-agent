import React, { useState, useEffect } from 'react';

interface Conversation {
  id: string;
  user_id: string;
  title: string;
  messages: Array<{
    role: string;
    content: string;
    timestamp: string;
  }>;
  created_at: string;
  updated_at: string;
  summary?: string;
}

export function Conversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const [newConversationTitle, setNewConversationTitle] = useState('');

  useEffect(() => {
    // Simulate fetching conversations
    const mockConversations: Conversation[] = [
      {
        id: '1',
        user_id: 'user1',
        title: 'Project Setup',
        messages: [
          {
            role: 'user',
            content: 'Help me set up a new Python project',
            timestamp: '2023-01-01T10:00:00Z',
          },
          {
            role: 'assistant',
            content: 'I\'ll help you set up a new Python project. First, let me create a plan...',
            timestamp: '2023-01-01T10:01:00Z',
          },
        ],
        created_at: '2023-01-01T10:00:00Z',
        updated_at: '2023-01-01T10:05:00Z',
      },
      {
        id: '2',
        user_id: 'user1',
        title: 'Code Review',
        messages: [
          {
            role: 'user',
            content: 'Can you review this code for me?',
            timestamp: '2023-01-02T14:30:00Z',
          },
          {
            role: 'assistant',
            content: 'I\'d be happy to review your code. Please share it with me.',
            timestamp: '2023-01-02T14:31:00Z',
          },
        ],
        created_at: '2023-01-02T14:30:00Z',
        updated_at: '2023-01-02T14:35:00Z',
      },
    ];

    setConversations(mockConversations);
    setSelectedConversation(mockConversations[0]);
  }, []);

  const handleSendMessage = () => {
    if (!selectedConversation || !newMessage.trim()) return;
    
    // In a real implementation, this would call the API
    const updatedConversation = {
      ...selectedConversation,
      messages: [
        ...selectedConversation.messages,
        {
          role: 'user',
          content: newMessage,
          timestamp: new Date().toISOString(),
        },
      ],
      updated_at: new Date().toISOString(),
    };
    
    setSelectedConversation(updatedConversation);
    setConversations(conversations.map(conv => 
      conv.id === selectedConversation.id ? updatedConversation : conv
    ));
    setNewMessage('');
  };

  const handleCreateConversation = () => {
    if (!newConversationTitle.trim()) return;
    
    // In a real implementation, this would call the API
    const newConversation: Conversation = {
      id: String(conversations.length + 1),
      user_id: 'user1',
      title: newConversationTitle,
      messages: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    
    setConversations([newConversation, ...conversations]);
    setSelectedConversation(newConversation);
    setNewConversationTitle('');
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Conversations</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Manage your conversations with AI agents
          </p>
        </div>
        
        <div className="flex space-x-2">
          <input
            type="text"
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md"
            placeholder="New conversation title..."
            value={newConversationTitle}
            onChange={(e) => setNewConversationTitle(e.target.value)}
          />
          <button
            onClick={handleCreateConversation}
            disabled={!newConversationTitle.trim()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
          >
            New
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Conversation list */}
        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
            <ul className="divide-y divide-gray-200 dark:divide-gray-700 max-h-[calc(100vh-200px)] overflow-y-auto">
              {conversations.map((conversation) => (
                <li
                  key={conversation.id}
                  className={`px-4 py-4 sm:px-6 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-750 ${
                    selectedConversation?.id === conversation.id ? 'bg-gray-50 dark:bg-gray-750' : ''
                  }`}
                  onClick={() => setSelectedConversation(conversation)}
                >
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-indigo-600 dark:text-indigo-400 truncate">{conversation.title}</p>
                    <div className="ml-2 flex-shrink-0 flex">
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {new Date(conversation.updated_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 flex justify-between">
                    <div className="sm:flex">
                      <p className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                        {conversation.messages.length} messages
                      </p>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Conversation details */}
        <div className="lg:col-span-2">
          {selectedConversation ? (
            <div className="bg-white dark:bg-gray-800 shadow rounded-lg flex flex-col h-[calc(100vh-200px)]">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                  {selectedConversation.title}
                </h3>
              </div>
              
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {selectedConversation.messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                      }`}
                    >
                      <p>{message.content}</p>
                      <p className="text-xs mt-1 opacity-70">
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                
                {selectedConversation.messages.length === 0 && (
                  <div className="text-center py-8">
                    <svg className="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No messages</h3>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">Start a conversation by sending a message.</p>
                  </div>
                )}
              </div>
              
              <div className="border-t border-gray-200 dark:border-gray-700 p-4">
                <div className="flex rounded-md shadow-sm">
                  <input
                    type="text"
                    className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-l-md sm:text-sm border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    placeholder="Type a message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        handleSendMessage();
                      }
                    }}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!newMessage.trim()}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-r-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
              <div className="px-4 py-12 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No conversation selected</h3>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">Select a conversation from the list or create a new one.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}