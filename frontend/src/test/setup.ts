import '@testing-library/jest-dom'

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
})

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
}
global.localStorage = localStorageMock

// Mock sessionStorage
const sessionStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
}
global.sessionStorage = sessionStorageMock

// Mock WebSocket
global.WebSocket = jest.fn().mockImplementation(() => ({
  readyState: 1,
  send: jest.fn(),
  close: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
}))

// Mock fetch
global.fetch = jest.fn()

// Mock console methods to reduce noise in tests
const originalConsoleError = console.error
const originalConsoleWarn = console.warn

beforeAll(() => {
  console.error = jest.fn()
  console.warn = jest.fn()
})

afterAll(() => {
  console.error = originalConsoleError
  console.warn = originalConsoleWarn
})

// Mock IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock requestAnimationFrame
global.requestAnimationFrame = jest.fn(cb => setTimeout(cb, 0))
global.cancelAnimationFrame = jest.fn()

// Mock getComputedStyle
Object.defineProperty(window, 'getComputedStyle', {
  value: () => ({
    getPropertyValue: () => '',
  }),
})

// Mock Element.prototype.scrollIntoView
Element.prototype.scrollIntoView = jest.fn()

// Mock HTMLElement.prototype.focus
HTMLElement.prototype.focus = jest.fn()

// Mock HTMLElement.prototype.blur
HTMLElement.prototype.blur = jest.fn()

// Mock window.scrollTo
window.scrollTo = jest.fn()

// Mock window.scrollBy
window.scrollBy = jest.fn()

// Mock window.scroll
window.scroll = jest.fn()

// Mock window.scrollX
Object.defineProperty(window, 'scrollX', {
  value: 0,
  writable: true,
})

// Mock window.scrollY
Object.defineProperty(window, 'scrollY', {
  value: 0,
  writable: true,
})

// Mock window.innerWidth
Object.defineProperty(window, 'innerWidth', {
  value: 1024,
  writable: true,
})

// Mock window.innerHeight
Object.defineProperty(window, 'innerHeight', {
  value: 768,
  writable: true,
})

// Mock window.devicePixelRatio
Object.defineProperty(window, 'devicePixelRatio', {
  value: 1,
  writable: true,
})

// Mock window.location
Object.defineProperty(window, 'location', {
  value: {
    href: 'http://localhost:3000',
    origin: 'http://localhost:3000',
    protocol: 'http:',
    host: 'localhost:3000',
    hostname: 'localhost',
    port: '3000',
    pathname: '/',
    search: '',
    hash: '',
    assign: jest.fn(),
    replace: jest.fn(),
    reload: jest.fn(),
  },
  writable: true,
})

// Mock window.history
Object.defineProperty(window, 'history', {
  value: {
    length: 1,
    scrollRestoration: 'auto',
    state: null,
    back: jest.fn(),
    forward: jest.fn(),
    go: jest.fn(),
    pushState: jest.fn(),
    replaceState: jest.fn(),
  },
  writable: true,
})

// Mock window.navigator
Object.defineProperty(window, 'navigator', {
  value: {
    userAgent: 'Mozilla/5.0 (Test Browser)',
    language: 'en-US',
    languages: ['en-US', 'en'],
    cookieEnabled: true,
    onLine: true,
    platform: 'Win32',
    vendor: 'Test Vendor',
    maxTouchPoints: 0,
  },
  writable: true,
})

// Mock window.screen
Object.defineProperty(window, 'screen', {
  value: {
    availHeight: 768,
    availWidth: 1024,
    colorDepth: 24,
    height: 768,
    width: 1024,
    orientation: {
      angle: 0,
      type: 'landscape-primary',
    },
    pixelDepth: 24,
  },
  writable: true,
})

// Mock window.performance
Object.defineProperty(window, 'performance', {
  value: {
    now: jest.fn(() => Date.now()),
    timeOrigin: Date.now(),
    getEntries: jest.fn(() => []),
    getEntriesByName: jest.fn(() => []),
    getEntriesByType: jest.fn(() => []),
    mark: jest.fn(),
    measure: jest.fn(),
    clearMarks: jest.fn(),
    clearMeasures: jest.fn(),
    clearResourceTimings: jest.fn(),
  },
  writable: true,
})

// Mock window.crypto
Object.defineProperty(window, 'crypto', {
  value: {
    getRandomValues: jest.fn((array) => {
      for (let i = 0; i < array.length; i++) {
        array[i] = Math.floor(Math.random() * 256)
      }
      return array
    }),
    randomUUID: jest.fn(() => 'test-uuid'),
  },
  writable: true,
})

// Mock window.URL
global.URL = jest.fn().mockImplementation((url) => ({
  href: url,
  origin: 'http://localhost:3000',
  protocol: 'http:',
  host: 'localhost:3000',
  hostname: 'localhost',
  port: '3000',
  pathname: '/',
  search: '',
  hash: '',
  searchParams: new URLSearchParams(),
  toString: () => url,
}))

