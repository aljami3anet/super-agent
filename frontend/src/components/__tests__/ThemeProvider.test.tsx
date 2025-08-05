import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { ThemeProvider, useTheme } from '../theme/ThemeProvider'

// Test component that uses the theme
const TestComponent = () => {
  const { theme, setTheme, resolvedTheme } = useTheme()
  return (
    <div>
      <div data-testid="current-theme">{theme}</div>
      <div data-testid="resolved-theme">{resolvedTheme}</div>
      <button onClick={() => setTheme('light')}>Light</button>
      <button onClick={() => setTheme('dark')}>Dark</button>
      <button onClick={() => setTheme('system')}>System</button>
    </div>
  )
}

describe('ThemeProvider', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    // Reset document class
    document.documentElement.classList.remove('light', 'dark')
  })

  it('renders children', () => {
    render(
      <ThemeProvider>
        <div data-testid="child">Test Child</div>
      </ThemeProvider>
    )

    expect(screen.getByTestId('child')).toBeInTheDocument()
  })

  it('defaults to system theme when no preference is stored', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    )

    expect(screen.getByTestId('current-theme')).toHaveTextContent('system')
  })

  it('loads theme from localStorage', () => {
    localStorage.setItem('theme', 'dark')

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    )

    expect(screen.getByTestId('current-theme')).toHaveTextContent('dark')
  })

  it('allows changing theme', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    )

    // Change to light theme
    fireEvent.click(screen.getByText('Light'))
    expect(screen.getByTestId('current-theme')).toHaveTextContent('light')

    // Change to dark theme
    fireEvent.click(screen.getByText('Dark'))
    expect(screen.getByTestId('current-theme')).toHaveTextContent('dark')

    // Change to system theme
    fireEvent.click(screen.getByText('System'))
    expect(screen.getByTestId('current-theme')).toHaveTextContent('system')
  })

  it('saves theme preference to localStorage', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    )

    fireEvent.click(screen.getByText('Dark'))
    
    expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'dark')
  })

  it('applies correct CSS classes to document', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    )

    // Change to light theme
    fireEvent.click(screen.getByText('Light'))
    expect(document.documentElement).toHaveClass('light')
    expect(document.documentElement).not.toHaveClass('dark')

    // Change to dark theme
    fireEvent.click(screen.getByText('Dark'))
    expect(document.documentElement).toHaveClass('dark')
    expect(document.documentElement).not.toHaveClass('light')
  })

  it('handles system theme preference', () => {
    // Mock matchMedia to return dark preference
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation(query => ({
        matches: query === '(prefers-color-scheme: dark)',
        media: query,
        onchange: null,
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    })

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    )

    // Set to system theme
    fireEvent.click(screen.getByText('System'))
    
    // Should resolve to dark theme based on system preference
    expect(screen.getByTestId('resolved-theme')).toHaveTextContent('dark')
  })

  it('throws error when useTheme is used outside provider', () => {
    // Suppress console.error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})

    expect(() => {
      render(<TestComponent />)
    }).toThrow('useTheme must be used within a ThemeProvider')

    consoleSpy.mockRestore()
  })
})