// Mock URLSearchParams
global.URLSearchParams = jest.fn().mockImplementation((init) => {
  const params = new Map()
  if (init) {
    if (typeof init === 'string') {
      init.split('&').forEach(pair => {
        const [key, value] = pair.split('=')
        params.set(key, value)
      })
    } else if (Array.isArray(init)) {
      init.forEach(([key, value]) => params.set(key, value))
    }
  }
  return {
    get: jest.fn((key) => params.get(key)),
    getAll: jest.fn((key) => Array.from(params.entries()).filter(([k]) => k === key).map(([, v]) => v)),
    has: jest.fn((key) => params.has(key)),
    set: jest.fn((key, value) => params.set(key, value)),
    append: jest.fn((key, value) => {
      const existing = params.get(key)
      if (existing) {
        params.set(key, existing + ',' + value)
      } else {
        params.set(key, value)
      }
    }),
    delete: jest.fn((key) => params.delete(key)),
    toString: jest.fn(() => Array.from(params.entries()).map(([k, v]) => `${k}=${v}`).join('&')),
  }
})

// Mock AbortController
global.AbortController = jest.fn().mockImplementation(() => ({
  signal: {
    aborted: false,
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
  },
  abort: jest.fn(),
}))

// Mock TextEncoder
global.TextEncoder = jest.fn().mockImplementation(() => ({
  encode: jest.fn((text) => new Uint8Array(Buffer.from(text, 'utf8'))),
  encodeInto: jest.fn(),
}))

// Mock TextDecoder
global.TextDecoder = jest.fn().mockImplementation(() => ({
  decode: jest.fn((buffer) => Buffer.from(buffer).toString('utf8')),
  encoding: 'utf-8',
  fatal: false,
  ignoreBOM: false,
}))

// Mock structuredClone
global.structuredClone = jest.fn((obj) => JSON.parse(JSON.stringify(obj)))

// Mock queueMicrotask
global.queueMicrotask = jest.fn((callback) => Promise.resolve().then(callback))

// Mock requestIdleCallback
global.requestIdleCallback = jest.fn((callback) => setTimeout(callback, 0))

// Mock cancelIdleCallback
global.cancelIdleCallback = jest.fn((id) => clearTimeout(id))

// Mock requestAnimationFrame with better timing
let rafId = 0
global.requestAnimationFrame = jest.fn((callback) => {
  rafId++
  setTimeout(() => callback(rafId), 16) // ~60fps
  return rafId
})

global.cancelAnimationFrame = jest.fn((id) => {
  // Clear the timeout if it exists
  clearTimeout(id)
})

// Mock performance.now with better precision
const startTime = Date.now()
global.performance = {
  ...global.performance,
  now: jest.fn(() => Date.now() - startTime),
}

// Mock IntersectionObserver with better implementation
global.IntersectionObserver = jest.fn().mockImplementation((callback) => ({
  observe: jest.fn((element) => {
    // Simulate intersection
    setTimeout(() => callback([{
      target: element,
      isIntersecting: true,
      intersectionRatio: 1,
      boundingClientRect: element.getBoundingClientRect(),
      rootBounds: null,
      time: Date.now(),
    }]), 0)
  }),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock ResizeObserver with better implementation
global.ResizeObserver = jest.fn().mockImplementation((callback) => ({
  observe: jest.fn((element) => {
    // Simulate resize
    setTimeout(() => callback([{
      target: element,
      contentRect: element.getBoundingClientRect(),
      borderBoxSize: [{ inlineSize: 100, blockSize: 100 }],
      contentBoxSize: [{ inlineSize: 100, blockSize: 100 }],
      devicePixelContentBoxSize: [{ inlineSize: 100, blockSize: 100 }],
    }]), 0)
  }),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock MutationObserver
global.MutationObserver = jest.fn().mockImplementation((callback) => ({
  observe: jest.fn(),
  disconnect: jest.fn(),
  takeRecords: jest.fn(() => []),
}))

// Mock getBoundingClientRect
Element.prototype.getBoundingClientRect = jest.fn(() => ({
  x: 0,
  y: 0,
  width: 100,
  height: 100,
  top: 0,
  right: 100,
  bottom: 100,
  left: 0,
}))

// Mock getClientRects
Element.prototype.getClientRects = jest.fn(() => [{
  x: 0,
  y: 0,
  width: 100,
  height: 100,
  top: 0,
  right: 100,
  bottom: 100,
  left: 0,
}])

// Mock scrollIntoView
Element.prototype.scrollIntoView = jest.fn()

// Mock focus and blur
HTMLElement.prototype.focus = jest.fn()
HTMLElement.prototype.blur = jest.fn()

// Mock click
HTMLElement.prototype.click = jest.fn()

// Mock select
HTMLInputElement.prototype.select = jest.fn()

// Mock setSelectionRange
HTMLInputElement.prototype.setSelectionRange = jest.fn()

// Mock checkValidity
HTMLFormElement.prototype.checkValidity = jest.fn(() => true)

// Mock reportValidity
HTMLFormElement.prototype.reportValidity = jest.fn()

// Mock submit
HTMLFormElement.prototype.submit = jest.fn()

// Mock reset
HTMLFormElement.prototype.reset = jest.fn()

// Mock play and pause for media elements
HTMLMediaElement.prototype.play = jest.fn(() => Promise.resolve())
HTMLMediaElement.prototype.pause = jest.fn()

// Mock canvas methods
HTMLCanvasElement.prototype.getContext = jest.fn(() => ({
  fillRect: jest.fn(),
  clearRect: jest.fn(),
  getImageData: jest.fn(() => ({ data: new Uint8ClampedArray(4) })),
  putImageData: jest.fn(),
  createImageData: jest.fn(() => ({ data: new Uint8ClampedArray(4) })),
  setTransform: jest.fn(),
  drawImage: jest.fn(),
  save: jest.fn(),
  fillText: jest.fn(),
  restore: jest.fn(),
  beginPath: jest.fn(),
  moveTo: jest.fn(),
  lineTo: jest.fn(),
  closePath: jest.fn(),
  stroke: jest.fn(),
  translate: jest.fn(),
  scale: jest.fn(),
  rotate: jest.fn(),
  arc: jest.fn(),
  fill: jest.fn(),
  measureText: jest.fn(() => ({ width: 0 })),
  transform: jest.fn(),
  rect: jest.fn(),
  clip: jest.fn(),
}))

// Mock toDataURL
HTMLCanvasElement.prototype.toDataURL = jest.fn(() => 'data:image/png;base64,test')

// Mock toBlob
HTMLCanvasElement.prototype.toBlob = jest.fn((callback) => {
  const blob = new Blob(['test'], { type: 'image/png' })
  callback(blob)
})

// Mock createObjectURL and revokeObjectURL
global.URL.createObjectURL = jest.fn(() => 'blob:test')
global.URL.revokeObjectURL = jest.fn()

// Mock FileReader
global.FileReader = jest.fn().mockImplementation(() => ({
  readAsText: jest.fn(),
  readAsDataURL: jest.fn(),
  readAsArrayBuffer: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  result: null,
  error: null,
  readyState: 0,
}))

// Mock FormData
global.FormData = jest.fn().mockImplementation(() => ({
  append: jest.fn(),
  delete: jest.fn(),
  get: jest.fn(),
  getAll: jest.fn(),
  has: jest.fn(),
  set: jest.fn(),
  forEach: jest.fn(),
  entries: jest.fn(() => []),
  keys: jest.fn(() => []),
  values: jest.fn(() => []),
}))

// Mock Headers
global.Headers = jest.fn().mockImplementation((init) => {
  const headers = new Map()
  if (init) {
    Object.entries(init).forEach(([key, value]) => {
      headers.set(key.toLowerCase(), value)
    })
  }
  return {
    append: jest.fn((name, value) => headers.set(name.toLowerCase(), value)),
    delete: jest.fn((name) => headers.delete(name.toLowerCase())),
    get: jest.fn((name) => headers.get(name.toLowerCase())),
    has: jest.fn((name) => headers.has(name.toLowerCase())),
    set: jest.fn((name, value) => headers.set(name.toLowerCase(), value)),
    forEach: jest.fn((callback) => headers.forEach(callback)),
    entries: jest.fn(() => headers.entries()),
    keys: jest.fn(() => headers.keys()),
    values: jest.fn(() => headers.values()),
  }
})

// Mock Request
global.Request = jest.fn().mockImplementation((input, init) => ({
  url: typeof input === 'string' ? input : input.url,
  method: (init && init.method) || 'GET',
  headers: new Headers(init && init.headers),
  body: init && init.body,
  mode: (init && init.mode) || 'cors',
  credentials: (init && init.credentials) || 'same-origin',
  cache: (init && init.cache) || 'default',
  redirect: (init && init.redirect) || 'follow',
  referrer: (init && init.referrer) || '',
  integrity: (init && init.integrity) || '',
  clone: jest.fn(),
}))

// Mock Response
global.Response = jest.fn().mockImplementation((body, init) => ({
  body: body,
  bodyUsed: false,
  headers: new Headers(init && init.headers),
  ok: (init && init.status >= 200 && init.status < 300) || true,
  redirected: false,
  status: (init && init.status) || 200,
  statusText: (init && init.statusText) || '',
  type: 'default',
  url: '',
  clone: jest.fn(),
  json: jest.fn(() => Promise.resolve(JSON.parse(body))),
  text: jest.fn(() => Promise.resolve(body)),
  blob: jest.fn(() => Promise.resolve(new Blob([body]))),
  arrayBuffer: jest.fn(() => Promise.resolve(new ArrayBuffer(0))),
  formData: jest.fn(() => Promise.resolve(new FormData())),
}))

// Mock fetch with better implementation
global.fetch = jest.fn((url, options) => {
  return Promise.resolve(new Response('{"success": true}', {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  }))
})

// Mock console methods to reduce noise in tests
const originalConsoleError = console.error
const originalConsoleWarn = console.warn

beforeAll(() => {
  console.error = jest.fn()
  console.warn = jest.fn()
})

afterAll(() => {
  console.error = originalConsoleError
  console.warn = originalConsoleWarn
})